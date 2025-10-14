import os
import base64
import jinja2
import logging
import subprocess
import json
import tempfile
from pathlib import Path
from collections import OrderedDict

import requests

from agent import ClusterAgentConfig, SwarmAgentConfig, Agent
from dataclasses import dataclass
from logging import Logger
from statemachine import RetryingStateMachine
from swarmexecutor import SwarmExecutor
from swarmkubecache import SwarmKubeCache
from taskpool import TaskPool
from withcontainerconfigs import WithContainerConfigs
from threading import Event
from typing import Dict


@dataclass
class ClusterConfig:
    ocm_token: str
    controller_image_path: str
    logging: Logger
    single_node: bool
    num_workers: int
    index: int
    swarm_identifier: str
    storage_dir: Path
    service_mode: str
    service_url: str
    release_image: str
    ssh_pub_key: str
    pull_secret: str
    pull_secret_token: str
    kube_cache: SwarmKubeCache
    task_pool: TaskPool
    num_locks: int
    executor: SwarmExecutor
    shared_graphroot: Path
    can_start_agents: Event
    started_all_agents: Event
    with_nmstate: bool
    just_infraenv: bool
    infraenv_labels: Dict[str, str]
    pull_secret_file: str


class Cluster(RetryingStateMachine, WithContainerConfigs):
    def __init__(self, cluster_config: ClusterConfig, swarm_agent_config: SwarmAgentConfig):
        super().__init__(
            initial_state="Initializing",
            terminal_state="Done",
            states=OrderedDict(
                {
                    "Initializing": self.initialize,
                    "Creating cluster": self.create_cluster,
                    "Creating infraenv": self.create_infraenv,
                    "Generating manifests": self.generate_manifests,
                    "Applying manifests": self.apply_manifests,
                    "Launching agents": self.launch_agents,
                    "Waiting for AgentClusterInstall clusterMetadata infraID": self.wait_for_agentclusterinstall_cluster_metadata_infraid,
                    "Waiting for cluster ready": self.wait_for_cluster_ready,
                    "Triggering cluster install": self.trigger_cluster_install,
                    "Generating container configurations": self.create_container_configs,
                    "Wait for agents to have roles": self.wait_for_agents_to_have_roles_assigned,
                    "Running controller": self.run_controller,
                    "Wait for agents to complete": self.wait_for_agents,
                    "Done": self.done,
                }
            ),
            logging=logging,
            name=f"Cluster {cluster_config.index}",
        )

        self.cluster_config = cluster_config
        self.swarm_agent_config = swarm_agent_config

        self.identifier = f"{cluster_config.swarm_identifier}-{cluster_config.index}"
        self.cluster_dir = cluster_config.storage_dir / self.identifier
        self.manifest_dir = self.cluster_dir / "manifests"
        self.personal_graphroot = self.cluster_dir / "graphroot"

        WithContainerConfigs.__init__(
            self,
            self.personal_graphroot,
            self.cluster_config.shared_graphroot,
            self.cluster_dir,
            self.cluster_config.num_locks,
        )

        assert (
            cluster_config.single_node is False or cluster_config.num_workers == 0
        ), "Cannot have single node with workers"

        self.num_control_plane = 1 if cluster_config.single_node else 3
        self.num_workers = cluster_config.num_workers

        assert (
            self.total_agents <= 2 ** 16 - 4
        ), f"Too many agents in one cluster, {self.total_agents} larger than {2**16 - 4}"

        self.controller_stdout_path = self.cluster_dir / "controller.stdout.logs"
        self.controller_stderr_path = self.cluster_dir / "controller.stderr.logs"

        self.logging = logging

    def agent_directory(self, agent_index):
        return self.cluster_dir / f"agent-{agent_index}"

    def agent_ip(self, agent_index):
        ip_index = agent_index + 1
        # return f"10.123.{ip_index >> 8}.{ip_index & 0xff}/16"
        return f"10.123.{ip_index >> 8}.{ip_index & 0xff}/22"

    def hostname(self, agent_index):
        return f"{self.identifier}-{agent_index}"

    def dry_reboot_marker(self, agent_index):
        return Path("/var/log") / f"{self.identifier}-{agent_index}-cluster_fake_reboot_marker"

    @property
    def cluster_hosts(self):
        return [
            {
                "hostname": self.hostname(agent_index),
                "ip": self.agent_ip(agent_index),
                "rebootMarkerPath": str(self.dry_reboot_marker(agent_index)),
            }
            for agent_index in range(self.total_agents)
        ]

    @property
    def total_agents(self):
        return self.num_control_plane + self.num_workers

    @staticmethod
    def make_mac(cluster_index, agent_index):
        assert cluster_index < 2 ** 24, "Cluster index too large"
        assert agent_index < 2 ** 24, "Agent index too large"

        octets = (
            cluster_index >> 16,
            cluster_index >> 8,
            cluster_index & 0xFF,
            agent_index >> 16,
            agent_index >> 8,
            agent_index & 0xFF,
        )
        return ":".join(f"{o:02x}" for o in octets)

    def create_cluster(self, next_state):
        resp = requests.post(
            f"{self.cluster_config.service_url}/api/assisted-install/v2/clusters",
            headers={"Authorization": f"Bearer {self.cluster_config.ocm_token}"},
            json={
                "name": self.identifier,
                "openshift_version": self.cluster_config.release_image.split(":")[-1].split("-")[0],
                "pull_secret": self.cluster_config.pull_secret,
                "high_availability_mode": "None" if self.cluster_config.single_node else "Full",
                "base_dns_domain": "example.com",
                "user_managed_networking": False,
                "ssh_public_key": self.cluster_config.ssh_pub_key,
                "api_vips": [
                    {
                        # "ip": "10.123.255.253",
                        "ip": "10.123.3.253",
                    },
                ],
                "ingress_vips": [
                    {
                        # "ip": "10.123.255.254",
                        "ip": "10.123.3.254",
                    },
                ],
                "control_plane_count": self.num_control_plane,
            },
        )
        self.logging.info(f"Create cluster response: {resp.status_code} {resp.text}")
        resp.raise_for_status()

        cluster_data = resp.json()
        self.cluster_id = cluster_data["id"]

        self.logging.info(f"Created cluster {self.identifier} in service")
        return next_state

    def create_infraenv(self, next_state):
        resp = requests.post(
            f"{self.cluster_config.service_url}/api/assisted-install/v2/infra-envs",
            headers={"Authorization": f"Bearer {self.cluster_config.ocm_token}"},
            json={
                "name": self.identifier,
                "pull_secret": self.cluster_config.pull_secret,
                "ssh_authorized_key": self.cluster_config.ssh_pub_key,
                "cluster_id": self.cluster_id,
                "cpu_architecture": "x86_64",
                "image_type": "minimal-iso",
            },
        )

        self.logging.info(f"Create infraenv response: {resp.status_code} {resp.text}")

        resp.raise_for_status()

        infraenv_data = resp.json()

        self.infraenv_id = infraenv_data["id"]

        self.logging.info(f"Created infraenv {self.identifier} in service")

        return next_state


    def generate_manifests(self, next_state):
        if self.cluster_config.service_mode != "k8s":
            return next_state

        per_cluster_manifests = [
            "namespace",
            "secret_pull",
            "infraenv",
        ]

        if not self.cluster_config.just_infraenv:
            per_cluster_manifests.extend(
                (
                    "agentclusterinstall",
                    "clusterdeployment",
                    "clusterimageset",
                )
            )

        if self.cluster_config.with_nmstate:
            per_cluster_manifests.append("nmstate")

        per_agent_manifests = (
            "baremetalhost",
            "secret_bmh",
        )

        template_params = {
            "release_image": self.cluster_config.release_image,
            "machine_network": "10.123.0.0/22",
            "ssh_pub_key": self.cluster_config.ssh_pub_key,
            "pull_secret_b64": base64.b64encode(self.cluster_config.pull_secret.encode("utf-8")).decode("utf-8"),
            "num_control_plane": self.num_control_plane,
            "num_workers": self.num_workers,
            "cluster_identifier": self.identifier,
            "single_node": self.cluster_config.single_node,
            "just_infraenv": self.cluster_config.just_infraenv,
            "infraenv_labels": json.dumps(self.cluster_config.infraenv_labels, separators=(",", ":")),
            "api_vip": "10.123.3.253",
            "ingress_vip": "10.123.3.254",
        }

        all_rendered_manifests = []

        def render(manifest_name, **extra_params):
            with (Path("manifests") / f"{manifest_name}.yaml.j2").open() as manifest_file:
                all_rendered_manifests.append(
                    jinja2.Template(manifest_file.read()).render(**template_params, **extra_params)
                )

        for manifest_name in per_cluster_manifests:
            render(manifest_name)

        for agent_index in range(self.total_agents):
            for manifest_name in per_agent_manifests:
                render(
                    manifest_name,
                    mac_address=self.make_mac(self.cluster_config.index, agent_index),
                    agent_identifier=f"{self.identifier}-{agent_index}",
                    role="master" if agent_index < self.num_control_plane else "worker",
                )

        self.manifests = "\n---\n".join(all_rendered_manifests)

        with open(self.manifest_dir / "manifests.yaml", "w") as f:
            f.write(self.manifests)
        return next_state

    def apply_manifests(self, next_state):
        if self.cluster_config.service_mode != "k8s":
            return next_state

        subprocess.run(["oc", "apply", "-f", "-"], input=self.manifests.encode("utf-8"), check=True)

        return next_state

    def initialize(self, next_state):
        for dir in (self.cluster_dir, self.manifest_dir):
            dir.mkdir(parents=True, exist_ok=True)

        return next_state

    def launch_agents(self, next_state):
        self.cluster_config.can_start_agents.wait()

        self.agents = [
            Agent(
                self.swarm_agent_config,
                ClusterAgentConfig(
                    index=agent_index,
                    mac_address=self.make_mac(self.cluster_config.index, agent_index),
                    machine_ip=self.agent_ip(agent_index),
                    machine_hostname=self.hostname(agent_index),
                    cluster_identifier=self.identifier,
                    cluster_dir=self.cluster_dir,
                    identifier=f"{self.identifier}-{agent_index}",
                    cluster_hosts=self.cluster_hosts,
                    agent_dir=self.agent_directory(agent_index),
                    fake_reboot_marker_path=self.dry_reboot_marker(agent_index),
                    infraenv_id=self.infraenv_id,
                ),
            )
            for agent_index in range(self.total_agents)
        ]

        self.agent_tasks = []
        for agent_index, agent in enumerate(self.agents):
            self.logging.info(f"Launching agent {agent_index}")
            self.agent_tasks.append(self.cluster_config.task_pool.submit(agent.start))

        self.cluster_config.started_all_agents.set()

        return next_state

    def wait_for_agents_to_have_roles_assigned(self, next_state):
        if self.cluster_config.service_mode != "saas":
            return next_state

        resp = requests.get(
            f"{self.cluster_config.service_url}/api/assisted-install/v2/clusters/{self.cluster_id}?with_hosts=true",
            headers={"Authorization": f"Bearer {self.cluster_config.ocm_token}"},
        )
        resp.raise_for_status()
        cluster_data = resp.json()
        hosts = cluster_data.get("hosts", [])
        if len(hosts) < self.total_agents:
            self.logging.info(f"Waiting for all agents to register, have {len(hosts)}/{self.total_agents}")
            return self.state

        roles_assigned = all("role" in host and host["role"] in ("master", "worker") for host in hosts)
        if not roles_assigned:
            self.logging.info("Waiting for all agents to have roles assigned")
            return self.state

        self.first_non_bootstrap_master = next(agent for agent in self.agents if agent.identifier == json.loads(next(
            host for host in hosts if host.get("role") == "master" and not host.get("bootstrap", False)
        )["inventory"])["hostname"])

        return next_state

    def run_controller(self, next_state):
        podman_environment = {
            "CONTAINERS_CONF": str(self.container_config),
            # "CONTAINERS_STORAGE_CONF": str(self.container_storage_conf),
        }

        # Arbitrarily choose the first non-bootstrap master's reboot marker path as a signal for the controller that
        # it should start
        fake_reboot_marker_path = self.first_non_bootstrap_master.fake_reboot_marker_path

        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, dir=Path("/var/log/"), prefix="controller_cluster_hosts_"
        ) as cluster_hosts_file:
            cluster_hosts_file.write(json.dumps(self.cluster_hosts))
            cluster_hosts_file_path = cluster_hosts_file.name

        controller_environment = {
            "CLUSTER_ID": self.cluster_id,
            "DRY_ENABLE": "true",
            "INVENTORY_URL": self.cluster_config.service_url,
            "PULL_SECRET_TOKEN": self.cluster_config.pull_secret_token,
            "OPENSHIFT_VERSION": 4.9,  # TODO: Make this configurable? Does it matter in any way?
            "DRY_FAKE_REBOOT_MARKER_PATH": str(fake_reboot_marker_path),
            "SKIP_CERT_VERIFICATION": "true",
            "HIGH_AVAILABILITY_MODE": "false",
            "CHECK_CLUSTER_VERSION": "true",
            "DRY_CLUSTER_HOSTS_PATH": cluster_hosts_file_path,
            "DEBUG": "1",
        }

        controller_mounts = {str(fake_reboot_marker_path.parent): str(fake_reboot_marker_path.parent)}

        controller_ports = {2345}  # For debugging

        podman_command = [
            "podman",
            "run",
            "--authfile",
            self.cluster_config.pull_secret_file,
            "--net=host",
            "--pid=host",
            "--privileged",
            "-it",
            *(f"-p={port}:{port}" for port in controller_ports),
            *(f"-e={var}={value}" for var, value in controller_environment.items()),
            *(f"-v={host_path}:{container_path}" for host_path, container_path in controller_mounts.items()),
            self.cluster_config.controller_image_path,
        ]

        with self.controller_stdout_path.open("ab") as controller_stdout_file:
            with self.controller_stderr_path.open("ab") as controller_stderr_file:
                controller_stdout_file.write(
                    f"Running controller with command: {podman_command} and env {podman_environment}".encode("utf-8")
                )
                controller_process = self.cluster_config.executor.Popen(
                    self.cluster_config.executor.prepare_sudo_command(podman_command, podman_environment),
                    env={**os.environ, **podman_environment},
                    stdin=subprocess.DEVNULL,
                    stdout=controller_stdout_file,
                    stderr=controller_stderr_file,
                )

        if controller_process.wait() != 0:
            self.logging.error(f"Controller exited with non-zero exit code {controller_process.returncode}")
            return self.state

        return next_state

    def wait_for_agents(self, next_state):
        for agent in self.agent_tasks:
            agent.result()

        return next_state

    def wait_for_agentclusterinstall_cluster_metadata_infraid(self, next_state):
        # In k8s the only reasonable way for us to get the cluster ID is through this field
        if self.cluster_config.service_mode != "k8s":
            return next_state

        agent_cluster_install = self.cluster_config.kube_cache.get_agent_cluster_install(
            namespace=self.identifier, name=self.identifier
        )

        if agent_cluster_install is not None:
            infra_id = agent_cluster_install.get("spec", {}).get("clusterMetadata", {}).get("infraID", None)

            if not infra_id:
                return self.state

            self.cluster_id = infra_id

            return next_state

        self.logging.info(f"Waiting for agent cluster install {self.identifier}/{self.identifier} to be created")

        return self.state

    def wait_for_cluster_ready(self, next_state):
        if self.cluster_config.service_mode != "saas":
            return next_state

        resp = requests.get(
            f"{self.cluster_config.service_url}/api/assisted-install/v2/clusters/{self.cluster_id}",
            headers={"Authorization": f"Bearer {self.cluster_config.ocm_token}"},
        )
        
        if not resp.ok:
            self.logging.error(f"Failed to get cluster status: {resp.status_code} {resp.text}")
            return self.state
            
        cluster_data = resp.json()
        cluster_status = cluster_data.get("status", "")
        
        self.logging.info(f"Cluster {self.cluster_id} status: {cluster_status}")
        
        if cluster_status == "ready":
            return next_state
        elif cluster_status in ["error", "cancelled"]:
            self.logging.error(f"Cluster is in error state: {cluster_status}")
            return self.state
        else:
            return self.state

    def trigger_cluster_install(self, next_state):
        if self.cluster_config.service_mode != "saas":
            return next_state

        self.logging.info(f"Triggering installation for cluster {self.cluster_id}")
        
        resp = requests.post(
            f"{self.cluster_config.service_url}/api/assisted-install/v2/clusters/{self.cluster_id}/actions/install",
            headers={"Authorization": f"Bearer {self.cluster_config.ocm_token}"},
        )
        
        if not resp.ok:
            self.logging.error(f"Failed to trigger cluster install: {resp.status_code} {resp.text}")
            return self.state
            
        self.logging.info(f"Successfully triggered installation for cluster {self.cluster_id}")
        return next_state

    def done(self, _):
        return self.state

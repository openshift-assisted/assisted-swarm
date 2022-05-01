import subprocess
import waiting
from swarmexecutor import SwarmExecutor
from assisted_swarm_client.assisted_swarm import SwarmApi

DEFAULT_AGENT_IMAGE = "quay.io/oamizur/assisted-swarm:latest"
DEFAULT_STDOUT_FILE = "/tmp/combined-agent.stdout"
DEFAULT_STDERR_FILE = "/tmp/combined-agent.stderr"


class CombinedAgent:
    def __init__(self, executor: SwarmExecutor, swarm_client: SwarmApi):
        self.executor = executor
        self.swarm_client = swarm_client

    def spawn(self, agent_image=DEFAULT_AGENT_IMAGE, stdout_fname=DEFAULT_STDOUT_FILE,
              stderr_fname=DEFAULT_STDERR_FILE):
        command = ["podman",
                   "run",
                   "--rm",
                   "--net=host",
                   "--privileged",
                   "-v",
                   "/var/log:/var/log",
                   "-v",
                   "/run/udev:/run/udev",
                   "-v",
                   "/dev/disk:/dev/disk",
                   "-v",
                   "/run/systemd/journal/socket:/run/systemd/journal/socket",
                   "-v",
                   "/var/log:/host/var/log:ro",
                   "-v",
                   "/proc/meminfo:/host/proc/meminfo:ro",
                   "-v",
                   "/sys/kernel/mm/hugepages:/host/sys/kernel/mm/hugepages:ro",
                   "-v",
                   "/proc/cpuinfo:/host/proc/cpuinfo:ro",
                   "-v",
                   "/etc/mtab:/host/etc/mtab:ro",
                   "-v",
                   "/sys/block:/host/sys/block:ro",
                   "-v",
                   "/sys/devices:/host/sys/devices:ro",
                   "-v",
                   "/sys/bus:/host/sys/bus:ro",
                   "-v",
                   "/sys/class:/host/sys/class:ro",
                   "-v",
                   "/run/udev:/host/run/udev:ro",
                   "-v",
                   "/dev/disk:/host/dev/disk:ro",
                   "-v",
                   "/opt:/opt:rw",
                   agent_image]

        with open(stdout_fname, "ab") as stdout_file:
            with open(stderr_fname, "ab") as stderr_file:
                self.executor.Popen(
                    command,
                    stdin=subprocess.DEVNULL,
                    stdout=stdout_file,
                    stderr=stderr_file
                )
        self.wait_for_health()

    def wait_for_health(self):
        def get_health_status():
            try:
                self.swarm_client.health()
                return True
            except Exception:
                return False

        waiting.wait(get_health_status,
                     sleep_seconds=1,
                     timeout_seconds=300)

    def stop(self):
        self.swarm_client.exit()

function podman_remote() {
  curl --retry 5 --connect-timeout 30 -L https://github.com/containers/podman/releases/download/v4.1.1/podman-remote-static.tar.gz -o "podman-remote.tar.gz"
  tar -zxvf podman-remote.tar.gz
  mv podman-remote-static /usr/local/bin/podman-remote
  rm -f podman-remote.tar.gz
}

"$@"
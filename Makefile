ASSISTED_SWARM = build/assisted-swarm
IMAGE := $(or $(IMAGE),quay.io/otuchfel/assisted-swarm:latest)

.PHONY: $(ASSISTED_SWARM) build-image generate clean

build-image: $(ASSISTED_SWARM)
	podman build -f Dockerfile.assisted-swarm . -t $(IMAGE)

generate:
	./hack/generate.sh generate_from_swagger

$(ASSISTED_SWARM):
	CGO_ENABLED=1 go build -o $(ASSISTED_SWARM) cmd/main.go

push:
	podman push $(IMAGE)

clean:
	/bin/rm -f $(ASSISTED_SWARM)
	podman image rm $(IMAGE)

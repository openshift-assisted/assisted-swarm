ASSISTED_SWARM = build/assisted-swarm
CONTAINER_COMMAND := $(or $(CONTAINER_COMMAND),docker)
IMAGE := $(or $(IMAGE),quay.io/oamizur/assisted-swarm:latest)
ifeq ($(CONTAINER_COMMAND), docker)
	CONTAINER_COMMAND = $(shell docker -v | cut -f1 -d' ' | tr '[:upper:]' '[:lower:]')
endif

.PHONY: build-image generate clean

build-image: $(ASSISTED_SWARM)
	$(CONTAINER_COMMAND) build -f Dockerfile.assisted-swarm . -t $(IMAGE)

generate:
	CONTAINER_COMMAND="$(CONTAINER_COMMAND)" ./hack/generate.sh generate_from_swagger

$(ASSISTED_SWARM):
	CGO_ENABLED=1 go build -o $(ASSISTED_SWARM) cmd/main.go

push:
	$(CONTAINER_COMMAND) push $(IMAGE)

clean:
	/bin/rm -f $(ASSISTED_SWARM)
	$(CONTAINER_COMMAND) image rm $(IMAGE)

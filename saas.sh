#!/bin/bash

set -euxo pipefail

sudo python3 main.py 6 testplan.example.yaml service_config.example.yaml

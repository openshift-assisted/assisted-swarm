#!/usr/bin/env bash

set -o nounset
set -o pipefail
set -o errexit
set -x

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__root="$(cd "$(dirname "${__dir}")" && pwd)"

UID_FLAGS=${UID_FLAGS--u $(id -u):$(id -u)}

function lint_swagger() {
    spectral lint swagger.yaml
}

function generate_go_server() {
    rm -rf restapi/
    goswagger generate server --template=stratoscale -f ${__root}/swagger.yaml
}

function generate_go_client() {
    rm -rf client/ models/*.go
    goswagger generate client --template=stratoscale -f swagger.yaml
}

function remove_dashes_and_dots() {
    for f in models/*.go ; do
        sed -i 's/Dash//g;s/Dot//g' $f
    done
}

function validate_swagger_file() {
    ! egrep -rq 'Dash|Dot' models/*.go || egrep -r 'Dash|Dot' models/*.go | grep -v //  | awk '\
        {reversed=gensub("Dash","-","g", $2); \
         reversed=gensub("Dot",".","g",reversed); \
         original=gensub("\"","","g", $5);\
         if (match(original, "[.-]") == 0 || index(tolower(reversed), original) == 0)  {\
             printf("Enum value %s does not match go generated value %s. Usage of Dash or Dot in the swagger file is not supported\n", original, $2); \
             exit(-1); \
         }}'
    if [ $? != 0 ] ; then
        echo "Failed validating swagger generated files before replacing Dash (-) and Dot (.) Please see https://github.com/go-swagger/go-swagger/issues/2515"
        exit -1
    fi
}

function generate_python_client() {
  base_dir=assisted_swarm_client
  output_dir=${__root}/${base_dir}
  mkdir -p ${output_dir}
  /bin/rm -rf ${output_dir}/* || /bin/true
  ${CONTAINER_COMMAND} build -f hack/Dockerfile.python-client-generate . -t python-generator:latest && ${CONTAINER_COMMAND} run --user ${UID}:${UID} \
   -v ${output_dir}:/assisted_swarm_client --env SWAGGER_FILE=swagger.yaml --env OUTPUT=/assisted_swarm_client --env BASE_DIR=${base_dir} python-generator:latest
}

function generate_from_swagger() {
    lint_swagger
    generate_go_client
    generate_go_server
    validate_swagger_file
    remove_dashes_and_dots
    generate_python_client
}




function generate_all() {
    generate_from_swagger
    generate_mocks
}

function print_help() {
    echo "The available functions are:"
    compgen -A function | tr "_" "-" | grep "^generate" | awk '{print "\t" $1}'
}

declare -F $@ || (echo "Function \"$@\" unavailable." && print_help && exit 1)

if [ "$1" != "print_help" ]; then
    set -o xtrace
fi

"$@"

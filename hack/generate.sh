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

function generate_python_client() {
    local dest="${BUILD_FOLDER}"
    rm -rf "${dest}"/assisted-service-client/*

    SWAGGER_FILE="${__root}"/swagger.yaml \
        OUTPUT="${dest}"/assisted-service-client/ \
        "${__root}"/tools/generate_python_client.sh
    cd "${dest}"/assisted-service-client/ && \
        python3 "${__root}"/tools/client_package_initializer.py "${dest}"/assisted-service-client/ https://github.com/openshift/assisted-service
    cp "${dest}"/assisted-service-client/dist/assisted-service-client-*.tar.gz "${dest}"
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

function generate_from_swagger() {
    lint_swagger
    generate_go_client
    generate_go_server
    validate_swagger_file
    remove_dashes_and_dots
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

#!/usr/bin/env sh

set -o nounset

temp_swagger_file=$(mktemp)
sed '/pattern:/d' ${SWAGGER_FILE} > ${temp_swagger_file}
temp_config_file=$(mktemp)
echo '{"packageName" : "assisted_swarm", "packageVersion": "1.0.0"}' > ${temp_config_file}
java -jar /opt/swagger-codegen-cli/swagger-codegen-cli.jar generate --lang python --config ${temp_config_file} --output ${OUTPUT} --input-spec ${temp_swagger_file}
for f in $(find ${OUTPUT} -type f) ; do
  sed -i -e "s/^from assisted_swarm\([. ].*import \)/from ${BASE_DIR}.assisted_swarm\1/" \
    -e "s/ assisted_swarm\([.].*\)\$/ ${BASE_DIR}.assisted_swarm\1/" \
    -e "s/^import assisted_swarm\$/import ${BASE_DIR}.assisted_swarm/" \
    -e "s/\([a-z_][a-z_]*[(]\)assisted_swarm[.]/\1${BASE_DIR}.assisted_swarm./" $f
done

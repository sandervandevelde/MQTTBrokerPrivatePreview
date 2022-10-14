#!/bin/bash

## Copyright (c) Microsoft. All rights reserved.
## Licensed under the MIT license. See LICENSE file in the project root for full license information.

function update_ca_certificate_resources()
{
    local cert_path="${1}"

    local full_cert_value=""
    while read -r line
    do
        [[ $line = ----* ]] && continue
        full_cert_value="${full_cert_value}${line}"
    done < $cert_path
    
    local escaped_full_cert_value=$(printf '%s\n' "$full_cert_value" | sed -e 's/[\/&]/\\&/g')

    for file in ${2}/Scenario*/resources/CAC_*
    do
        echo "Updating cert value in file: $file"
        sed -i "s/<<ca-cert-pem-content>>/${escaped_full_cert_value}/" "$file"
    done
}

az cloud register -n centraluseuap --endpoint-active-directory https://login.microsoftonline.com --endpoint-active-directory-graph-resource-id https://graph.windows.net/ --endpoint-active-directory-resource-id https://management.core.windows.net/ --endpoint-gallery https://gallery.azure.com/ --endpoint-management https://management.core.windows.net/ --endpoint-resource-manager https://centraluseuap.management.azure.com/ --suffix-storage-endpoint core.windows.net --suffix-keyvault-dns vault.azure.net

az cloud set --name centraluseuap
## az cloud set --name AzureCloud
az login

az account set -s ${sub_id}

pushd ../cert-gen
./certGen.sh create_root_and_intermediate
popd

update_ca_certificate_resources "../cert-gen/certs/azure-mqtt-test-only.intermediate.cert.pem" ".."

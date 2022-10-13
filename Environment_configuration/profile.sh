#!/bin/bash

## Copyright (c) Microsoft. All rights reserved.
## Licensed under the MIT license. See LICENSE file in the project root for full license information.

export sub_id="d8560037-8993-40ac-b191-4b2d877a9359"
export rg_name="slb-rg"
export ns_name_suffix="${rg_name:0:10}-${sub_id:0:8}"
export base_type="Microsoft.EventGrid/namespaces"
export ns_id_prefix="/subscriptions/${sub_id}/resourceGroups/${rg_name}/providers/Microsoft.EventGrid/namespaces"

echo "Namespace prefix set to ${ns_id_prefix}"

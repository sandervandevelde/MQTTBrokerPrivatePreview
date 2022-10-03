# Copyright (c) Microsoft. All rights reserved.  # Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
set -e

pip install pre-commit
pre-commit install
echo "pre-commit is installed.  use 'pre-commit uninstall' to remove hook"

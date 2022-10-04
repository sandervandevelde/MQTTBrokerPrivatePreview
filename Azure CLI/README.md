## Prerequisites

- We will enable the feature for the subscription ID you shared in the sign up form. If you haven't responded, please fill out this [form](https://forms.office.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbRxdDENSpgZtIq581m55eAQpURURXNEw4UkpTOEdNVTVXSllLQVhBUUo0US4u)

- Azure CLI:

    This quickstart requires Azure CLI version 2.17.1 or later. Run the below command to find the version.

    ```bash 
    az --version
    ```

    To install or upgrade, see [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- Register Private Preview (in Central US EUAP region) by running below command in CLI:
    ```bash
    az cloud register --name Private_Preview --endpoint-active-directory-resource-id https://management.core.windows.net/ --endpoint-resource-manager https://api-dogfood.resources.windows-int.net/ --endpoint-active-directory  https://login.windows-ppe.net/ --endpoint-active-directory-graph-resource-id https://graph.ppe.windows.net/
    ```
- Set Private Preview cloud
    ```bash
    az cloud set --name Private_Preview
    ```
- Login to Private Preview
    ```bash
    az login
    ```
- Resource Group:

    Use portal to create a resource group called "MQTT-Pri-Prev-rg1"





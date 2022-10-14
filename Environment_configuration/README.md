# Instructions for the initial environment setup

Follow these steps to configure Azure CLI and set the common variables that will be used in the each scenario for deploying resources.

1.Make sure you have [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt) installed. Run `az --version` to verify. If it's not installed, run the following command to install it:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```
2. Navigate to the Environment_configuration folder in your cloned repo through `cd ./MQTTBrokerPrivatePreview/Environment_configuration/`
3. Update profile.sh file to specify your subscription id and resource group name.
```bash
sub_id="<<your-subscription-id>>"
rg_name="<<your-resource-name>>"
```
4. Make the scripts executable:
```bash
chmod 700 profile.sh
chmod 700 setupEnv.sh
```
5. Run the following scripts. A browser window will open to complete the login. Make sure you rerun these scripts on every new shell window to set the right variables used in the scripts in the scenarios.
```bash
source profile.sh
./setupEnv.sh
```

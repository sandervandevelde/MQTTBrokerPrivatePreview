# Instructions for the initial environment setup

Follow these steps to configure Azure CLI and set the common variables that will be used in the each scenario for deploying resources. You will need to follow these steps in every new terminal window before testing.

1. Navigate to the Environment_configuration folder in your cloned repo through `cd ./MQTTBrokerPrivatePreview/Environment_configuration/`
2.   Update profile.sh file to specify your subscription id and resource group name.
```bash
sub_id="<<your-subscription-id>>"
rg_name="<<your-resource-name>>"
```
3. Make the scripts executable:
```bash
chmod 700 profile.sh
chmod 700 setupEnv.sh
```
4. Run the following scripts. Make sure you rerun these scripts on every new shell window to set the right variables used in the scripts in the scenarios.
```bash
source profile.sh
./setupEnv.sh
```

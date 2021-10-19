# Creating a function app using az cli


## [Installing AZ CLI on Linux](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)

One step process for installing `az cli` using curl
```
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```
Install step-by-step

Get packages needed for the install process:

**Bash**
```
sudo apt-get update
sudo apt-get install ca-certificates curl apt-transport-https lsb-release gnupg
```
Download and install the Microsoft signing key:

**Bash**
```
curl -sL https://packages.microsoft.com/keys/microsoft.asc |
    gpg --dearmor |
    sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null
```
Add the Azure CLI software repository:

**Bash**
```
AZ_REPO=$(lsb_release -cs)
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" |
    sudo tee /etc/apt/sources.list.d/azure-cli.list
```    
Update repository information and install the azure-cli package:

**Bash**
```
sudo apt-get update
sudo apt-get install azure-cli
```
##
1. Log into azure using the following cmd line `az login`

Option A: Run the following code

```
rg=<resource gropu>
storageName=<storage name>
funtionAppName=<function name>
region=<region>
runtime=<language: c#, python, javascript, java, c# script>
runtimeVersion=<runtime version>
functionVersion=<version [1,2,3]>
# version 3 is latest

az storage account create --name $storageName --location $region --resource-group $rg --sku Standard_LRS
az functionapp create --name $funtionAppName --storage-account $storageName --consumption-plan-location $region --resource-group $rg --os-type Linux --runtime $runtime --runtime-version $runtimeVersion --functions-version $functionVersion
```
Option B: run the shell script
```
$>cd model_deployment/cli

$>./makeFunctionApp.sh

```

#!/bin/bash

rg=coding-forge-rg
storageName=aaaaaaaanewsa
funtionAppName=aaaaaaaafuncapp
region=eastus
runtime=python
runtimeVersion=3.7
functionVersion=3

az storage account create --name $storageName --location $region --resource-group $rg --sku Standard_LRS
az functionapp create --name $funtionAppName --storage-account $storageName --consumption-plan-location $region --resource-group $rg --os-type Linux --runtime $runtime --runtime-version $runtimeVersion --functions-version $functionVersion
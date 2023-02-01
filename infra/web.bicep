param name string
param location string = resourceGroup().location
param tags object = {}

param containerAppsEnvironmentName string
param containerRegistryName string
param imageName string = ''
param keyVaultName string
param serviceName string = 'web'
param postgresDomainName string
param postgresDatabaseName string
param postgresUser string
@secure()
param postgresPassword string = ''


module app 'core/host/container-app.bicep' = {
  name: '${serviceName}-container-app-module'
  params: {
    name: name
    location: location
    tags: union(tags, { 'azd-service-name': serviceName })
    containerAppsEnvironmentName: containerAppsEnvironmentName
    containerRegistryName: containerRegistryName
    secrets: [{
      name: 'postgres-password'
      value: postgresPassword
    }]
    env: [
      {
        name: 'DBHOST'
        value: postgresDomainName
      }
      {
        name: 'DBUSER'
        value: postgresUser
      }
      {
        name: 'DBNAME'
        value: postgresDatabaseName
      }
      {
        name: 'KEY_VAULT_NAME'
        value: keyVault.name
      }
      {
        name: 'DBPASS'
        secretRef: 'postgres-password'
      }
      {
        name: 'RUNNING_IN_PRODUCTION'
        value: 'true'
      }
    ]
    imageName: !empty(imageName) ? imageName : 'nginx:latest'
    keyVaultName: keyVault.name
  }
}

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
  name: keyVaultName
}

output SERVICE_WEB_IDENTITY_PRINCIPAL_ID string = app.outputs.identityPrincipalId
output SERVICE_WEB_NAME string = app.outputs.name
output SERVICE_WEB_URI string = app.outputs.uri
output SERVICE_WEB_IMAGE_NAME string = app.outputs.imageName

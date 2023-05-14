param name string
param location string = resourceGroup().location
param tags object = {}

param identityName string
param containerAppsEnvironmentName string
param containerRegistryName string
param serviceName string = 'web'
param exists bool
param postgresDomainName string
param postgresDatabaseName string
param postgresUser string
@secure()
param postgresPassword string
@secure()
param flaskSecret string

resource webIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}


module app 'core/host/container-app-upsert.bicep' = {
  name: '${serviceName}-container-app-module'
  params: {
    name: name
    location: location
    tags: union(tags, { 'azd-service-name': serviceName })
    identityName: webIdentity.name
    exists: exists
    containerAppsEnvironmentName: containerAppsEnvironmentName
    containerRegistryName: containerRegistryName
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
        name: 'RUNNING_IN_PRODUCTION'
        value: 'true'
      }
      {
        name: 'FLASKSECRET'
        secretRef: 'flasksecret'
      }
      {
        name: 'DBPASS'
        secretRef: 'dbpass'
      }
    ]
    targetPort: 50505
    secrets: [
      {
        name: 'dbpass'
        value: postgresPassword
      }
      {
        name: 'flasksecret'
        value: flaskSecret
      }
    ]
  }
}

output SERVICE_WEB_IDENTITY_PRINCIPAL_ID string = webIdentity.properties.principalId
output SERVICE_WEB_NAME string = app.outputs.name
output SERVICE_WEB_URI string = app.outputs.uri
output SERVICE_WEB_IMAGE_NAME string = app.outputs.imageName

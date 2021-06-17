# Fortinet FlexVM Postman Collection

## Setup

Import the collection and the environment into your Postman client.

Update the variables in the environment with your API username and password.

## The Requests

The Requests are categorized in four groups. Use the request in the **Authenticate** group to obtain a token. The token is used for requests in the other groups.

A successful authentication will update the Postman environment variables with the returned *access_token* and *refresh_token*. A post request test is run in the *Retrieve Authentication token* request. The post request test popultates the taken variables in the Postman environment. The *access_token* is utilized by the requests in the other groups, the *refresh_token* is not currently utilized.

All of the requests have a sample body, except for the *list* request in the **Programs** group. 

- Authenticate
  - Retrieve Authentication token

- Configurations
  - list - Get list of Flex VM Configurations for a Program
  - create - Create a new Configuration under a Program
  - update - Modify a Configuration's name or parameters
  - disable - Disable a Configuration
  - enable - Enable a Configuration

- Programs
  - list - Get list of Flex VM Programs for the account

- Virtual Machines
  - list - Get list of existing VMs for a Configuration
  - create - Create one or more VMs based on a Configuration
  - update - Update a VM to use another Configuration or change its description or end date
  - stop - Stop a VM entitlement
  - reactivate - Reactivate a VM entitlement after being stopped
  - token - Regenerate token for a VM
  - points by serial number - Get point usage for a VM by serial number
  - points by config id - Get point usage for VMs by config id
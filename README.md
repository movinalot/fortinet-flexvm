# Fortinet FortiFlex (FlexVM) Python sample and Postman Collection

## Overview

FortiFlex API allows you to automate tasks such as creating entitlements when integrating with cloud orchestration platforms.

### Authentication

Authentication will be done via OAuth token. To call Flex VM external API, 3rd party applications need to do following steps:

1. Create an API User for the account in [IAM](https://docs.fortinet.com/document/forticloud/21.2.0/identity-access-management-iam/282341/adding-an-api-user).

2. Give desired permission (Admin, ReadWrite, ReadOnly) for FlexVM to the newly created or existing API User. Actions that involve changing or creating data (such as creating a new Configuration or updating a VM) will require ReadWrite permission or above.

3. Call our API at `https://customerapiauth.fortinet.com/api/v1/oauth/token/` to retrieve OAuth token. Request body should be similar to:

    ```json
      {
        "username": "<API Username>",
        "password": "<API Password>",
        "client_id": "flexvm",
        "grant_type": "password"
      }
    ```

    > Refer [here](https://docs.fortinet.com/document/fortiauthenticator/6.1.2/rest-api-solution-guide/498666/oauth-server-token-oauth-token) for more information

4. Call FortiFlex API endpoints with the OAuth token as Authorization header with Bearer scheme.

For example:

  ```python
    Authorization: Bearer BOR1COV9QHUjWs1FMZHS1A42VAe5D3

    V1: https://support.fortinet.com/ES/api/flexvm/v1/
    V2: https://support.fortinet.com/ES/api/fortiflex/v2/
  ```

  ![FortiFlex Parameters](images/fortiflex-parameters.png)

## Setup

### Postman

Import the desired FortiFlex version collection and environment into your Postman client.

Update the variables in the environment with your username and password.

### Python

Create a Virtual Environment, add packages from requirements.txt

Use Environment variables for authentication.

V1

- FLEXVM_ACCESS_USERNAME
- FLEXVM_ACCESS_PASSWORD

V2

- FORTIFLEX_ACCESS_USERNAME
- FORTIFLEX_ACCESS_PASSWORD

Uncomment code after __main__ for desired functions.

## The Requests

The Requests are categorized in four groups. Use the request in the __Authenticate__ group to obtain a token. The token is used for requests in the other groups.

A successful authentication will update the Postman environment variables with the returned *access_token* and *refresh_token*. A post request test is run in the *Retrieve Authentication token* request. The post request test populates the taken variables in the Postman environment. The *access_token* is utilized by the requests in the other groups, the *refresh_token* is not currently utilized.

All of the requests have a sample body, except for the *list* request in the __Programs__ group.

- Authenticate
  - Retrieve Authentication token

- Configurations
  - list - Get list of Flex VM Configurations for a Program
  - create - Create a new Configuration under a Program
  - update - Modify a Configuration's name or parameters
  - disable - Disable a Configuration
  - enable - Enable a Configuration

- Groups
  - list - Get list of Flex VM Token Groups (folders under "My Assets" support.fortinet.com)
  - nexttoken - Get next unused token in specified Group

- Programs
  - list - Get list of Flex VM Programs for the account

- Virtual Machines
  - list - Get list of existing VMs for a Configuration
  - create - Create one or more VMs based on a Configuration
  - update - Update a VM to use another Configuration or change its description or end date
  - stop - Stop a VM entitlement
  - reactivate - Reactivate a VM entitlement after being stopped
  - token - Regenerate token for a VM
  - points
    - by serial number - Get point usage for a VM by serial number
    - points by config ID - Get point usage for VMs by config ID
  
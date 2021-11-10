"""
    FlexVM API
    John McDonough (@movinalot)
    Fortinet

    Checked by sken.ai
"""

import json
import requests

FLEXVM_API_BASE_URI = "https://support.fortinet.com/ES/api/flexvm/v1/"

COMMON_HEADERS = {"Content-type": "application/json", "Accept": "application/json"}


def requests_post(resource_url, json_body, headers):
    """Requests Post"""
    try:
        result = requests.post(resource_url, json=json_body, headers=headers)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error) from error
    if result.ok:
        json_data = json.loads(result.content)
        return_value = json_data
    else:
        return_value = None
    return return_value


def get_token(username, password, client_id, grant_type):
    """Get Authentication Token"""
    print("--> Retieving FlexVM API Token...")

    uri = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

    body = {
        "username": username,
        "password": password,
        "client_id": client_id,
        "grant_type": grant_type,
    }

    results = requests_post(uri, body, COMMON_HEADERS)
    return results


def programs_list(access_token):
    """Retrieve FlexVM Programs List"""
    print("--> Retrieving FlexVM Programs...")

    uri = FLEXVM_API_BASE_URI + "programs/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    results = requests_post(uri, "", headers)
    return results


def configs_create(access_token, program_serial_number, name, cpus, svc_package):
    """Create FlexVM Configuration"""
    print("--> Create FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/create"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {
        "programSerialNumber": program_serial_number,
        "name": name,
        "productTypeId": 1,
        "parameters": [{"id": 1, "value": cpus}, {"id": 2, "value": svc_package}],
    }

    results = requests_post(uri, body, headers)
    return results


def configs_disable(access_token, config_id):
    """Disable FlexVM Configuration"""
    print("--> Disable FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/disable"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {"id": config_id}

    results = requests_post(uri, body, headers)
    return results


def configs_enable(access_token, config_id):
    """Enable FlexVM Configuration"""
    print("--> Enable FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/enable"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {"id": config_id}

    results = requests_post(uri, body, headers)
    return results


def configs_list(access_token, program_serial_number):
    """List FlexVM Configurations"""
    print("--> List FlexVM Configurations...")

    uri = FLEXVM_API_BASE_URI + "configs/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {"programSerialNumber": program_serial_number}

    results = requests_post(uri, body, headers)
    return results


def configs_update(access_token, config_id, name, cpu, svc_package):
    """Update FlexVM Configuration"""
    print("--> Update FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/update"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {
        "id": config_id,
        "name": name,
        "parameters": [{"id": 1, "value": cpu}, {"id": 2, "value": svc_package}],
    }

    results = requests_post(uri, body, headers)
    return results


def vms_create(access_token, config_id, count, description, end_date):
    """Create FlexVM Virtual Machines"""
    print("--> Create FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/create"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {
        "configId": config_id,
        "count": count,
        "description": description,
        "endDate": end_date,
    }

    results = requests_post(uri, body, headers)
    return results


def vms_list(access_token, config_id):
    """List FlexVM Virtual Machines"""
    print("--> List FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {"configId": config_id}

    results = requests_post(uri, body, headers)
    return results


def vms_points_by_config_id(access_token, config_id, start_date, end_date):
    """Retrieve FlexVM Virtual Machines Points by Configuration ID"""
    print("--> Retrieve FlexVM Virtual Machines Points by Configuration ID...")

    uri = FLEXVM_API_BASE_URI + "vms/points"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {"configId": config_id, "startDate": start_date, "endDate": end_date}

    results = requests_post(uri, body, headers)
    return results


def vms_points_by_serial_number(access_token, vm_serial_number, start_date, end_date):
    """Retrieve FlexVM Virtual Machines Points by Configuration ID"""
    print("--> Retrieve FlexVM Virtual Machines Points by Configuration ID...")

    uri = FLEXVM_API_BASE_URI + "vms/points"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {
        "serialNumber": vm_serial_number,
        "startDate": start_date,
        "endDate": end_date,
    }

    results = requests_post(uri, body, headers)
    return results


def vms_update(access_token, vm_serial_number, config_id, description, end_date):
    """Update FlexVM Virtual Machine"""
    print("--> Update FlexVM Virtual Machine...")

    # Only Active Virtual Machines can be updated
    process_update = False
    vm_status = "Not Found"
    vm_list = vms_list(access_token, config_id)
    if vm_list:
        print(vm_list)
        for virtual_machine in vm_list["vms"]:
            if (
                virtual_machine["serialNumber"] == vm_serial_number
                and virtual_machine["status"] == "ACTIVE"
            ):
                process_update = True
                break
            if (
                virtual_machine["serialNumber"] == vm_serial_number
                and virtual_machine["status"] == "STOPPED"
            ):
                vm_status = virtual_machine["status"]
                break

    if process_update:
        uri = FLEXVM_API_BASE_URI + "vms/update"
        headers = COMMON_HEADERS.copy()
        headers["Authorization"] = "Bearer {0}".format(access_token)

        body = {
            "serialNumber": vm_serial_number,
            "configId": config_id,
            "description": description,
            "endDate": end_date,
        }
        results = requests_post(uri, body, headers)
    else:
        results = {
            "error": "Cannot update VM: " + vm_serial_number,
            "configId": config_id,
            "status": vm_status,
        }

    return results


def vms_reactivate(access_token, vm_serial_number):
    """Reactivate FlexVM Virtual Machines"""
    print("--> Reactivate FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/reactivate"
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {0}".format(access_token),
    }
    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


def vms_stop(access_token, vm_serial_number):
    """Stop FlexVM Virtual Machines"""
    print("--> Stop FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/stop"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


def vms_token(access_token, vm_serial_number):
    """Retrieve FlexVM Virtual Machines Token"""
    print("--> Retrieve FlexVM Virtual Machines Token...")

    uri = FLEXVM_API_BASE_URI + "vms/token"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = "Bearer {0}".format(access_token)

    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


if __name__ == "__main__":

    # Get API Token
    API_USERNAME = "api-username-goes-here"
    API_PASSWORD = "api-password-goes-here"
    CLIENT_ID = "flexvm"
    GRANT_TYPE = "password"
    api_token = get_token(API_USERNAME, API_PASSWORD, CLIENT_ID, GRANT_TYPE)
    if api_token:
        print(api_token["access_token"])
        api_access_token = api_token["access_token"]

    # # FlexVM Programs
    # List FlexVM Programs
    programs_list = programs_list(api_access_token)
    if programs_list:
        print(programs_list)

    # # FlexVM Configurations
    # List FlexVM Configurations
    # PROGRAM_SERIAL_NUMBER = 'ELAVMS0000000198'
    # config_list = configs_list(
    #     api_access_token,
    #     PROGRAM_SERIAL_NUMBER
    # )
    # if config_list:
    #     print(config_list)

    # # Create FlexVM Configuration
    # CONFIG_NAME = "create_config"
    # CONFIG_CPUS = 4
    # CONFIG_SVC_PACKAGE = "UTM" # 360, ENT, UTM, FC
    # config_create = configs_create(
    #     api_access_token,
    #     PROGRAM_SERIAL_NUMBER,
    #     CONFIG_NAME,
    #     CONFIG_CPUS,
    #     CONFIG_SVC_PACKAGE
    # )

    # if config_create:
    #     print(config_create)

    # # Disable FlexVM Configuration
    # CONFIG_ID = 584
    # config_disable = configs_disable(
    #     api_access_token,
    #     CONFIG_ID
    # )
    # if config_disable:
    #     print(config_disable)

    # # Enable FlexVM Configuration
    # CONFIG_ID = 584
    # config_enable = configs_enable(
    #     api_access_token,
    #     CONFIG_ID
    # )
    # if config_enable:
    #     print(config_enable)

    # # Update FlexVM Configuration
    # CONFIG_NAME = "update_config"
    # CONFIG_CPUS = 2
    # CONFIG_SVC_PACKAGE = "360" # 360, ENT, UTM, FC
    # CONFIG_ID = 584
    # config_update = configs_update(
    #     api_access_token,
    #     CONFIG_ID,
    #     CONFIG_NAME,
    #     CONFIG_CPUS,
    #     CONFIG_SVC_PACKAGE
    # )
    # if config_update:
    #     print(config_update)

    # # FlexVM Virtual Machines
    # List FlexVM VMs
    # CONFIG_ID = 584
    # vm_list = vms_list(api_access_token, CONFIG_ID)
    # if vm_list:
    #     print(vm_list)

    # # Create FlexVM Virtual Machine
    # CONFIG_ID = 584
    # VM_COUNT = 4
    # VM_DESCR = "VM02 360"
    # VM_END_DATE = "2021-10-11"
    # vm_create = vms_create(
    #     api_access_token,
    #     CONFIG_ID,
    #     VM_COUNT,
    #     VM_DESCR,
    #     VM_END_DATE
    # )

    # if vm_create:
    #     print(vm_create)

    # # Reactivate FlexVM Virtual Machine
    # VM_SERIAL_NUMBER = 'FGVMMLTM21006013'
    # vm_reactivate = vms_reactivate(
    #     api_access_token,
    #     VM_SERIAL_NUMBER
    # )

    # if vm_reactivate:
    #     print(vm_reactivate)

    # # Stop FlexVM Virtual Machine
    # VM_SERIAL_NUMBER = 'FGVMMLTM21006013'
    # vm_stop = vms_stop(
    #     api_access_token,
    #     VM_SERIAL_NUMBER
    # )

    # if vm_stop:
    #     print(vm_stop)

    # # Token for FlexVM Virtual Machine
    # VM_SERIAL_NUMBER = 'FGVMMLTM21006013'
    # vm_token = vms_token(
    #     api_access_token,
    #     VM_SERIAL_NUMBER
    # )

    # if vm_token:
    #     print(vm_token)

    # # Update FlexVM Virtual Machine
    # VM_SERIAL_NUMBER = 'FGVMMLTM21006013'
    # CONFIG_ID = 584
    # VM_DESCR = "VM02 360"
    # VM_END_DATE = "2021-11-11"
    # vm_update = vms_update(
    #     api_access_token,
    #     VM_SERIAL_NUMBER,
    #     CONFIG_ID,
    #     VM_DESCR,
    #     VM_END_DATE
    # )

    # if vm_update:
    #     print(vm_update)

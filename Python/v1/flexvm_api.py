"""
    FlexVM API
    John McDonough (@movinalot)
    Fortinet

    Checked by FortiDevSec
"""

# pylint: disable=too-many-arguments

import json
import os
import sys
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

FLEXVM_API_BASE_URI = "https://support.fortinet.com/ES/api/flexvm/v1/"
FORTICARE_AUTH_URI = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

COMMON_HEADERS = {"Content-type": "application/json", "Accept": "application/json"}


def requests_post(resource_url, json_body, headers):
    """Requests Post"""

    logging.debug(resource_url)
    logging.debug(json_body)
    logging.debug(headers)

    try:
        result = requests.post(resource_url, json=json_body, headers=headers, timeout=20)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error) from error
    if result.ok:
        return_value = json.loads(result.content)
    else:
        logging.debug(result)
        logging.debug(result.content)
        return_value = None
    return return_value


def get_token(username, password, client_id, grant_type):
    """Get Authentication Token"""

    logging.debug(username, password, client_id, grant_type)
    logging.debug("--> Retieving FlexVM API Token...")

    body = {
        "username": username,
        "password": password,
        "client_id": client_id,
        "grant_type": grant_type,
    }

    results = requests_post(FORTICARE_AUTH_URI, body, COMMON_HEADERS)
    return results


def programs_list(access_token):
    """Retrieve FlexVM Programs List"""

    logging.debug(access_token)
    logging.debug("--> Retrieving FlexVM Programs...")

    uri = FLEXVM_API_BASE_URI + "programs/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    results = requests_post(uri, "", headers)
    return results


def configs_create(
    access_token, program_serial_number, name, product_type, cpus, svc_package
):
    """Create FlexVM Configuration"""
    logging.debug("--> Create FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/create"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {
        "programSerialNumber": program_serial_number,
        "name": name,
        "productTypeId": product_type,
        "parameters": [{"id": 1, "value": cpus}, {"id": 2, "value": svc_package}],
    }

    results = requests_post(uri, body, headers)
    return results


def configs_disable(access_token, config_id):
    """Disable FlexVM Configuration"""
    logging.debug("--> Disable FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/disable"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"id": config_id}

    results = requests_post(uri, body, headers)
    return results


def configs_enable(access_token, config_id):
    """Enable FlexVM Configuration"""
    logging.debug("--> Enable FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/enable"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"id": config_id}

    results = requests_post(uri, body, headers)
    return results


def configs_list(access_token, program_serial_number):
    """List FlexVM Configurations"""
    logging.debug("--> List FlexVM Configurations...")

    uri = FLEXVM_API_BASE_URI + "configs/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"programSerialNumber": program_serial_number}

    results = requests_post(uri, body, headers)
    return results


def configs_update(access_token, config_id, name, cpu, svc_package):
    """Update FlexVM Configuration"""
    logging.debug("--> Update FlexVM Configuration...")

    uri = FLEXVM_API_BASE_URI + "configs/update"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {
        "id": config_id,
        "name": name,
        "parameters": [{"id": 1, "value": cpu}, {"id": 2, "value": svc_package}],
    }

    results = requests_post(uri, body, headers)
    return results


def groups_list(access_token):
    """Retrieve FlexVM Programs List"""
    logging.debug("--> Retrieving FlexVM Groups...")

    uri = FLEXVM_API_BASE_URI + "groups/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    results = requests_post(uri, "", headers)
    return results


def groups_nexttoken(access_token, folder_path):
    """Get FlexVM Group Next Token"""
    logging.debug("--> Get FlexVM Group Next Token...")

    uri = FLEXVM_API_BASE_URI + "groups/nexttoken"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"folderPath": folder_path}

    results = requests_post(uri, body, headers)
    return results


def vms_create(access_token, config_id, count, description, end_date):
    """Create FlexVM Virtual Machines"""
    logging.debug("--> Create FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/create"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

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
    logging.debug("--> List FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/list"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"configId": config_id}

    results = requests_post(uri, body, headers)
    return results


def vms_points_by_config_id(access_token, config_id, start_date, end_date):
    """Retrieve FlexVM Virtual Machines Points by Configuration ID"""
    logging.debug("--> Retrieve FlexVM Virtual Machines Points by Configuration ID...")

    uri = FLEXVM_API_BASE_URI + "vms/points"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"configId": config_id, "startDate": start_date, "endDate": end_date}

    results = requests_post(uri, body, headers)
    return results


def vms_points_by_serial_number(access_token, vm_serial_number, start_date, end_date):
    """Retrieve FlexVM Virtual Machines Points by Configuration ID"""
    logging.debug("--> Retrieve FlexVM Virtual Machines Points by Configuration ID...")

    uri = FLEXVM_API_BASE_URI + "vms/points"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {
        "serialNumber": vm_serial_number,
        "startDate": start_date,
        "endDate": end_date,
    }

    results = requests_post(uri, body, headers)
    return results


def vms_update(access_token, vm_serial_number, config_id, description, end_date):
    """Update FlexVM Virtual Machine"""
    logging.debug("--> Update FlexVM Virtual Machine...")

    # Only Active Virtual Machines can be updated
    process_update = False
    vm_status = "Not Found"
    vm_list = vms_list(access_token, config_id)
    if vm_list:
        logging.debug(vm_list)
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
        headers["Authorization"] = f"Bearer {access_token}"

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
    logging.debug("--> Reactivate FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/reactivate"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


def vms_stop(access_token, vm_serial_number):
    """Stop FlexVM Virtual Machines"""
    logging.debug("--> Stop FlexVM Virtual Machines...")

    uri = FLEXVM_API_BASE_URI + "vms/stop"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


def vms_token(access_token, vm_serial_number):
    """Retrieve FlexVM Virtual Machines Token"""
    logging.debug("--> Retrieve FlexVM Virtual Machines Token...")

    uri = FLEXVM_API_BASE_URI + "vms/token"
    headers = COMMON_HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"

    body = {"serialNumber": vm_serial_number}

    results = requests_post(uri, body, headers)
    return results


if __name__ == "__main__":

    # Set credentials in enviroment or locally
    FLEXVM_ACCESS_USERNAME = os.getenv("FLEXVM_ACCESS_USERNAME", "api-username-goes-here")
    FLEXVM_ACCESS_PASSWORD = os.getenv("FLEXVM_ACCESS_PASSWORD", "api-password-goes-here")
    API_CLIENT_ID = os.getenv("API_CLIENT_ID", "flexvm")
    API_GRANT_TYPE = os.getenv("API_GRANT_TYPE", "password")

    # Get API Token
    api_token = get_token(
        FLEXVM_ACCESS_USERNAME, FLEXVM_ACCESS_PASSWORD, API_CLIENT_ID, API_GRANT_TYPE
    )
    if api_token:
        api_access_token = api_token["access_token"]
        LOG_MESSAGE = f"API access_token: {api_access_token}"
        logging.debug(LOG_MESSAGE)
        api_access_token = api_token["access_token"]
    else:
        sys.exit("error retreiving api access token")

    # ### FlexVM Programs ###
    # List FlexVM Programs
    programs_list = programs_list(api_access_token)
    if programs_list:
        print(programs_list)

    # ### FlexVM Configurations ###
    # # List FlexVM Configurations
    #
    # PROGRAM_SERIAL_NUMBER = 'ELAVMS0000000000'
    # config_list = configs_list(
    #     api_access_token,
    #     PROGRAM_SERIAL_NUMBER
    # )
    # if config_list:
    #     print(config_list)

    # # Create FlexVM Configuration
    # CONFIG_NAME = "create_config"
    # PRODUCT_TYPE_ID = 1 # FortiGate -> 1 FortiWeb -> 3
    # CONFIG_CPUS = 4
    # CONFIG_SVC_PACKAGE = "UTM" # FortiGate -> ENT, UTM, FC FortiWeb -> FWBSTD, FWBADV
    # config_create = configs_create(
    #     api_access_token,
    #     PROGRAM_SERIAL_NUMBER,
    #     CONFIG_NAME,
    #     PRODUCT_TYPE_ID,
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
    # CONFIG_SVC_PACKAGE = "ENT" # FortiGate -> ENT, UTM, FC fotiWeb -> FWBSTD
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

    # ### FlexVM Groups ###
    # # List FlexVM Groups
    # groups_list = groups_list(api_access_token)
    # if groups_list:
    #     print(groups_list)

    # # Get FlexVM Group Next Token
    # FOLDER_PATH = 'My Assets'
    # groups_nexttoken = groups_nexttoken(
    #     api_access_token,
    #     FOLDER_PATH
    # )

    # if groups_nexttoken:
    #     print(groups_nexttoken)

    # ### FlexVM Virtual Machines ###
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

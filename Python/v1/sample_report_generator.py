"""
    Sample report generator

    Based on FlexVM API, created by Daniel Romio (@Forti-Cloud-BDE) - Fortinet

    Checked by FortiDevSec
"""

# pylint: disable=too-many-arguments

from datetime import datetime, timedelta
import logging
import json
import os
import sys
import pandas as pd
import requests


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

FLEXVM_API_BASE_URI = "https://support.fortinet.com/ES/api/flexvm/v1/"
FORTICARE_AUTH_URI = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

COMMON_HEADERS = {"Content-type": "application/json", "Accept": "application/json"}


def requests_post(resource_url, json_body, headers):
    """Requests Post"""

    logging.debug(resource_url)
    logging.debug(json_body)
    logging.debug(headers)

    try:
        result = requests.post(
            resource_url, json=json_body, headers=headers, timeout=20
        )
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


def get_first_date_of_current_month(year, month):
    """Return the first date of the month.

    Args:
        year (int): Year
        month (int): Month

    Returns:
        date (datetime): First date of the current month
    """
    first_date = datetime(year, month, 1)
    return first_date.strftime("%Y-%m-%d")


def get_last_date_of_month(year, month):
    """Return the last date of the month.

    Args:
        year (int): Year, i.e. 2022
        month (int): Month, i.e. 1 for January

    Returns:
        date (datetime): Last date of the current month
    """

    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) + timedelta(days=-1)

    return last_date.strftime("%Y-%m-%d")


# Recommended to set the variables in your desktop emvironment

FLEXVM_ACCESS_USERNAME = os.getenv("FLEXVM_ACCESS_USERNAME", "api-username-goes-here")
FLEXVM_ACCESS_PASSWORD = os.getenv("FLEXVM_ACCESS_PASSWORD", "api-password-goes-here")
API_CLIENT_ID = os.getenv("API_CLIENT_ID", "flexvm")
API_GRANT_TYPE = os.getenv("API_GRANT_TYPE", "password")


# Get API Token
api_token = get_token(FLEXVM_ACCESS_USERNAME, FLEXVM_ACCESS_PASSWORD, API_CLIENT_ID, API_GRANT_TYPE)
if api_token:
    api_access_token = api_token["access_token"]
    LOG_MESSAGE = f"API access_token: {api_access_token}"
    logging.debug(LOG_MESSAGE)
    api_access_token = api_token["access_token"]
else:
    sys.exit("error retreiving api access token")


programs_list = programs_list(api_access_token)
if programs_list:
    print(programs_list)

# Create a dataframe to store the programs
programs = pd.DataFrame(programs_list["programs"])

# Please, replace this variable with the relevant program SN for your environment
# Example : MY_PROGRAM = 'ELAVMS0000000467'
MY_PROGRAM = ""


# Create a dataframe to store the configs
configs = pd.DataFrame(configs_list(api_access_token, MY_PROGRAM)["configs"])

# Lists of selected dataframe columns to keep from the dataframes
conf_cols = ["id", "name", "productType", "programSerialNumber", "status"]
vms_cols = ["serialNumber", "description", "endDate", "token", "tokenStatus"]
points_cols = []

# Using the current month start and end dates
# Feel free to change them to your needs
r_start_date = get_first_date_of_current_month(datetime.now().year, datetime.now().month)
r_end_date = get_last_date_of_month(datetime.now().year, datetime.now().month)

print(r_start_date)
print(r_end_date)

# For each CONFIG available and for the date range selected,
# print the config name, ID & parameters, the VM list associated
# and the points consumed by VM.

for idx in range(configs.shape[0]):
    print("#" * 120 + "\n" + "#" * 120 + "\n")
    print("\nConfig\n------\n")
    print(configs.iloc[idx][conf_cols].to_markdown(tablefmt="grid"))
    print("\nConfig Parameters\n-----------------\n")
    print(
        pd.DataFrame(configs.iloc[idx]["parameters"]).to_markdown(
            tablefmt="grid", index=False
        )
    )
    print("\nVM list\n-------\n")
    prog = int(configs.iloc[idx]["id"])
    vms = pd.DataFrame(vms_list(api_access_token, prog)["vms"])
    if vms.shape[0] != 0:
        print(vms[vms_cols].to_markdown(tablefmt="grid", index=False))
    else:
        print("No VMs available for this config")
    print("\n")
    print("\nPoints by Config\n--------------\n")
    print("Start Date: " + r_start_date)
    print("End Date: " + r_end_date)
    points = vms_points_by_config_id(api_access_token, prog, r_start_date, r_end_date)
    if points["vms"] != []:
        print(
            pd.DataFrame(points["vms"])[["serialNumber", "points"]].to_markdown(
                tablefmt="grid", index=False
            )
        )
    else:
        print("No consumption identified")
    print("\n")

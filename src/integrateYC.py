import time
import jwt
import requests
import json
import os

CLOUD_ID = os.environ.get("CLOUD_ID")
FOLDER_ID = os.environ.get("FOLDER_ID")
SUBNET_ID = os.environ.get("SUBNET_ID")
IMAGE_ID = os.environ.get("IMAGE_ID")
YC_SERVICE_ACCOUNT_ID = os.environ.get("YC_SERVICE_ACCOUNT_ID")
YC_SERVICE_ACCOUNT_KEY_ID = os.environ.get("YC_SERVICE_ACCOUNT_KEY_ID")

# Get IAM-Token
# Step 1. Get JWT
def get_jwt_token():

    with open("key.txt", "r") as private:
        private_key = private.read()  # Reading the private key from the file.

    now = int(time.time())
    payload = {
        "aud": "https://iam.api.cloud.yandex.net/iam/v1/tokens",
        "iss": YC_SERVICE_ACCOUNT_ID,
        "iat": now,
        "exp": now + 360,
    }

    # JWT generation.
    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm="PS256",
        headers={"kid": YC_SERVICE_ACCOUNT_KEY_ID},
    )

    return encoded_token


# step 2. Exchange the JWT for an IAM token
def exchange_jwt_to_iam(encoded_token):
    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    headers = {"Content-Type": "application/json", "jwt": str(encoded_token)}
    resp = requests.post(url, json=headers)
    resp = resp.json()

    resp = resp.get("iamToken")

    return str(resp)


def get_iam_local():
    token = get_jwt_token()
    iam_access_token = exchange_jwt_to_iam(token)

    return str(iam_access_token)


def get_iam_serverless():
    url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {"Metadata-Flavor": "Google"}
    resp = requests.get(url, headers=headers)
    resp = resp.json()

    return str(resp.get("access_token"))


def get_organizations(access_token):
    url = "https://organization-manager.api.cloud.yandex.net/organization-manager/v1/organizations"
    token = "Bearer " + access_token
    headers = {"Authorization": token}

    resp = requests.get(url, headers=headers)
    print(resp)
    resp = resp.json()

    return resp

def get_clouds(access_token, organization):
    url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/clouds?organizationId=" + organization
    token = "Bearer " + access_token
    headers = {"Authorization": token}

    resp = requests.get(url, headers=headers)
    
    return resp.json()


def get_folders(access_token, cloud=CLOUD_ID):
    url = "https://resource-manager.api.cloud.yandex.net/resource-manager/v1/folders?cloudId=" + cloud # CLOUD_ID)
    token = "Bearer " + access_token
    headers = {"Authorization": token}

    resp = requests.get(url, headers=headers)
    resp = resp.json()

    return resp


def get_instances_list(access_token, folder_id):
    url = "https://compute.api.cloud.yandex.net/compute/v1/instances?folderId=" + folder_id

    token = "Bearer " + access_token
    headers = {"Authorization": token}

    resp = requests.get(url, headers=headers)
    resp = resp.json()

    instances = resp.get("instances")
    if instances == None:
        return "Empty"
        
    instance_info = {}  # {id1: {}, id2:[]}

    for instance in instances:
        instance_info.update({instance.get("id"): {}})

        interfaces = instance.get("networkInterfaces")
        for interface in interfaces:
            primaryV4Address = (
                interface.get("primaryV4Address").get("oneToOneNat").get("address")
            )

            instance_info.get(instance.get("id")).update(
                {"external_ip": primaryV4Address}
            )

    #print(instances)
    return instance_info


def stop_vm(access_token, vm_id):
    url = "https://compute.api.cloud.yandex.net/compute/v1/instances/" + vm_id + ":stop"
    token = "Bearer " + access_token
    headers = {"Authorization": token}
    resp = requests.post(url, headers=headers)
    resp = resp.json()

    return str(resp)


def start_vm(access_token, vm_id):
    url = (
        "https://compute.api.cloud.yandex.net/compute/v1/instances/" + vm_id + ":start"
    )
    token = "Bearer " + access_token
    headers = {"Authorization": token}
    resp = requests.post(url, headers=headers)
    resp = resp.json()

    return str(resp)


def restart_vm(access_token, vm_id):
    url = (
        "https://compute.api.cloud.yandex.net/compute/v1/instances/"
        + vm_id
        + ":restart"
    )

    token = "Bearer " + access_token
    headers = {"Authorization": token}
    resp = requests.post(url, headers=headers)
    print(resp.text)
    resp = resp.json()

    return str(resp)


def create_vm(
    access_token, folder_id=FOLDER_ID, image_id=IMAGE_ID, subnet_id=SUBNET_ID
):
    url = "https://compute.api.cloud.yandex.net/compute/v1/instances"
    token = "Bearer " + access_token
    headers = {"Authorization": token, "Content-Type": "applications/json"}

    # TODO: 1. set config
    # mkpasswd -m sha-512
    with open("configs/default.json", "r") as data:
        config = data.read()

    config = json.loads(config)
    config["folderId"] = folder_id
    config["bootDiskSpec"]["diskSpec"]["imageId"] = image_id
    config["networkInterfaceSpecs"][0]["subnetId"] = subnet_id

    # TODO !!!!
    # if rs.status != 200:
    #    rs.status.code ...
    #   rs.raise_for_status()
    #   rs.text

    resp = requests.post(url, headers=headers, data=str(json.dumps(config)))
    print(resp)
    resp = resp.json()

    return str(resp)


def delete_vm(access_token, vm_id):
    url = "https://compute.api.cloud.yandex.net/compute/v1/instances/" + vm_id
    token = "Bearer " + access_token
    headers = {"Authorization": token}
    resp = requests.delete(url, headers=headers)
    resp = resp.json()

    return str(resp)

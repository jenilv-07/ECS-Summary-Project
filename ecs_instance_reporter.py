import json
from datetime import datetime
import os
import ipaddress
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkecs.v2 import EcsClient, ListServersDetailsRequest, ListFlavorsRequest
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion

# Function to get ECS client
def get_ecs_client():
    """
    Initializes and returns the ECS client using environment variables.
    Raises a ValueError if any required environment variables are missing.
    Returns:
        EcsClient: Initialized ECS client.
    """
    # Access environment variables
    ak = os.environ.get('HUAWEI_ACCESS_KEY')
    sk = os.environ.get('HUAWEI_SECRET_KEY')
    project_id = os.environ.get('HUAWEI_PROJECT_ID')
    region = os.environ.get('HUAWEI_REGION')

    # Ensure all necessary environment variables are set
    if not all([ak, sk, project_id, region]):
        raise ValueError("One or more environment variables are not set.")

    # Set up the credentials
    credentials = BasicCredentials(ak, sk, project_id)

    # Initialize and return the ECS client with the correct region
    return EcsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(EcsRegion.value_of(region)) \
        .build()

def get_flavor_dict(client):
    """
    Fetches the list of flavors and creates a dictionary mapping flavor IDs to flavor details.
    Args:
        client (EcsClient): The ECS client used to send the request.
    Returns:
        dict: A dictionary mapping flavor IDs to flavor details.
    """
    flavor_request = ListFlavorsRequest()

    try:
        # Send the request and get the flavor response
        flavor_response = client.list_flavors(flavor_request)
        # Map flavor IDs to flavor details
        return {flavor.id: flavor for flavor in flavor_response.flavors}

    except Exception as e:
        raise RuntimeError(f"Failed to fetch flavors: {str(e)}")

def is_private_ip(ip):
    """
    Checks if the given IP address is private.
    Args:
        ip (str): The IP address to check.
    Returns:
        bool: True if the IP is private, False otherwise.
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False  # Return False if the IP address is invalid

def get_ecs_servers(client, flavor_dict):
    """
    Fetches ECS server details and maps them with the corresponding flavor details.
    Args:
        client (EcsClient): The ECS client used to send the request.
        flavor_dict (dict): A dictionary containing flavor details keyed by flavor ID.
    Returns:
        list: A list of ECS server information.
    """
    server_request = ListServersDetailsRequest()

    try:
        # Send the request and get the server response
        server_response = client.list_servers_details(server_request)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch ECS servers: {str(e)}")

    ecs_data = []

    # Iterate over each server and extract relevant details
    for server in server_response.servers:
        flavor = flavor_dict.get(server.flavor.id)
        flavor_spec = f"{flavor.name} | {flavor.vcpus} vCPUs | {flavor.ram / 1024} GiB | {flavor.id}" if flavor else "Flavor details not available"

        # Server Summary
        server_summary = {
            'Name': server.name,
            'ID': server.id,
            'Status': server.status,
            'Flavor': flavor_spec,
            'Created': server.created,
            'Updated': server.updated,
            'Image ID': server.image.id,
            'Key Name': server.key_name,
            'Region': os.environ.get('HUAWEI_REGION')
        }

        # Network Interfaces
        network_interfaces = []
        for net_name, net_info in server.addresses.items():
            for addr in net_info:
                # Determine whether the IP is private or public
                ip_type = 'private' if is_private_ip(addr.addr) else 'public'
                interface_info = {
                    'Network Name': net_name,
                    'Address': addr.addr,
                    'Type': ip_type,  # Set based on public/private check
                    'MAC Address': getattr(addr, 'mac_addr', None),
                    'Version': getattr(addr, 'version', None)
                }
                network_interfaces.append(interface_info)

        # Security Groups
        security_groups = [sg.name for sg in server.security_groups]

        # Additional placeholders
        monitoring = {}  # Add monitoring data extraction logic here
        tags = server.metadata  # Assuming metadata contains tags
        cloud_backup = {}  # Add cloud backup data extraction logic here
        host_security = {}  # Add host security data extraction logic here

        ecs_info = {
            'Server Summary': server_summary,
            'Network Interfaces': network_interfaces,
            'Security Groups': security_groups,
            'Monitoring': monitoring,
            'Tags': tags,
            'Cloud Backup': cloud_backup,
            'Host Security': host_security
        }

        ecs_data.append(ecs_info)

    return ecs_data

def save_data_to_json(ecs_data, filename):
    """
    Saves ECS data to a JSON file.
    Args:
        ecs_data (list): The ECS data to be saved.
        filename (str): The name of the file where the data will be saved.
    """
    try:
        with open(filename, 'w') as json_file:
            json.dump(ecs_data, json_file, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to save data to JSON file: {str(e)}")

def main():
    """
    Main function to retrieve ECS instances and flavors and save the data to a JSON file.
    """
    try:
        ecs_client = get_ecs_client()
        flavor_dict = get_flavor_dict(ecs_client)
        ecs_data = get_ecs_servers(ecs_client, flavor_dict)

        # Get the current date and time for the filename
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        ak = os.environ.get('HUAWEI_ACCESS_KEY')
        project_id = os.environ.get('HUAWEI_PROJECT_ID')
        region = os.environ.get('HUAWEI_REGION')

        # Format filename with environment variables and timestamp
        json_filename = f'ecs_summary_{ak}_{project_id}_{region}_{current_time}.json'
        
        # Save the ECS data to JSON
        save_data_to_json(ecs_data, json_filename)
        print(f"Data saved to {json_filename}")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except RuntimeError as re:
        print(f"Runtime Error: {re}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()

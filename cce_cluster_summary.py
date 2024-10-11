import os
import json
import logging
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcce.v3 import CceClient, ListClustersRequest, ShowClusterRequest
from huaweicloudsdkcce.v3.region.cce_region import CceRegion

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def serialize_endpoints(endpoints):
    """
    Convert endpoints to a JSON-serializable format.

    Args:
        endpoints (list): List of endpoint objects.

    Returns:
        list: List of dictionaries containing endpoint details.
    """
    return [{'url': endpoint.url, 'type': endpoint.type} for endpoint in endpoints]

def get_cce_summary():
    """
    Fetches and stores the summary of CCE clusters in a JSON file.

    Raises:
        ValueError: If required environment variables are not set.
        Exception: For any errors during API requests or data processing.
    """
    try:
        # Access environment variables for credentials
        ak = os.environ.get('HUAWEI_ACCESS_KEY')
        sk = os.environ.get('HUAWEI_SECRET_KEY')
        project_id = os.environ.get('HUAWEI_PROJECT_ID')
        region = os.environ.get('HUAWEI_REGION')

        # Ensure all necessary environment variables are set
        if not all([ak, sk, project_id, region]):
            raise ValueError("One or more environment variables are not set.")

        # Set up the credentials
        credentials = BasicCredentials(ak, sk, project_id)

        # Initialize the CCE client with the correct region
        cce_client = CceClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(CceRegion.value_of(region)) \
            .build()

        # Create a request to list CCE clusters
        list_clusters_request = ListClustersRequest()

        # Send the request and get the response
        clusters_response = cce_client.list_clusters(list_clusters_request)

        # Extract and format the data
        cce_data = []
        for cluster_summary in clusters_response.items:
            # Fetch detailed information for each cluster
            cluster_id = cluster_summary.metadata.uid
            show_cluster_request = ShowClusterRequest(cluster_id=cluster_id)

            # Get the response
            cluster_response = cce_client.show_cluster(show_cluster_request)
            
            # Assuming the correct attribute to access the cluster details
            cluster_detail = cluster_response

            # Collect detailed information
            cluster_info = {
                'Cluster Name': cluster_detail.metadata.name,
                'Cluster ID': cluster_detail.metadata.uid,
                'Status': cluster_detail.status.phase,
                'Created': cluster_detail.metadata.creation_timestamp,
                'Version': cluster_detail.spec.version,
                'Cluster Type': cluster_detail.spec.type,
                'Flavor': cluster_detail.spec.flavor,
                'Region': region,
                'Network Mode': getattr(cluster_detail.spec.host_network, 'mode', 'N/A'),
                'Container Network': cluster_detail.spec.container_network.mode,
                'Authentication': cluster_detail.spec.authentication.mode,
                'Billing Mode': cluster_detail.spec.billing_mode,
                'Labels': cluster_detail.metadata.labels,
                'Annotations': cluster_detail.metadata.annotations,
                'Endpoints': serialize_endpoints(cluster_detail.status.endpoints)
            }
            cce_data.append(cluster_info)

        # Convert the data to JSON format
        cce_data_json = json.dumps(cce_data, indent=4)

        # Save the JSON data to a file
        with open('cce_clusters_detailed_info.json', 'w') as json_file:
            json_file.write(cce_data_json)
        
        logging.info("CCE cluster summary has been saved to 'cce_clusters_detailed_info.json'.")

    except ValueError as ve:
        logging.error("ValueError: %s", ve)
    except Exception as e:
        logging.exception("An error occurred while fetching the CCE cluster summary: %s", e)

if __name__ == "__main__":
    get_cce_summary()

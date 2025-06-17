from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

def list_adls_gen2_container_blobs(account_url, container_name, account_key):
    """
    List blobs in an ADLS Gen2 container using account key authentication.
    :param account_url: The URL of the storage account (e.g., 'https://<account>.dfs.core.windows.net')
    :param container_name: The name of the container
    :param account_key: The storage account key
    """
    service_client = BlobServiceClient(account_url=account_url, credential=account_key)
    container_client = service_client.get_container_client(container_name)
    print(f"Blobs in container '{container_name}':")
    for blob in container_client.list_blobs():
        print(blob.name)

def list_adls_gen2_container_blobs_with_credential(account_url, container_name):
    """
    List blobs in an ADLS Gen2 container using Azure AD credentials (DefaultAzureCredential).
    :param account_url: The URL of the storage account (e.g., 'https://<account>.dfs.core.windows.net')
    :param container_name: The name of the container
    """
    credential = DefaultAzureCredential()
    service_client = BlobServiceClient(account_url=account_url, credential=credential)
    container_client = service_client.get_container_client(container_name)
    print(f"Blobs in container '{container_name}':")
    for blob in container_client.list_blobs():
        print(blob.name)

# Example usage (replace with your actual values):
# account_url = "https://<your-storage-account>.dfs.core.windows.net"
# container_name = "<your-container-name>"
# account_key = "<your-account-key>"
# list_adls_gen2_container_blobs(account_url, container_name, account_key)
# list_adls_gen2_container_blobs_with_credential(account_url, container_name)
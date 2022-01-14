import json
import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from decouple import config


def printBlobsInContainer(container):
    total_size = 0

    print(f"Container {container.container_name}:")
    for blob in container.list_blobs():
        print(f"\t{blob.name} {blob.size}")
        total_size += blob.size

        stream = container.download_blob(blob)
        s = stream.content_as_text()
        print(s)

    print(f"Total size: {total_size//1024}Kb")


def main():
    connection_string = config('AZURE_STORAGE_CONNECTION_STRING')
    if not connection_string:
        print("Please, set AZURE_STORAGE_CONNECTION_STRING env variable!")
        return

    print("Connecting to Azure Blob service...")
    service = BlobServiceClient.from_connection_string(connection_string)

    print("\nConnected! Properties:")
    properties = service.get_service_properties()
    print(properties)

    print("\n*** Containers:")
    for container_props in service.list_containers():
        container = service.get_container_client(container_props.name)

        printBlobsInContainer(container)


if __name__ == "__main__":
    main()

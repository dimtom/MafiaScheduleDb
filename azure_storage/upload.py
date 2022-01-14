import json
import os
import os.path

import azure.core.exceptions
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from decouple import config


def uploadToAzure(connection_string, container_name, data_directory):
    service = BlobServiceClient.from_connection_string(connection_string)

    try:
        container = service.create_container(container_name)
    except azure.core.exceptions.ResourceExistsError:
        print(f"Azure container already exists: {container_name}")

    container = service.get_container_client(container_name)
    print(container.get_container_properties())

    print(f"\nUploading schedules to Azure Blobs from: {data_directory} ")

    count = 0
    for root, dirs, files in os.walk(data_directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext != ".txt":
                print(f"\nSkipping file: {filename}")
                continue

            full_filename = os.path.join(root, filename)
            print(f"\nLoading from file: {full_filename}")
            with open(full_filename) as f:
                print(f"Loading JSON fron file: {filename}")
                s = json.load(f)
                str = json.dumps(s)

                blob = service.get_blob_client(container_name, name)
                if blob.exists():
                    print("Warning! Overwriting the data!")

                print(f"Uploading {len(str)} bytes to blob: {name}")
                blob.upload_blob(str, overwrite=True)
                count += 1

    print(f"Total number of files uploaded: {count}")


def main():
    connection_string = connection_string = config(
        'AZURE_STORAGE_CONNECTION_STRING')
    container_name = "schedules"
    data_directory = os.path.abspath("../data")
    uploadToAzure(connection_string, container_name, data_directory)


if __name__ == "__main__":
    main()

from google.cloud import storage
import os
import tempfile


storage_bucket = os.environ.get("storage_bucket")
storage_path = os.environ.get("storage_path")
# Find the temporary storage path
path = tempfile.gettempdir()


def download_alarm_configs(apps):
    global path

    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    # for now, windows has not been considered which will be taken
    # into account later
    storage_bucket = "eviden-ai-poc"
    storage_path = "alert-configs/linux"

    storage_client = storage.Client()

    bucket = storage_client.bucket(storage_bucket)

    for app in apps:
        source_blob_name = f"{storage_path}/{app}-alerts"
        destination_file = f"{path}/{app}-alerts"
        
        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file)

        print(
            "Downloaded storage object {} from bucket {} to local file {}.".format(
                source_blob_name, storage_bucket, destination_file
            )
        )


def process_alerts(apps,instance_id):
    # Step 1: Download alerts configs
    download_alarm_configs(apps)
    # Step 2: Read all configs, merge and put in a file
    #alert_configuration = f"{path}/alert_configuration"
    file_contents = f"""#instanceid:{instance_id}
 
 """
    # Adding new line character
    new_line = """
 """

    for app in apps:
        destination_file = f"{path}/{app}-alerts"
        file = open(destination_file, "r")
        temporary_contents = file.read()
        file_contents = file_contents + temporary_contents \
                            + new_line
    
    print(file_contents)
    return file_contents

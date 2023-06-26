from flask import Flask, request
from googleapiclient import discovery
import storageHandler
import updateGithub


app = Flask(__name__)
service = discovery.build('compute', 'v1')


def get_metadata(project_id,zone,compute_name):
    # Request metadata
    request = service.instances(). \
            get(project=project_id,zone=zone,instance=compute_name)

    # Execute the request
    response = request.execute()

    # Retrieve the metadata field
    metadata = response['metadata']

    # Print metadata
    #print(metadata)

    application_names = ""

    for item in metadata["items"]:
        if item.get("key") == "apps":
            application_names =  item.get("value").split(";")

    return application_names


@app.route("/", methods=['POST'])
def get_event():

    envelope = request.get_json()

    if not envelope:
        msg = "No message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    #print(envelope)

    instance_id = envelope["resource"]["labels"]["instance_id"]
    zone = envelope["resource"]["labels"]["zone"]
    project_id = envelope["resource"]["labels"]["project_id"]
    compute_name = envelope["protoPayload"]["resourceName"]
    compute_name = compute_name[compute_name.rindex("/")+1:len(compute_name)]
    
    print(instance_id)

    print(zone)

    print(project_id)

    print(compute_name)

    application_names = get_metadata(project_id,zone,compute_name)

    file_contents = storageHandler.process_alerts(application_names, \
                                                  instance_id)

    updateGithub.process_github_commit(file_contents)

    return ("Completed.", 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

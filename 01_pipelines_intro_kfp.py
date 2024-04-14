from typing import NamedTuple

import google.cloud.aiplatform as aip
from kfp import compiler, dsl
from kfp.dsl import component
from google.oauth2 import service_account

PROJECT_ID = "static-bond-416914"
REGION = "us-central1"
BUCKET_URI = "gs://asgb-vertex-ai-pipelines"
API_ENDPOINT = "{}-aiplatform.googleapis.com".format(REGION)
PIPELINE_ROOT = "{}/pipeline_root/intro".format(BUCKET_URI)
DISPLAY_NAME = "intro_pipeline_job_unique"


# Path to your service account key JSON file
key_path = "/Users/shlok/.ssh/per-gcp-exp-vertex-ai.json"

# Load the credentials from the service account key file
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    # scopes=["https://www.googleapis.com/auth/cloud-platform"],
)


aip.init(credentials=credentials, project=PROJECT_ID, staging_bucket=BUCKET_URI)


@component(base_image="python:3.9")
def hello_world(text: str) -> str:
    print(text)
    return text


@component(base_image="python:3.9", packages_to_install=["google-cloud-storage"])
def two_outputs(
        text: str,
) -> NamedTuple(
    "Outputs",
    [
        ("output_one", str),  # Return parameters
        ("output_two", str),
    ],
):
    # the import is not actually used for this simple example, but the import
    # is successful, as it was included in the `packages_to_install` list.
    from google.cloud import storage  # noqa: F401

    o1 = f"output one from text: {text}"
    o2 = f"output two from text: {text}"
    print("output one: {}; output_two: {}".format(o1, o2))
    return (o1, o2)
# this has written a output file under the pipeline root
# asgb-vertex-ai-pipelines/pipeline_root/intro/737482735608/intro-pipeline-unique-20240407184353/two-outputs_1623121673630777344/executor_output.json
# {
#     "parameterValues": {
#         "output_one": "output one from text: hi there",
#         "output_two": "output two from text: hi there"
#     }
# }

@component()
def consumer(text1: str, text2: str, text3: str) -> str:
    print(f"text1: {text1}; text2: {text2}; text3: {text3}")
    return f"text1: {text1}; text2: {text2}; text3: {text3}"
# this has written a output file under the pipeline root
# asgb-vertex-ai-pipelines/pipeline_root/intro/737482735608/intro-pipeline-unique-20240407184353/consumer_7387729196665012224/executor_output.json
# {
#     "parameterValues": {
#         "Output": "text1: hi there; text2: output one from text: hi there; text3: output two from text: hi there"
#     }
# }
@dsl.pipeline(
    name="intro-pipeline-unique",
    description="A simple intro pipeline",
    pipeline_root=PIPELINE_ROOT,
)
def pipeline(text: str = "hi there"):
    hw_task = hello_world(text=text)
    two_outputs_task = two_outputs(text=text)
    consumer_task = consumer(  # noqa: F841
        text1=hw_task.output,
        text2=two_outputs_task.outputs["output_one"],
        text3=two_outputs_task.outputs["output_two"],
    )


def compile_pipeline():
    compiler.Compiler().compile(pipeline_func=pipeline, package_path="intro_pipeline.yaml")


def get_job():
    return aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="intro_pipeline.yaml",
        pipeline_root=PIPELINE_ROOT,
        credentials=credentials,
        enable_caching=False,           # TODO: Set to True to enable caching
    )


# compile_pipeline()
# get_job().run()
# get_job().delete()


# for j in get_job().list():
#     print(j.resource_name)


pipelines = aip.PipelineJob.list(
    filter=f"display_name={DISPLAY_NAME}", order_by="create_time desc"
)
pipeline = pipelines[0]
print(pipeline.resource_name)

# tried to use my own credentials but it failed with the following error
# raise exceptions.from_grpc_error(exc) from exc google.api_core.exceptions.InvalidArgument: 400 You do not have permission to act as service_account: 737482735608-compute@developer.gserviceaccount.com. (or it may not exist).
# solution is : conolse - my service account - add role - seleve service account -- service account user

# if i rerun the pipeline then it completed in 2 seconds because by default the cache is enabled
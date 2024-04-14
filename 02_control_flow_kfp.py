import json
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

@component
def args_generator_op() -> str:
    import json

    return json.dumps(
        [{"cats": "1", "dogs": "2"}, {"cats": "10", "dogs": "20"}],
        sort_keys=True,
    )


@component
def print_op(msg: str):
    print(msg)


@component
def flip_coin_op() -> str:
    """Flip a coin and output heads or tails randomly."""
    import random

    result = "heads" if random.randint(0, 1) == 0 else "tails"
    return result



@dsl.pipeline(
    name="control",
    pipeline_root=PIPELINE_ROOT,
)
def pipeline(
        json_string: str = json.dumps(
            [
                {
                    "snakes": "anaconda",
                    "lizards": "anole",
                    "bunnies": [{"cottontail": "bugs"}, {"cottontail": "thumper"}],
                },
                {
                    "snakes": "cobra",
                    "lizards": "gecko",
                    "bunnies": [{"cottontail": "roger"}],
                },
                {
                    "snakes": "boa",
                    "lizards": "iguana",
                    "bunnies": [
                        {"cottontail": "fluffy"},
                        {"fuzzy_lop": "petunia", "cottontail": "peter"},
                    ],
                },
            ],
            sort_keys=True,
        )
):

    flip1 = flip_coin_op()

    with dsl.Condition(
            flip1.output != "no-such-result", name="alwaystrue"
    ):  # always true

        args_generator = args_generator_op()
        with dsl.ParallelFor(args_generator.output) as item:
            print_op(msg=json_string)

            with dsl.Condition(flip1.output == "heads", name="heads"):
                print_op(msg=item.cats)

            with dsl.Condition(flip1.output == "tails", name="tails"):
                print_op(msg=item.dogs)

    with dsl.ParallelFor(json_string) as item:
        with dsl.Condition(item.snakes == "boa", name="snakes"):
            print_op(msg=item.snakes)
            print_op(msg=item.lizards)
            print_op(msg=item.bunnies)

    # it is possible to access sub-items
    with dsl.ParallelFor(json_string) as item:
        with dsl.ParallelFor(item.bunnies) as item_bunnies:
            print_op(msg=item_bunnies.cottontail)




def compile_pipeline():
    compiler.Compiler().compile(
        pipeline_func=pipeline, package_path="02_control_flow_kfp.yaml"
    )

def run_pipeline():
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="02_control_flow_kfp.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run()

compile_pipeline()
run_pipeline()
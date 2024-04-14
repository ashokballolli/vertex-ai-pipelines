from typing import List, Any
import logging
import google.cloud.aiplatform as aip
from kfp import compiler, dsl
from kfp.dsl import component
from google.oauth2 import service_account


ENDPOINT_ID = "2488175022447788032"
PROJECT_ID = "737482735608"
REGION = "us-central1"
BUCKET_URI = "gs://asgb-vertex-ai-pipelines"
API_ENDPOINT = "{}-aiplatform.googleapis.com".format(REGION)
PIPELINE_ROOT = "{}/pipeline_root/intro".format(BUCKET_URI)
DISPLAY_NAME = "gbq_pre_process_pred_post_process"


# Path to your service account key JSON file
key_path = "/Users/shlok/.ssh/per-gcp-exp-vertex-ai.json"

# Load the credentials from the service account key file
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    # scopes=["https://www.googleapis.com/auth/cloud-platform"],
)


aip.init(credentials=credentials, project=PROJECT_ID, staging_bucket=BUCKET_URI)



# def predict_custom_trained_model(instances, project_number, endpoint_id):
#     """
#     Uses Vertex AI endpoint to make predictions
#     Args:
#         instances (str): JSON-encoded instances.
#         project_number (str): Google Cloud project number.
#         endpoint_id (str): Vertex AI endpoint ID.
#     Returns:
#         dict: Prediction results
#     """
#     from google.cloud import aiplatform
#     endpoint = aiplatform.Endpoint(
#         endpoint_name=f"projects/{project_number}/locations/us-central1/endpoints/{endpoint_id}"
#     )
#     result = endpoint.predict(instances=instances)
#     return result



@component(base_image="python:3.9")
def read_input_data() -> dict:
    import logging
    # Your preprocessing code here
    input_data = {"data": [1001, 1002]}  # Assume you are querying BigQuery to get this data
    logging.info("********* input_data **********")
    logging.info(input_data)
    return input_data


# Define preprocessing component
@component(base_image="python:3.9")
def preprocess_data(input_data: dict) -> dict:
    import logging
    # Your preprocessing code here
    # assume while pre-processing you found out that for image 1001 there is no image, so filtered out
    # get image to image vector for the remaining
    logging.info(input_data)
    image_data_map = {}
    image_data_map["model"] = "MNIST"
    image_data_map["mandatory-field"] = "dummy"
    image_data_map["image_id"] = 1002
    image_data_map["ser-image"] = [[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01568627543747425, 0.0117647061124444, 0.0, 0.0, 0.027450980618596077, 0.019607843831181526, 0.0, 0.0117647061124444, 0.0, 0.0, 0.0117647061124444, 0.03529411926865578, 0.0235294122248888, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.027450980618596077, 0.0, 0.0, 0.003921568859368563, 0.0, 0.0, 0.0, 0.027450980618596077, 0.0117647061124444, 0.003921568859368563, 0.007843137718737125, 0.007843137718737125, 0.0, 0.0, 0.0, 0.0235294122248888, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.003921568859368563, 0.0235294122248888, 0.0235294122248888, 0.0117647061124444, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0117647061124444, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01568627543747425, 0.0117647061124444, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01568627543747425, 0.0, 0.0, 0.03921568766236305, 0.054901961237192154, 0.0117647061124444, 0.0, 0.007843137718737125, 0.007843137718737125, 0.007843137718737125, 0.003921568859368563, 0.003921568859368563, 0.007843137718737125, 0.0117647061124444, 0.003921568859368563, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.003921568859368563, 0.0117647061124444, 0.0, 0.0, 0.01568627543747425, 0.01568627543747425, 0.0, 0.0, 0.0, 0.0, 0.007843137718737125, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.003921568859368563, 0.0117647061124444, 0.0313725508749485, 0.04313725605607033, 0.0235294122248888, 0.0, 0.0, 0.007843137718737125, 0.0, 0.0, 0.0, 0.0, 0.0117647061124444, 0.0313725508749485, 0.019607843831181526, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3137255012989044, 0.7921568751335144, 0.7411764860153198, 0.21176470816135406, 0.0, 0.01568627543747425, 0.019607843831181526, 0.0, 0.0, 0.04313725605607033, 0.15294118225574493, 0.1921568661928177, 0.0941176488995552, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0117647061124444, 0.0, 0.0, 0.027450980618596077, 0.0117647061124444, 0.0, 0.1411764770746231, 0.9490196108818054, 0.9686274528503418, 0.9921568632125854, 0.47058823704719543, 0.0, 0.0, 0.0, 0.0, 0.01568627543747425, 0.5098039507865906, 1.0, 0.8313725590705872, 0.11764705926179886, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0313725508749485, 0.0, 0.0, 0.0235294122248888, 0.027450980618596077, 0.0, 0.0, 0.0, 0.0117647061124444, 0.7137255072593689, 1.0, 0.95686274766922, 1.0, 0.9098039269447327, 0.3176470696926117, 0.0, 0.07450980693101883, 0.4274509847164154, 0.8901960849761963, 0.9490196108818054, 0.9921568632125854, 0.9529411792755127, 0.0, 0.019607843831181526, 0.0, 0.0, 0.0, 0.0], [0.019607843831181526, 0.0, 0.0, 0.003921568859368563, 0.0, 0.0, 0.0, 0.01568627543747425, 0.29411765933036804, 0.95686274766922, 0.9686274528503418, 0.6352941393852234, 0.5098039507865906, 0.9058823585510254, 1.0, 0.95686274766922, 0.9490196108818054, 0.9882352948188782, 0.9882352948188782, 1.0, 1.0, 0.4274509847164154, 0.0, 0.003921568859368563, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0117647061124444, 0.027450980618596077, 0.0, 0.0, 0.0117647061124444, 0.0, 0.0, 0.5960784554481506, 1.0, 0.95686274766922, 0.16078431904315948, 0.03529411926865578, 0.6392157077789307, 1.0, 0.9411764740943909, 0.7686274647712708, 0.9411764740943909, 1.0, 0.9058823585510254, 0.6392157077789307, 0.07058823853731155, 0.0, 0.01568627543747425, 0.0, 0.0, 0.0, 0.0], [0.003921568859368563, 0.0, 0.0, 0.0, 0.027450980618596077, 0.027450980618596077, 0.0, 0.062745101749897, 0.8470588326454163, 0.929411768913269, 0.6274510025978088, 0.0235294122248888, 0.03529411926865578, 0.01568627543747425, 0.0313725508749485, 0.1568627506494522, 0.12941177189350128, 0.8235294222831726, 1.0, 0.9372549057006836, 0.18039216101169586, 0.0, 0.0117647061124444, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0313725508749485, 0.0, 0.0, 0.007843137718737125, 0.007843137718737125, 0.0, 0.03921568766236305, 0.40784314274787903, 1.0, 0.9921568632125854, 0.3843137323856354, 0.007843137718737125, 0.0, 0.0, 0.01568627543747425, 0.0, 0.5254902243614197, 0.9882352948188782, 0.9019607901573181, 0.6666666865348816, 0.0235294122248888, 0.0, 0.03921568766236305, 0.0, 0.0, 0.0, 0.0, 0.0], [0.019607843831181526, 0.0, 0.0313725508749485, 0.0, 0.0, 0.0, 0.04313725605607033, 0.4470588266849518, 0.772549033164978, 0.4117647111415863, 0.0, 0.027450980618596077, 0.0, 0.0, 0.07058823853731155, 0.2549019753932953, 0.9176470637321472, 1.0, 0.8470588326454163, 0.16078431904315948, 0.0, 0.062745101749897, 0.0, 0.019607843831181526, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0235294122248888, 0.0, 0.03921568766236305, 0.06666667014360428, 0.0, 0.03921568766236305, 0.01568627543747425, 0.0, 0.0, 0.03529411926865578, 0.01568627543747425, 0.0, 0.007843137718737125, 0.7176470756530762, 0.95686274766922, 1.0, 0.29019609093666077, 0.0, 0.0235294122248888, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0313725508749485, 0.0, 0.01568627543747425, 0.0, 0.03921568766236305, 0.3529411852359772, 0.9411764740943909, 0.9843137264251709, 0.6784313917160034, 0.04313725605607033, 0.0, 0.05098039284348488, 0.0, 0.054901961237192154, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0313725508749485, 0.01568627543747425, 0.03529411926865578, 0.007843137718737125, 0.0, 0.21960784494876862, 1.0, 1.0, 0.7568627595901489, 0.07450980693101883, 0.0, 0.0313725508749485, 0.0, 0.0, 0.0, 0.03529411926865578, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.003921568859368563, 0.09019608050584793, 0.6705882549285889, 0.9529411792755127, 0.8901960849761963, 0.4117647111415863, 0.0, 0.003921568859368563, 0.0784313753247261, 0.0, 0.03921568766236305, 0.003921568859368563, 0.01568627543747425, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0235294122248888, 0.0, 0.08627451211214066, 0.04313725605607033, 0.40784314274787903, 1.0, 0.9254902005195618, 0.22745098173618317, 0.03529411926865578, 0.04313725605607033, 0.0, 0.0, 0.0, 0.007843137718737125, 0.019607843831181526, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0117647061124444, 0.019607843831181526, 0.0, 0.33725491166114807, 0.9098039269447327, 0.9843137264251709, 0.6039215922355652, 0.0, 0.0, 0.08627451211214066, 0.0, 0.0, 0.062745101749897, 0.0, 0.0, 0.007843137718737125, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0235294122248888, 0.07450980693101883, 0.7333333492279053, 1.0, 0.6705882549285889, 0.0, 0.09019608050584793, 0.0, 0.01568627543747425, 0.019607843831181526, 0.019607843831181526, 0.01568627543747425, 0.0, 0.01568627543747425, 0.0470588244497776, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.007843137718737125, 0.0941176488995552, 0.7960784435272217, 0.9254902005195618, 0.7686274647712708, 0.3176470696926117, 0.0, 0.0, 0.003921568859368563, 0.0, 0.04313725605607033, 0.0, 0.0, 0.019607843831181526, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5098039507865906, 1.0, 1.0, 0.4117647111415863, 0.03921568766236305, 0.0, 0.019607843831181526, 0.007843137718737125, 0.0, 0.0, 0.007843137718737125, 0.0470588244497776, 0.0, 0.0, 0.019607843831181526, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3294117748737335, 1.0, 0.9411764740943909, 0.7254902124404907, 0.14509804546833038, 0.0117647061124444, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6705882549285889, 1.0, 1.0, 0.32549020648002625, 0.0, 0.0, 0.0, 0.019607843831181526, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.8784313797950745, 0.9372549057006836, 0.9686274528503418, 0.21176470816135406, 0.05098039284348488, 0.0235294122248888, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06666667014360428, 0.04313725605607033, 0.0, 0.0, 0.0, 0.007843137718737125, 0.007843137718737125, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]]
    # preprocessed_data = [image_data_map]
    preprocessed_data = image_data_map
    logging.info("*********** preprocessed_data ************")
    logging.info(preprocessed_data)

    return preprocessed_data

# Define inference component

# Define a function to call the Vertex AI endpoint for prediction
@component(base_image="python:3.9", packages_to_install=["google-cloud-aiplatform"])
def call_vertex_ai_endpoint(project_id: str, location: str, endpoint_id: str, input_data: dict) -> dict:
    import logging
    # Initialize the Vertex AI client
    # client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    # client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # # Prepare the input data for prediction
    # instances = [{"image_bytes": input_data}]  # Assuming input data is an image in bytes format
    # input_data = json_format.ParseDict({"instances": instances}, Value())

    # # Create the endpoint resource name
    # endpoint_name = f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}"
    #
    # # Make the prediction request
    # response = client.predict(endpoint=endpoint_name, instances=input_data)
    #
    import google.cloud.aiplatform as aip
    endpoint = aip.Endpoint(
        endpoint_name=f"projects/{project_id}/locations/us-central1/endpoints/{endpoint_id}"
    )
    response = endpoint.predict(instances=[input_data])

    # Extract and return the predictions
    logging.info("******** predictions ********")
    logging.info(response)
    predictions = response.predictions
    logging.info(predictions)
    return predictions[0]

# Define output writing component
@component(base_image="python:3.9")
def write_output_to_bigquery(endpoint_response: dict):
    import logging
    # Your code to write output to BigQuery
    output_data = endpoint_response  # Placeholder for writing output to BigQuery
    # Write output data to BigQuery table
    logging.info("*********** endpoint_response ***********")
    logging.info(endpoint_response)

# Define pipeline
@dsl.pipeline(
    name="VertexAI_Inference_Pipeline",
    pipeline_root=PIPELINE_ROOT,
)
def vertex_ai_inference_pipeline(): #here this parameter is of no use. Just to show we can pass this value extrnally
    import logging
    input_data_task = read_input_data()
    preprocess_task = preprocess_data(input_data=input_data_task.output)
    inference_task = call_vertex_ai_endpoint(
        project_id=PROJECT_ID,
        location=REGION,
        endpoint_id=ENDPOINT_ID,
        input_data=preprocess_task.output
    )

    write_output_to_bigquery(endpoint_response=inference_task.output)


# Compile pipeline
def compile_pipeline():
    compiler.Compiler().compile(
        pipeline_func=vertex_ai_inference_pipeline, package_path="gbq_pre_process_pred_post_process.yaml"
    )

# Run pipeline
def run_pipeline():
    job = aip.PipelineJob(
        display_name=DISPLAY_NAME,
        template_path="gbq_pre_process_pred_post_process.yaml",
        pipeline_root=PIPELINE_ROOT,
        enable_caching=False,
    )

    job.run()


compile_pipeline()
run_pipeline()
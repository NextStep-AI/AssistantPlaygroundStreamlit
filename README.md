# AssistantPlaygroundStreamlit
Assistant Playground back end with Streamlit front end working chat.

## Set Up and Run

Check if Python is installed on a Windows machine with the following command:

`python -v`

If Python is installed, this command will display the version of Python installed on your system. If it is not installed, you will need to download and install Python from the official website: https://www.python.org/downloads/.

To set up and use a virtual environment in this project, follow these steps:

1. **Create a Virtual Environment:** Open Command Prompt and navigate to your project directory. Then run:

`python -m venv venv`

This will create a virtual environment named `venv` in your project directory.

2. **Activate the Virtual Environment:** To activate the virtual environment, run:

`venv\Scripts\activate`

You should see `(venv)` at the beginning of your command prompt, indicating that the virtual environment is active.

3. **Install Dependencies:** With the virtual environment activated, install the required dependencies using the `requirements.txt` file:

`pip install -r requirements.txt`

4. `sample_env` contains a template for creating your own `.env` file to provide the following variables: 

`AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""`

To obtain the values, go to this link: [Settings - Azure AI Studio](https://ai.azure.com/build/settings/connections?wsid=/subscriptions/702e343d-d816-494d-afe6-5f496dc2cb24/resourceGroups/rg-nextstep/providers/Microsoft.MachineLearningServices/workspaces/Next-step-ai&tid=16b3c013-d300-468d-ac64-7eda0820b6d3) 

The `Azure OpenAI Endpoint` target is: https://aihubnextstep0138686319.openai.azure.com/

The `Azure OpenAI API key` is the first key on the list in the Settings - Azure AI Studio link above.

5. **Run the Streamlit Application:** Now you can run your Streamlit application:

`streamlit run streamlit_demo.py`


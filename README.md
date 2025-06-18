# Insurance AI Agent API

Welcome to the Insurance AI Agent project, powered by [crewAI](https://crewai.com) and served via [FastAPI](https://fastapi.tiangolo.com/). This application provides a robust API for interacting with a multi-agent AI system designed for the insurance industry.

It features two primary crews:
- **Onboarding Crew**: Handles new client insurance quotes and initial inquiries.
- **RAG Crew**: Answers specific policy questions by retrieving information from a knowledge base.

## Initial Project Scaffolding with `crewAI` CLI (For Reference)

These steps outline how the initial `crewAI` project structure can be created. The subsequent sections detail how to set up and run the project in its current FastAPI-based form.

1.  **Create Project Folder:**
    Create a new directory for your project and navigate into it:
    ```bash
    mkdir "Insure AI Agent"
    cd "Insure AI Agent"
    ```

2.  **Scaffold `crewAI` Flow:**
    Use the `crewAI` CLI to create the initial flow structure. This will create a subdirectory named `insure_agent` (or your chosen flow name).
    ```bash
    crewai create flow insure_agent
    ```
    *Navigate into the newly created `insure_agent` directory for the following steps if you ran the above command from the parent "Insure AI Agent" directory.*

3.  **Initialize Virtual Environment with `uv`:**
    It's recommended to use a virtual environment. `uv` can create and manage this.
    ```bash
    uv venv --python 3.12 
    # Or your preferred Python 3.10+ version
    ```

4.  **Activate Virtual Environment:**
    ```bash
    # For Windows:
    .venv\Scripts\activate

    # For macOS/Linux:
    source .venv/bin/activate
    ```

5.  **Install `crewAI` (if not already available globally/as a uv tool):
    If you used `crewai create flow` successfully, `crewai` and its dependencies might already be in your environment if you followed `crewai install` from its template. If starting truly fresh or ensuring `crewai` is installed in the venv:
    ```bash
    uv tool install crewai
    ```

6.  **Add Other Dependencies:**
    Install any additional packages required for your project (like `fastapi`, `uvicorn`, `python-dotenv`, `elasticsearch`, etc.) using `uv`.
    ```bash
    uv pip install fastapi uvicorn python-dotenv "elasticsearch[async]" pydantic sse-starlette
    # Add other packages as needed, e.g., specific langchain components or tools.
    ```

## Setting Up This Project (After Cloning)

If you have cloned this repository (which already includes the FastAPI integration and `crewAI` structure):

1.  **Ensure Python Version:** Make sure you have Python 3.10 - 3.12 installed.

2.  **Navigate to Project Root:** Open your terminal in the root directory of this cloned project (i.e., the `insure_agent` folder).

3.  **Create and Activate Virtual Environment:**
    Refer to steps 3 and 4 in the "Initial Project Scaffolding" section above for guidance on creating a virtual environment (e.g., using `uv venv` or `python -m venv .venv`) and activating it.

4.  **Install Dependencies:**
    With your virtual environment activated, install all project dependencies from the `requirements.txt` file:
    ```bash
pip install -r requirements.txt
    # Or, if using uv:
    # uv pip install -r requirements.txt
    ```
    This command installs FastAPI, Uvicorn, CrewAI, and all other necessary packages.

5.  **Configure Environment:**
    Proceed to the "Environment Configuration" section below to set up your API keys and other necessary variables.

### 3. Environment Configuration

This project requires several environment variables for API keys and service configuration. Create a `.env` file in the project root directory (`insure_agent/.env`) and add the following variables. Wrap all values in double quotes (`""`) to prevent parsing issues.

```env
OPENROUTER_API_KEY="your_openrouter_api_key"
MEM0_API_KEY="your_mem0_api_key"
OPIK_API_KEY="your_opik_api_key"
OPENAI_API_KEY="your_openai_api_key"
VAPI_API_KEY="your_vapi_api_key"
ELASTICSEARCH_CLOUD_ID="your_elasticsearch_cloud_id"
ELASTICSEARCH_API_KEY="your_elasticsearch_api_key"
ELASTICSEARCH_URL="your_elasticsearch_url"
```

### 4. Knowledge Base

Place all your knowledge base documents (e.g., `Car_Insurance_Policy_Documents.pdf`) inside the `insure_agent/src/Knowledge` directory. The application is configured to load documents from this location.

## Running the Application

To start the FastAPI server, navigate to the `src` directory and run the following command:

```bash
cd src
uvicorn insure_agent.main:app --reload --port 80
```

The API will be available at `http://127.0.0.1:80`.

## API Endpoints

The API provides two POST endpoints for interacting with the crews.

### 1. Onboarding Quote Request

- **URL**: `/onboarding/quote`
- **Method**: `POST`
- **Description**: Initiates the Onboarding Crew to process a new insurance quote request.
- **Request Body**:
  ```json
  {
      "client_name": "Emmanuel Eze",
      "initial_request_type": "New Car Insurance Quote",
      "client_query": "I need a new car insurance policy for my 2024 Toyota Camry. I'm looking for full coverage and I have a clean driving record."
  }
  ```

### 2. RAG Policy Query

- **URL**: `/rag/query`
- **Method**: `POST`
- **Description**: Initiates the RAG Crew to answer a specific question about an insurance policy.
- **Request Body**:
  ```json
  {
      "client_query": "What are the benefits of comprehensive coverage?"
  }
  ```

### Testing with Postman

You can use a tool like [Postman](https://www.postman.com/) to test the endpoints. 
1. Set the method to `POST`.
2. Enter the full request URL (e.g., `http://127.0.0.1:80/onboarding/quote`).
3. Go to the `Body` tab, select `raw`, and choose `JSON`.
4. Paste the appropriate JSON request body and send the request.


## Docker

To build the Docker image, run the following command:

```bash
docker build -t insurance-ai-agent .
```

To run the Docker container, run the following command:

```bash
docker run -d -p 8080:80 insurance-ai-agent 
```

The API will be available at `http://127.0.0.1:8080`.


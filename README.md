# 🤖 Insurance AI Agent API - Your Digital Insurance Expert! 🛡️

**Welcome aboard the Insurance AI Revolution!** This isn't your grandfather's insurance system - it's a cutting-edge AI assistant powered by [crewAI](https://crewai.com) and served with [FastAPI](https://fastapi.tiangolo.com/) that's ready to transform how you interact with insurance services!

## ✨ What Makes This Special?

Our system features two AI crews working tirelessly for you:

- **🚀 Onboarding Crew**: Your friendly neighborhood insurance agents who handle new quotes and inquiries with superhuman efficiency.
- **🧠 RAG Crew**: The policy wizards who can answer even your trickiest insurance questions by diving into our knowledge vault.

## 🏗️ Setting Up Your Insurance AI Command Center

> *"Give me six hours to set up an Insurance AI system and I will spend the first four preparing the environment."* - Abraham Lincoln (if he were a developer today)

### 🧪 Starting Fresh? Here's Your Recipe!

1.  **🗂️ Create Your Project HQ:**
    ```bash
    mkdir "Insure AI Agent"
    cd "Insure AI Agent"
    ```

2.  **🔧 Summon the CrewAI Magic:**
    ```bash
    crewai create flow insure_agent
    ```
    *Now navigate into your newly conjured `insure_agent` directory!*

3.  **🔮 Create Your Virtual Sanctuary:**
    ```bash
    uv venv --python 3.12  # Python 3.10+ will also work!
    ```

4.  **🧙‍♂️ Activate Your Powers:**
    ```bash
    # Windows wizards, cast this spell:
    .venv\Scripts\activate

    # Mac/Linux sorcerers, chant this instead:
    source .venv/bin/activate
    ```

5.  **📚 Install the CrewAI Grimoire:**
    ```bash
    uv tool install crewai
    ```

6.  **🛠️ Gather Your Magical Tools:**
    ```bash
    uv pip install fastapi uvicorn python-dotenv "elasticsearch[async]" pydantic sse-starlette
    # Feel free to add more magical ingredients as needed!
    ```

### 🚀 Got the Repo? Let's Launch This Rocket!

1.  **🐍 Python Check**: Make sure you have Python 3.10 - 3.12 (we're not cavemen here!)

2.  **📂 Home Base**: Open your terminal in the `insure_agent` folder (that's mission control!)

3.  **🧪 Create Your Lab**:
    Create a virtual environment like a responsible scientist:
    ```bash
    uv venv --python 3.12  # or python -m venv .venv if you're old school
    ```
    Then activate it! (See step 4 above for the magic words)

4.  **💊 Take Your Dependencies**:
    ```bash
    pip install -r requirements.txt
    # Using UV? That works too:
    # uv pip install -r requirements.txt
    ```

5.  **⚙️ Configure Your Control Panel**:
    Head to the "Secret Sauce Configuration" section below!

### 🔑 Secret Sauce Configuration

Create a `.env` file in your project's root directory and fill it with these magical incantations:

```env
OPENROUTER_API_KEY="your_super_secret_openrouter_key"
MEM0_API_KEY="your_incredible_mem0_key" 
OPIK_API_KEY="your_amazing_opik_key"
OPENAI_API_KEY="your_fantastic_openai_key"
VAPI_API_KEY="your_magnificent_vapi_key"
ELASTICSEARCH_CLOUD_ID="your_stellar_elasticsearch_cloud_id"
ELASTICSEARCH_API_KEY="your_phenomenal_elasticsearch_key"
ELASTICSEARCH_URL="your_spectacular_elasticsearch_url"
```

### 📚 Feed The Knowledge Beast

Drop your insurance policy documents (like `Car_Insurance_Policy_Documents.pdf`) into the `insure_agent/src/Knowledge` directory. Our AI will devour these documents and become wiser!

## 🚀 Blast Off! Running Your Insurance AI

Time to bring your creation to life! Navigate to the `src` directory and unleash the kraken:

```bash
cd src
uvicorn insure_agent.main:app --reload --port 80
```

Your AI command center awaits at `http://127.0.0.1:80`! 

## 🔌 API Endpoints - Your Insurance AI Portals

### 1. 🚗 Get a New Quote
- **Portal**: `/onboarding/quote`
- **Secret Knock**: `POST`
- **Description**: Let our Onboarding Crew prepare a personalized insurance quote!
- **The Magic Words**:
  ```json
  {
      "client_name": "Emmanuel Eze",
      "initial_request_type": "New Car Insurance Quote",
      "client_query": "I need a new car insurance policy for my 2024 Toyota Camry. I'm looking for full coverage and I have a clean driving record."
  }
  ```

### 2. 🧠 Ask the Insurance Oracle
- **Portal**: `/rag/query`
- **Secret Knock**: `POST`
- **Description**: Have a burning insurance question? Our RAG Crew has the answers!
- **The Magic Words**:
  ```json
  {
      "client_query": "What are the benefits of comprehensive coverage?"
  }
  ```

### 🧪 Testing with Postman - Your API Laboratory

[Postman](https://www.postman.com/) is your perfect lab assistant for testing:
1. Set the experiment type to `POST`
2. Target your test tube at `http://127.0.0.1:80/onboarding/quote`
3. Navigate to the `Body` lab station, select `raw`, and choose `JSON`
4. Insert your test sample (JSON from above) and observe the reaction!


### 🐳 Docker - Put It In A Container!

Package this whole experiment in a nice Docker container:

```bash
docker build -t insurance-ai-agent .
```

Release it into the wild:

```bash
docker run -d -p 8080:800 insurance-ai-agent 
```

Visit your containerized creation at `http://127.0.0.1:8080`!

---


### 🚀 Kubernetes - Launch Into The Cloud!

```bash
# Deploy your magical secrets to the Kubernetes cosmos
kubectl create secret generic openai-secret --from-literal=OPENAI_API_KEY=your_openai_api_key
kubectl create secret generic mem0-secret --from-literal=MEM0_API_KEY=your_mem0_api_key
kubectl create secret generic openrouter-secret --from-literal=OPENROUTER_API_KEY=your_openrouter_api_key
``` 

Your insurance AI is now floating in the cloud, ready to serve clients across the galaxy! 🌌


## 🎯 Happy Insuring!

Now you're ready to revolutionize insurance with AI. Questions? Issues? Brilliant ideas? Open an issue or submit a pull request. Let's make insurance exciting again! (Was it ever exciting? Well, it is now!)


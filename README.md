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
    uv pip install fastapi uvicorn python-dotenv pydantic sse-starlette
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
OPENAI_API_KEY="your_fantastic_openai_key"
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


## 🐳 Docker Hub Deployment - Ship Your AI to the World!

### **Prerequisites**
- Docker Desktop installed and running
- Docker Hub account (sign up at [hub.docker.com](https://hub.docker.com))

### **Step 1: Login to Docker Hub**
```bash
# Login to your Docker Hub account
docker login
# Enter your Docker Hub username and password when prompted
```

### **Step 2: Build Your Container**
```bash
# Build the Docker image with version tag
docker build -t emarhnuel/insurance-ai-agent:v3 .

# Build for multiple platforms (recommended for production)
docker buildx build --platform linux/amd64,linux/arm64 -t emarhnuel/insurance-ai-agent:v3 .
```

### **Step 3: Push to Docker Hub**
```bash
# Push your image to Docker Hub
docker push emarhnuel/insurance-ai-agent:v3

# Push with latest tag as well
docker tag emarhnuel/insurance-ai-agent:v3 emarhnuel/insurance-ai-agent:latest
docker push emarhnuel/insurance-ai-agent:latest
```

### **Step 4: Test Your Published Image**
```bash
# Pull and run your published image
docker pull emarhnuel/insurance-ai-agent:v3
docker run -d -p 8080:8000 --name insurance-ai-test emarhnuel/insurance-ai-agent:v3

# Visit http://localhost:8080/docs to test
```

---

## ☸️ Kubernetes Deployment - Launch Into The Cloud!

### **Prerequisites**
- Kubernetes cluster (GKE, EKS, AKS, or local)
- kubectl configured to connect to your cluster
- Your API keys ready

### **Step 1: Create Kubernetes Secrets**
```bash
# Create secrets for your API keys
kubectl create secret generic openai-secret --from-literal=OPENAI_API_KEY=your_actual_openai_api_key
kubectl create secret generic openrouter-secret --from-literal=OPENROUTER_API_KEY=your_actual_openrouter_api_key
kubectl create secret generic mem0-secret --from-literal=MEM0_API_KEY=your_actual_mem0_api_key

# Verify secrets were created
kubectl get secrets
```

### **Step 2: Deploy the Application**
```bash
# Deploy using kubectl
kubectl apply -f deploy.yaml

# Check deployment status
kubectl rollout status deployment/insurance-agent-deployment

# Verify pods are running
kubectl get pods -l app=insurance-agent-pod
```

### **Step 3: Access Your Application**
```bash
# Get the external IP address
kubectl get svc insurance-agent-service

# Check service details
kubectl describe svc insurance-agent-service

# Your API will be available at: http://EXTERNAL-IP/docs
```

### **Step 4: Monitor and Debug**
```bash
# Check pod logs
kubectl logs -l app=insurance-agent-pod --tail=50

# Get detailed pod information
kubectl describe pods -l app=insurance-agent-pod

# Check deployment status
kubectl get deployment insurance-agent-deployment

# Scale your deployment (if needed)
kubectl scale deployment insurance-agent-deployment --replicas=3
```

### **Step 5: Update Your Deployment**
```bash
# After pushing a new image version to Docker Hub
kubectl set image deployment/insurance-agent-deployment insurance-agent=emarhnuel/insurance-ai-agent:v4

# Or edit the deployment directly
kubectl edit deployment insurance-agent-deployment

# Check rollout status
kubectl rollout status deployment/insurance-agent-deployment
```

### **Useful kubectl Commands**
```bash
# Delete deployment (if needed)
kubectl delete deployment insurance-agent-deployment

# Delete service (if needed)
kubectl delete svc insurance-agent-service

# Delete secrets (if needed)
kubectl delete secret openai-secret openrouter-secret mem0-secret

# View all resources
kubectl get all

# Get events (for troubleshooting)
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## 🔄 Automated Deployment with GitHub Actions

Your repository includes automated CI/CD! Every push to the `main` branch will:

1. **Build** your Docker image
2. **Push** to Google Container Registry
3. **Deploy** to your Kubernetes cluster automatically

### **Setup GitHub Actions (One-time setup)**
1. Add these secrets to your GitHub repository settings:
   - `GKE_PROJECT`: Your Google Cloud project ID
   - `GKE_SA_KEY`: Your service account JSON key
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `MEM0_API_KEY`: Your Mem0 API key

2. Update the cluster details in `.github/workflows/actions.yaml`:
   ```yaml
   env:
     GKE_CLUSTER: your-cluster-name
     GKE_ZONE: your-cluster-zone
   ```

3. Push your code and watch the magic happen! ✨

---

## 🎯 Production Tips

### **Docker Best Practices**
- Always use specific version tags (avoid `latest` in production)
- Use multi-stage builds for smaller images
- Scan images for vulnerabilities: `docker scout cves emarhnuel/insurance-ai-agent:v3`

### **Kubernetes Best Practices**
- Set resource limits and requests (already configured)
- Use health checks (already configured)
- Monitor your application logs regularly
- Keep your secrets secure and rotate them periodically

### **Monitoring Your Deployment**
```bash
# Watch pods in real-time
kubectl get pods -l app=insurance-agent-pod -w

# Stream logs
kubectl logs -f -l app=insurance-agent-pod

# Check resource usage
kubectl top pods -l app=insurance-agent-pod
```

Your insurance AI is now floating in the cloud, ready to serve clients across the galaxy! 🌌


## 🎯 Happy Insuring!

Now you're ready to revolutionize insurance with AI. Questions? Issues? Brilliant ideas? Open an issue or submit a pull request. Let's make insurance exciting again! (Was it ever exciting? Well, it is now!)


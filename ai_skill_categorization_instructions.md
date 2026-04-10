# AI Skill Categorization Instructions

## Overview

Each of the 464 Lightcast AI skills receives exactly **one primary category** (mutually exclusive) and **one or more cross-cutting tags** (non-exclusive). The primary category answers "what domain does this skill fundamentally belong to?" while tags capture secondary dimensions that cut across categories.

## Primary Categories (mutually exclusive)

### 1. Machine Learning & Predictive AI

The skill is primarily about **building, training, evaluating, or deploying predictive/analytical AI models**, or it is a **framework, algorithm, or infrastructure component** used in that process.

Includes:
- ML algorithms (XGBoost, SVM, Random Forest, K-Means, Bayesian networks)
- Deep learning architectures and frameworks (PyTorch, TensorFlow, Keras, CNNs, RNNs, transformers as architecture)
- Model training concepts (feature engineering, hyperparameter tuning, transfer learning, supervised/unsupervised learning)
- ML infrastructure and operations (MLOps, MLflow, SageMaker, Kubeflow, model monitoring)
- Computer vision models and tools (OpenCV, YOLO, object detection, image classification)
- Reinforcement learning
- General AI concepts (artificial intelligence, expert systems, knowledge representation)
- AI platforms used primarily for model building (Vertex AI, Azure ML, H2O.ai)
- Data processing for ML (feature extraction, dimensionality reduction, data classification)

Decision rule: if the skill is about **how models are built or how predictions are made**, it belongs here.

### 2. Generative AI

The skill is primarily about **generating content, understanding/producing natural language, or orchestrating LLM-based applications**.

Includes:
- Large language models and their ecosystem (GPT, LLaMA, BERT, Hugging Face, LangChain)
- Prompt engineering and context engineering
- Content generation (text, image, audio, code generation)
- Generative architectures (GANs, VAEs, diffusion models, DALL-E, Stable Diffusion)
- NLP tasks and tools (sentiment analysis, NER, text mining, machine translation, OCR, speech recognition)
- Conversational AI and chatbots (ChatGPT, Copilot, Alexa, conversational AI platforms)
- AI agents and agentic frameworks (CrewAI, LangGraph, AgentGPT, multi-agent systems)
- Retrieval-augmented generation (RAG)
- Vector databases used in LLM retrieval (PineCone, Qdrant, Weaviate)

Decision rule: if the skill is about **generating output, processing language, or orchestrating LLM-powered workflows**, it belongs here.

### 3. Robotics & Autonomous Systems

The skill is primarily about **physical automation, robotic systems, autonomous vehicles, or cyber-physical control**.

Includes:
- Industrial and advanced robotics (robotic programming, robotic systems, robot operating systems)
- Autonomous vehicles and driving (ADAS, SLAM, path planning, autonomous navigation)
- Automation systems (automation systems design, building automation, process automation hardware)
- Motion planning and control (servomotors, motion planning, dynamic routing)
- Sensor and perception for physical systems (LiDAR, remote sensing, thermal imaging for robotics)
- Simulation environments for robotics (NVIDIA Isaac SDK, OpenAI Gym Environments for robotics)
- Drones and unmanned systems (UAS)

Decision rule: if the skill is about **controlling physical systems or enabling autonomous operation in the real world**, it belongs here.

### 4. AI Governance, Risk & Strategy

The skill is primarily about **managing the responsible adoption, regulation, risk, or organizational strategy of AI**.

Includes:
- AI ethics and responsible AI (AI bias, AI alignment, AI safety, ethical AI, explainable AI)
- AI governance and compliance (AI-based legal compliance, data sovereignty, AI risk)
- AI strategy and adoption (AI strategy, AI product strategy, AI literacy, AI innovation as organizational capability)
- AI certifications focused on governance/policy (AI+ certifications)
- AI security

Decision rule: if the skill is about **how AI should be governed, regulated, adopted safely, or strategically managed**, it belongs here.

## Boundary Rules for Ambiguous Skills

1. **Explainable AI (XAI)**: → AI Governance (it's about making AI interpretable for stakeholders, not about model building)
2. **Synthetic Data Generation**: → Machine Learning & AI (it's a technique for model training)
3. **Vector databases** (PineCone, Qdrant, Weaviate): → Generative AI (they're primarily used in RAG/LLM retrieval pipelines now)
4. **Reinforcement Learning from Human Feedback (RLHF)**: → Generative AI (it's about LLM alignment)
5. **OpenAI Gym**: → Machine Learning & AI (it's an RL research environment)
6. **OpenAI Gym Environments**: → Robotics (when specifically about robotic simulation)
7. **Cognitive Computing / Cognitive Automation**: → Machine Learning & AI (legacy IBM concept, closer to classic AI)
8. **Bot Framework / Botpress**: → Generative AI (chatbot platforms)
9. **Building Automation Software**: → Robotics (physical building systems)
10. **Embedded AI / Edge Intelligence**: → Machine Learning & AI (deployment concern for models, not robotics-specific)
11. **AI Testing**: → Machine Learning & AI (model quality assurance)
12. **AIOps**: → Machine Learning & AI (operational AI for IT, not governance)
13. **Data Version Control (DVC)**: → Machine Learning & AI (ML pipeline tooling)
14. **Operationalizing AI**: → Machine Learning & AI (MLOps-adjacent)
15. **Swarm Intelligence**: → Machine Learning & AI (optimization algorithm family)
16. **Cyber-Physical Systems**: → Robotics & Autonomous Systems
17. **Game AI**: → Machine Learning & AI (game engine AI techniques)

## Cross-Cutting Tags

Each skill receives one or more tags from the following list. A skill must receive **at least one tag**. Tags are assigned based on what the skill **involves or is used for**, regardless of its primary category.

### Tag Definitions

| Tag | Description | Minimum qualifying criteria |
|-----|-------------|---------------------------|
| `Deep Learning` | Uses or relates to neural network architectures (CNNs, RNNs, transformers, autoencoders) | The skill explicitly involves deep neural networks |
| `NLP` | Involves processing, understanding, or generating human language | The skill works with text, speech, or language data |
| `Computer Vision` | Involves processing, analyzing, or generating visual data | The skill works with images, video, or 3D data |
| `AI Agents & Assistants` | Involves autonomous AI agents, copilots, virtual assistants, or agentic orchestration | The skill is about agent behavior, tool use, or assistant interaction |
| `Automation & Control` | Involves automating physical or digital processes, control systems | The skill automates workflows, industrial processes, or system control |
| `MLOps & Deployment` | Involves operationalizing, serving, monitoring, or managing ML models in production | The skill is about the ML production lifecycle |
| `Ethics & Responsible AI` | Involves ethics, risk, compliance, safety, or responsible adoption of AI | The skill addresses how AI is governed or regulated |
| `AI Platforms & Tools` | The skill is a specific vendor platform, cloud service, or commercial AI tool | The skill is a named product or service (AWS, Azure, Google, etc.) |

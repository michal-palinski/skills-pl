"""
Categorize all 464 Lightcast AI skills into 4 primary categories + cross-cutting tags.

Primary categories (mutually exclusive):
  1. Machine Learning & AI
  2. Generative AI & Language Technologies
  3. Robotics & Autonomous Systems
  4. AI Governance, Risk & Strategy

Tags (non-exclusive):
  Deep Learning, NLP & Language, Computer Vision, AI Agents & Assistants,
  Automation & Control, MLOps & Deployment, AI Governance, AI Platforms & Tools
"""

import pandas as pd
from pathlib import Path

XLSX = Path(__file__).parent / "ai_skills_2026_lightcast_scraped.xlsx"
OUT = Path(__file__).parent / "ai_skills_2026_lightcast_scraped.xlsx"

CAT_ML   = "Machine Learning & Predictive AI"
CAT_GEN  = "Generative AI"
CAT_ROB  = "Robotics & Autonomous Systems"
CAT_GOV  = "AI Governance, Risk & Strategy"

# ── Base cluster → primary category mapping ──────────────────────────────────
CLUSTER_TO_PRIMARY = {
    "Machine Learning":                     CAT_ML,
    "Neural Networks":                      CAT_ML,
    "Visual Image Recognition":             CAT_ML,
    "Artificial Intelligence":              CAT_ML,
    "Natural Language Processing":          CAT_GEN,
    "AI Agent":                             CAT_GEN,
    "Generative AI":                        CAT_GEN,
    "Robotics":                             CAT_ROB,
    "Autonomous Driving":                   CAT_ROB,
    "AI Ethics, Governance and Regulations": CAT_GOV,
}

# ── Per-skill overrides (boundary cases) ─────────────────────────────────────
OVERRIDES = {
    # Cluster "Artificial Intelligence" → move to Generative AI
    "PineCone":                            CAT_GEN,
    "Qdrant":                              CAT_GEN,
    "Weaviate":                            CAT_GEN,
    "Watson Conversation":                 CAT_GEN,
    "Artificial Intelligence Markup Language (AIML)": CAT_GEN,

    # Cluster "Machine Learning" → move to Generative AI
    "Transformer (Machine Learning Model)": CAT_GEN,
    "AutoGen":                             CAT_GEN,

    # Cluster "Machine Learning" → move to Robotics
    "Cyber-Physical Systems":              CAT_ROB,

    # Cluster "Neural Networks" → move to Generative AI
    "Sequence-to-Sequence Models (Seq2Seq)": CAT_GEN,

    # Cluster "AI Agent" → stays in Generative AI (already mapped)

    # Cluster "Robotics" → some were already correct
    "Reinforcement Learning from Human Feedback (RLHF)": CAT_GEN,
    "Meta-Reinforcement Learning":         CAT_ML,

    # Cluster "AI Ethics" → some are really ML
    "Explainable Artificial Intelligence (XAI)": CAT_GOV,
    "Explainable AI (XAI)":                CAT_GOV,
    "AI+ Cloud Certification":             CAT_GOV,
    "AI+ Developer Certification":         CAT_GOV,
    "AI+ Foundations Certification":        CAT_GOV,
    "AI+ Security Level1 Certification":   CAT_GOV,

    # Move some "Artificial Intelligence" catch-all skills
    "Bonsai":                              CAT_ML,
    "Azure AI Studio":                     CAT_ML,
    "AWS AI Tools":                        CAT_ML,
    "AWS Bedrock":                         CAT_GEN,
    "Azure OpenAI":                        CAT_GEN,
    "Azure Cognitive Services":            CAT_ML,
    "AI in Diagnostics":                   CAT_ML,
    "AI in EHR Systems":                   CAT_ML,
    "AI in Patient Services":              CAT_GEN,
    "AI-Driven Treatment Planning Algorithm": CAT_ML,
    "AI-Powered Professional Development": CAT_GEN,
    "Architecture Decision Records":       CAT_GOV,

    # Cluster "Generative AI" edge cases
    "Variational Autoencoders":            CAT_ML,
    "Variational Autoencoders (VAEs)":     CAT_ML,

    # NLP cluster edge cases
    "Nearest Neighbour Algorithm":         CAT_ML,

    # Autonomous Driving edge cases
    "OpenCV":                              CAT_ML,

    # "Artificial Intelligence" catch-all → governance
    "Artificial Intelligence Strategy":    CAT_GOV,
    "AI Product Strategy":                 CAT_GOV,
    "AI Innovation":                       CAT_GOV,

    # Move to robotics
    "Automated Planning And Scheduling":   CAT_ROB,
    "Automation Systems":                  CAT_ROB,
    "Automation Systems Design":           CAT_ROB,
    "Building Automation Software":        CAT_ROB,
    "Systems Automation":                  CAT_ROB,
    "Markov Decision Process (Optimal Decisions)": CAT_ROB,

    # Swarm Intelligence is algorithmic
    "Swarm Intelligence":                  CAT_ML,

    # Game AI is ML
    "Game Artificial Intelligence":        CAT_ML,
    "Game Ai":                             CAT_ML,

    # Fuzzy Logic is classical AI
    "Fuzzy Logic":                         CAT_ML,
}

# ── Tag assignment rules ─────────────────────────────────────────────────────

DL_KEYWORDS = {
    "neural network", "deep learning", "cnn", "rnn", "convolutional",
    "recurrent", "transformer", "autoencoder", "backpropagation",
    "resnet", "lstm", "gru", "attention mechanism", "spiking neural",
    "boltzmann", "perceptron", "deeplearning4j", "tensorflow", "pytorch",
    "keras", "caffe", "mxnet", "theano", "chainer", "pybrain", "cudnn",
    "paddlepaddle", "singa", "skflow", "openvinо", "openvino",
    "sequence-to-sequence", "seq2seq", "gan", "generative adversarial",
    "diffusion", "variational autoencoder", "vae", "deep reinforcement",
    "neuro-symbolic", "neural architecture", "neural ordinary",
    "evolutionary acquisition of neural", "model architecture",
}

NLP_KEYWORDS = {
    "natural language", "nlp", "text mining", "sentiment", "tokenization",
    "word embedding", "word2vec", "bert", "speech recognition", "speech synthesis",
    "text-to-speech", "tts", "machine translation", "summarization",
    "computational linguistics", "dialog", "semantic analysis", "semantic parsing",
    "semantic search", "semantic kernel", "named entity", "ner",
    "language model", "language understanding", "language generation",
    "fasttext", "hugging face", "spacy", "gensim", "antlr", "opennlp",
    "ocr", "optical character", "screen reader", "text retrieval",
    "shogun", "nuance", "voice", "conversational", "chatbot", "chat",
    "llm", "gpt", "copilot", "prompt", "langchain", "langgraph",
    "deepseek", "claude", "gemini", "llama", "amazon textract",
    "whisper", "deepspeech", "s voice", "alexa", "cortana", "siri",
    "ai transcription", "ai translation", "ai copywriting",
    "retrieval augmented", "rag", "small language model",
    "statistical language", "sentence transformer",
}

CV_KEYWORDS = {
    "computer vision", "image", "visual", "object recognition", "object detection",
    "object tracking", "face detection", "face recognition", "pose estimation",
    "3d reconstruction", "scene understanding", "motion analysis", "machine vision",
    "yolo", "opencv", "realsense", "mnist", "digital image", "thermal imaging",
    "lidar", "activity recognition", "contextual image", "deck.gl",
    "stable diffusion", "dall-e", "omnipage", "digital twin",
    "aforge",
}

AGENT_KEYWORDS = {
    "agent", "chatbot", "copilot", "assistant", "virtual assistant",
    "alexa", "cortana", "siri", "conversational ai", "bot framework",
    "botpress", "dialogflow", "rasa", "wit.ai", "nuance nina",
    "amelia", "agentgpt", "crewai", "autogen", "embedded ai",
    "autonomic computing", "multi-agent", "tool calling", "agentic",
    "deepseek", "claude ai", "cursor ai", "microsoft delve",
    "customer engagement suite", "azure openai", "custom gpt",
    "agent orchestration", "ai agent monitoring", "ai agent observability",
    "swarm intelligence",
}

AUTOMATION_KEYWORDS = {
    "automation", "robotic", "robot", "autonomous", "self-driving",
    "adas", "slam", "motion planning", "path planning", "path finding",
    "dynamic routing", "drone", "uas", "unmanned", "servomotor",
    "cyber-physical", "building automation", "systems automation",
    "cognitive robotics", "nvidia jetson", "nvidia isaac",
    "automated planning", "process automation",
}

MLOPS_KEYWORDS = {
    "mlops", "modelops", "mlflow", "kubeflow", "sagemaker", "vertex ai",
    "azure machine learning", "data version control", "dvc",
    "operationalizing", "ml inference", "model monitoring",
    "scalable machine learning infrastructure", "streaming machine learning",
    "feature store", "model serving", "model deployment",
    "machine learning strategy", "applied machine learning",
    "distributed machine learning", "predictionio",
    "oracle autonomous database", "pycaret",
    "aws certified machine learning",
    "sas certified modelops",
}

ETHICS_KEYWORDS = {
    "ethics", "ethical", "bias", "safety", "alignment", "responsible",
    "governance", "compliance", "regulation", "risk", "explainable",
    "xai", "literacy", "strategy", "certification", "data sovereignty",
    "ai security", "ai failure", "best practices", "ai innovation",
    "ai product strategy", "ai testing",
}

PLATFORM_KEYWORDS = {
    "aws", "azure", "google", "vertex", "sagemaker", "bedrock",
    "watson", "cognitive services", "oracle", "tensorflow", "pytorch",
    "keras", "caffe", "h2o", "databricks", "openai", "hugging face",
    "lightgbm", "xgboost", "scikit", "weka", "mahout", "spark",
    "dask", "mlflow", "kubeflow", "nvidia", "intel openvino",
    "microsoft copilot", "microsoft delve", "cortana", "alexa",
    "chatgpt", "deepseek", "claude", "cursor ai", "beautiful.ai",
    "adobe sensei", "baidu", "amelia", "botpress", "rasa",
    "dialogflow", "wit.ai", "nuance", "agentgpt", "crewai",
    "stable diffusion", "dall-e", "pycaret", "paddlepaddle",
    "pennylane", "qdrant", "pinecone", "weaviate", "langchain",
    "langgraph", "amazon", "maas",
}


def assign_tags(skill_name: str, description: str) -> list[str]:
    """Return list of tags for a skill based on its name and description."""
    text = f"{skill_name} {description}".lower()
    tags = []

    def _match(keywords):
        return any(kw in text for kw in keywords)

    if _match(DL_KEYWORDS):
        tags.append("Deep Learning")
    if _match(NLP_KEYWORDS):
        tags.append("NLP")
    if _match(CV_KEYWORDS):
        tags.append("Computer Vision")
    if _match(AGENT_KEYWORDS):
        tags.append("AI Agents & Assistants")
    if _match(AUTOMATION_KEYWORDS):
        tags.append("Automation & Control")
    if _match(MLOPS_KEYWORDS):
        tags.append("MLOps & Deployment")
    if _match(ETHICS_KEYWORDS):
        tags.append("Ethics & Responsible AI")
    if _match(PLATFORM_KEYWORDS):
        tags.append("AI Platforms & Tools")

    if not tags:
        tags.append("General AI")

    return tags


def categorize_all(df: pd.DataFrame) -> pd.DataFrame:
    """Add primary_category and tags columns."""
    categories = []
    all_tags = []

    for _, row in df.iterrows():
        name = str(row.get("lightcast_name", ""))
        cluster = str(row.get("excel_ai_skill_cluster", ""))
        desc = str(row.get("lightcast_description", ""))

        if name in OVERRIDES:
            cat = OVERRIDES[name]
        else:
            cat = CLUSTER_TO_PRIMARY.get(cluster, CAT_ML)

        tags = assign_tags(name, desc)
        categories.append(cat)
        all_tags.append("; ".join(tags))

    df = df.copy()
    df["primary_category"] = categories
    df["tags"] = all_tags
    return df


def main():
    df = pd.read_excel(XLSX, sheet_name="all_skills")
    valid = df[df["retrieve_status"] == "ok"].copy()
    invalid = df[df["retrieve_status"] != "ok"].copy()

    print(f"Total skills: {len(df)}, valid: {len(valid)}, invalid: {len(invalid)}")

    valid = categorize_all(valid)

    print("\n── Primary Category Counts ──")
    for cat, count in valid["primary_category"].value_counts().items():
        print(f"  {cat}: {count}")

    print("\n── Tag Counts ──")
    tag_counts = {}
    for tags_str in valid["tags"]:
        for tag in tags_str.split("; "):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        print(f"  {tag}: {count}")

    print("\n── Spot-check: 20 random skills ──")
    sample = valid.sample(20, random_state=42)
    for _, r in sample.iterrows():
        print(f"  {r['lightcast_name']:50s} → {r['primary_category']:40s} | {r['tags']}")

    print("\n── All categorized skills ──")
    for cat in [CAT_ML, CAT_GEN, CAT_ROB, CAT_GOV]:
        subset = valid[valid["primary_category"] == cat].sort_values("lightcast_name")
        print(f"\n  === {cat} ({len(subset)}) ===")
        for _, r in subset.iterrows():
            print(f"    {r['lightcast_name']:55s} | {r['tags']}")

    result = pd.concat([valid, invalid], ignore_index=True)
    with pd.ExcelWriter(OUT, engine="openpyxl") as writer:
        result.to_excel(writer, sheet_name="all_skills", index=False)
    print(f"\nSaved to {OUT}")


if __name__ == "__main__":
    main()

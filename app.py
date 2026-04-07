from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# ---------------- IMAGE GENERATION ---------------- #
import base64
import json
import time
import os
import requests

def generate_image(prompt):
    if not STABILITY_API_KEY:
        print("❌ API key missing")
        return None

    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "clip_guidance_preset": "FAST_BLUE",
        "height": 512,
        "width": 512,
        "samples": 1
    }

    try:
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps(payload)
        )

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("❌ Error:", response.text)
            return None

        result = response.json()
        image_base64 = result["artifacts"][0]["base64"]
        image_data = base64.b64decode(image_base64)

        os.makedirs("static", exist_ok=True)
        filename = f"gen_{int(time.time())}.png"
        path = os.path.join("static", filename).replace("\\", "/")

        with open(path, "wb") as f:
            f.write(image_data)

        print("✅ Image saved:", path)
        return f"/{path}"

    except Exception as e:
        print("❌ Exception:", e)
        return None


# ---------------- RESPONSE FORMAT ---------------- #
def format_response(content, mode):
    if mode == "one":
        return content["one"]
    elif mode == "points":
        return "\n".join([f"• {p}" for p in content["points"]])
    elif mode == "brief":
        return content["brief"] + "\n\n" + "\n".join([f"• {p}" for p in content["points"]])
    else:
        return content["definition"]


# ---------------- KNOWLEDGE BASE ---------------- #
ml_data = {

    "machine learning": {
        "one": "Machine Learning allows computers to learn from data.",
        "definition": "Machine Learning is a branch of AI where systems learn from data and improve without explicit programming.",
        "points": ["Learns from data", "Improves automatically", "Used in AI"],
        "brief": "Machine Learning is a field of AI where systems learn patterns from data."
    },

    "types of machine learning": {
        "one": "Supervised, Unsupervised, Reinforcement.",
        "definition": "Machine Learning has three types: supervised, unsupervised, and reinforcement learning.",
        "points": [
            "Supervised – labeled data",
            "Unsupervised – pattern finding",
            "Reinforcement – reward-based"
        ],
        "brief": "Machine learning is divided into three main types based on learning style."
    },

    "data transformation": {
        "one": "Data transformation converts data into usable format.",
        "definition": "Data transformation converts raw data into structured format for ML models.",
        "points": ["Normalization", "Scaling", "Encoding", "Standardization"],
        "brief": "Data transformation prepares raw data for better model performance."
    },

    "classification": {
        "one": "Classification predicts categories.",
        "definition": "Classification is a supervised learning method used to predict labels.",
        "points": ["Uses labeled data", "Predicts categories", "Spam detection"],
        "brief": "Classification assigns input data into categories."
    },

    "k means": {
        "one": "K-Means groups data into clusters.",
        "definition": "K-Means is an algorithm that divides data into K clusters.",
        "points": ["Centroids", "Grouping", "Iterative"],
        "brief": "K-Means clustering groups similar data points."
    },

    "decision tree": {
        "one": "Decision tree is a flowchart model.",
        "definition": "Decision tree is a supervised model used for classification.",
        "points": ["Tree structure", "Splitting", "Easy"],
        "brief": "Decision trees make decisions using a tree-like model."
    },

    "svm": {
        "one": "SVM separates data using hyperplane.",
        "definition": "SVM finds the best boundary between classes.",
        "points": ["Hyperplane", "Margin", "High dimension"],
        "brief": "SVM is used for classification by separating data."
    },

    "logistic regression": {
        "one": "Predicts probability.",
        "definition": "Logistic regression is used for binary classification.",
        "points": ["Sigmoid", "Probability", "Classification"],
        "brief": "Logistic regression predicts categorical outcomes."
    },

    "neural network": {
        "one": "Mimics human brain.",
        "definition": "Neural networks are deep learning models inspired by brain.",
        "points": ["Input layer", "Hidden layers", "Output"],
        "brief": "Neural networks are used for complex pattern learning."
    }
}


# ---------------- ALIASES ---------------- #
aliases = {
    "ml": "machine learning",
    "types of ml": "types of machine learning",
    "kmeans": "k means"
}


# ---------------- SMART MATCH ---------------- #
def find_best_match(user_message):
    for alias in aliases:
        if alias in user_message:
            user_message += " " + aliases[alias]

    best_match = None
    max_score = 0

    user_words = set(user_message.split())

    for key in ml_data:
        key_words = set(key.split())
        score = len(user_words & key_words)

        if score > max_score:
            max_score = score
            best_match = key

    return best_match


# ---------------- ROUTES ---------------- #
@app.route("/Laalithya")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json["message"].lower()
    image = None

    print("User asked:", user_message)

    # -------- MODE -------- #
    mode = "definition"
    if "1 line" in user_message:
        mode = "one"
    elif "points" in user_message:
        mode = "points"
    elif "brief" in user_message:
        mode = "brief"

    # -------- IMAGE -------- #
    if any(word in user_message for word in ["diagram", "image", "flowchart", "generate", "show", "draw"]):
        print("📸 Image request detected")

        image = generate_image(f"{user_message}, clean educational diagram, white background")

        if image:
            return jsonify({"reply": "Here is your diagram:", "image": image})
        else:
            return jsonify({"reply": "❌ Image generation failed. Check API key.", "image": None})

    # -------- TEXT -------- #
    match = find_best_match(user_message)

    if match:
        reply = format_response(ml_data[match], mode)
        return jsonify({"reply": reply, "image": image})

    return jsonify({
        "reply": "I am ML Buddy 🤖 Ask me ML topics or diagrams!",
        "image": image
    })


# ---------------- AUTO OPEN ---------------- #
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/Laalithya")


if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
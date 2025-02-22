import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from flask import Flask, request, jsonify
from huggingface_hub import login
import nltk
from nltk.tokenize import word_tokenize
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read token from environment variable
hf_token = os.getenv("HUGGINGFACE_TOKEN")
print(hf_token)
if hf_token is None:
    raise ValueError("Hugging Face token not found. Please set it in a .env file.")

# Authenticate with Hugging Face
login(hf_token)

# Get FAQ Data
with open("faq_data.json", "r", encoding="utf-8") as file:
    faq_data = json.load(file)


# Ensure word tokenizer is available
nltk.download('punkt_tab')



# Load sentence embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load text generation model
llm_pipeline = pipeline("text-generation", model='h2oai/h2o-danube3-500m-chat')


# Embed FAQ Questions
faq_questions = list(faq_data.keys())
faq_embeddings = embedding_model.encode(faq_questions)

# Build FAISS index for similarity search
dimension = faq_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(faq_embeddings))

# List of greetings
greetings = [
    "hello", "hi", "hey", "howdy", "hiya", "yo", "sup", "what's up",
    "good morning", "good afternoon", "good evening", "good night",
    "greetings", "salutations", "how are you", "how's it going",
    "bonjour", "hola", "namaste", "salaam", "shalom", "ciao",
    "konnichiwa", "annyeong", "ni hao", "vanakkam", "marhaba"
]

# Create Flask app
app = Flask(__name__)

@app.route("/chat", methods=['POST'])
def chat():
    user_query = request.json.get("query").strip()
    tokens = word_tokenize(user_query.lower())
    for token in tokens:
        if token in greetings:
            return jsonify({"response": f"{token.capitalize()}! How can I assist you today?"})
    # Encode user query
    query_embedding = np.array(embedding_model.encode([user_query]))
    distances, closest_index = index.search(query_embedding, k=1)
    
    confidence = 1 / (1 + distances[0][0])  # Convert distance to confidence score
    
    if confidence < 0.5:
        return jsonify({"response": "I'm sorry, but I cannot answer that question."})
    else:
        closest_question = faq_questions[closest_index[0][0]]
        retrieved_answer = faq_data[closest_question]
        llm_response = llm_pipeline(f"Given the user's query and the FAQ response, provide a concise answer. If the FAQ response is already consise return it\n\nUser: {user_query}\nFAQ Response: {retrieved_answer}\nFinal Answer:", max_length=100, do_sample=False)
        bot_response_text = llm_response[0]["generated_text"].strip()
    
    return jsonify({"response": bot_response_text})

if __name__ == "__main__":
    app.run(debug=False)

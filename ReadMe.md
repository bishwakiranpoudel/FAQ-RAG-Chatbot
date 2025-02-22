# FAQ Chatbot

This repository contains a chatbot that can handle greetings and answer frequently asked questions (FAQs) made for assesment round of AI Intern Application at Danson Solutions. It is built using Flask for the backend API and Streamlit for the frontend. The chatbot utilizes FAISS for efficient similarity search and SentenceTransformers for embedding generation. Additionally, an LLM-based pipeline is used for generating responses.

---

## Features

- Handles common greetings.
- Searches for the most relevant FAQ entry using FAISS.
- Uses SentenceTransformers for semantic search.
- Enhances responses using an LLM pipeline.
- Frontend built with Streamlit for a user-friendly interface.
- Flask API to handle chatbot requests.

---

## Setup Instructions

### 1. Clone the Repository or Acess the .zip file

```sh
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies

All required dependencies are listed in `requirements.txt`. Install them using:

```sh
pip install -r requirements.txt
```

### 3. Set up Environment Variables

Create a `.env` file and add your Hugging Face token. I have provided my personal token valid till the evaluation process are complete:

```
HUGGINGFACE_TOKEN=your_huggingface_api_token
```

### 4. Provide FAQ Data

Ensure `faq_data.json` exists in the root directory with your FAQ dataset in JSON format the faq data provided is a collection of scrapped data from Dason Solutions official website:

```json
{
  "What is your refund policy?": "We offer a 30-day refund policy for all products.",
  "How can I contact support?": "You can reach support via email at support@example.com."
}
```

### 5. Run the Chatbot API

Start the Flask API:

```sh
python chatbot.py
```

### 6. Run the Frontend

Start the Streamlit UI:

```sh
streamlit run app.py
```

---

## Usage

1. Open the Streamlit interface in your browser.
2. Enter a question in the input field.
3. The chatbot will respond with the most relevant FAQ entry.
4. If no relevant FAQ is found, the chatbot will generate a response using the LLM pipeline.

---

## Project Structure

```
📂 project-root
 ├── chatbot.py            # Flask API backend
 ├── app.py                # Streamlit frontend
 ├── faq_data.json         # FAQ dataset
 ├── requirements.txt      # Python dependencies
 ├── .env                  # Hugging Face token
 ├── README.md             # Documentation (this file)
 ├── video_demo.mp4        # Video demo of the project
 ├── report.pdf            # Report detailing project implementation
```

---

## Assessment Details

This project was developed as part of an AI Intern assessment at Danson Solutions. The requirements were:

- Develop a chatbot that can handle greetings and FAQs.
- Use any framework (Flask, Streamlit, Django, etc.).
- Optionally integrate NLP libraries like NLTK or spaCy.

---

## Dependencies

- `faiss-cpu`
- `numpy`
- `sentence-transformers`
- `transformers`
- `flask`
- `huggingface_hub`
- `streamlit`
- `requests`
- `nltk`
- `python-dotenv`

All dependencies are listed in `requirements.txt`.

---

## Contact

For any inquiries, please reach out via email bishwakiran725@gmail.com.

---

## Video Demonstration

A video demonstration of the chatbot is included in `video_demo.mp4`.

---

## Report

A detailed report explaining the implementation and technical details can be found in `report.pdf`.

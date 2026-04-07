# ML Buddy Chatbot 🤖

An advanced Flask-based chatbot with text-to-image generation, voice input, and Machine Learning knowledge.

## Features
- **ML Knowledge**: Explains various Machine Learning topics.
- **Image Generation**: Uses HuggingFace Stable Diffusion API to generate diagrams or images.
- **Voice Input**: Integrated microphone feature for hands-free interaction.
- **Modern UI**: Clean and responsive design.

## Setup Instructions

### 1. Prerequisites
- Python 3.x installed.
- Google Chrome browser (required for Voice Input).

### 2. Install Dependencies
Open your terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### 3. API Key Setup
1. Create a [HuggingFace account](https://huggingface.co/) if you don't have one.
2. Go to **Settings > Access Tokens** and create a new "Read" token.
3. Open the `.env` file in this folder.
4. Replace `your_huggingface_api_key` with your actual token:
   ```env
   HUGGINGFACE_API_KEY="hf_your_real_token_here"
   ```

### 4. Run the Project
Run the following command:
```bash
python app.py
```
The application will start at `http://127.0.0.1:5000` and should open automatically in your browser.

## How to Use
- **Text Chat**: Type questions like "What is supervised learning?".
- **Diagrams**: Ask "Show me a decision tree diagram".
- **Voice**: Click the 🎤 icon, wait for it to turn red (🛑), and speak clearly.
- **Image Generation**: Type "Generate image of a futuristic robot".

## Project Structure
- `app.py`: Backend Flask logic and API integration.
- `static/app.js`: Frontend logic for chat, images, and voice.
- `static/style.css`: UI styling.
- `templates/index.html`: Main HTML structure.
- `.env`: Environment variables (API Keys).

# AI Blog Generator

The AI Blog Generator is a web-based application that utilizes a Language Learning Model (LLM) via the OpenRouter API to generate coherent, detailed, and contextually relevant blog posts based on user prompts. This application is built using Flask and is designed to run both locally and in production environments.
- Live Link - https://ai-blogger-ra7l.onrender.com/

## Features

- **Generate Blog Posts**: Input a prompt and receive a generated blog post of approximately 1000 words.
- **Responsive Web Interface**: Built using Flask and Bootstrap for a responsive design that works on desktop and mobile browsers.
- **Secure API Integration**: Uses environment variables to securely integrate with OpenRouter's LLM API.

## Prerequisites

Before you begin installation, ensure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Installation

Follow these steps to get your development environment set up:

1. **Clone the repository**
   ```bash
   git clone https://github.com/KasAgg21/ai-blogger.git
   cd ai_blog_generator
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix or MacOS
   venv\Scripts\activate  # On Windows
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root of your project directory and add the following:
   ```plaintext
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

## Usage

To run the application locally:

```bash
python app.py
```

This will start the Flask development server. You can access the web interface by navigating to `http://127.0.0.1:5000/` in your web browser.

### How to Use the AI Blog Generator

1. **Enter a Prompt**: Use the text area on the web page to input your prompt.
2. **Generate Blog**: Click the "Generate Blog" button.
3. **View the Blog**: The generated blog post will appear below the form.



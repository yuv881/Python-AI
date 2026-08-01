# Python-AI

Shifra is a Django-based AI voice assistant with a web command API, text-to-speech output, web search helpers, system controls, and Hugging Face hosted AI responses.

## Live Preview

Preview: https://python-ai-7qx5.onrender.com

Render service id: `srv-d9mps1e417fc73bur7fg`

## Features

- Django web interface and command API
- Voice input with `SpeechRecognition`
- Text-to-speech with `pyttsx3`
- Hosted AI responses through `huggingface_hub`
- Google, YouTube, Wikipedia, and joke helpers
- Basic Windows desktop controls for local use
- IP-based rate limiting for the command API

## Live App Limitations

The live Render deployment runs on a Linux server, so it cannot control your personal Windows desktop directly.

These commands work only when running locally on Windows:

- Open or close desktop apps such as Notepad, Paint, Chrome, or Calculator
- Open local folders such as Downloads, Desktop, Documents, or Pictures
- Change system volume
- Lock the screen

On Render, those commands return a clear message instead of trying to run desktop-only actions on the server.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
HF_Token=your_hugging_face_token
COMMAND_RATE_LIMIT=20
COMMAND_RATE_LIMIT_WINDOW=60
```

Run locally:

```bash
python manage.py runserver
```

## API

Command endpoint:

```txt
POST /api/command/
```

Example JSON body:

```json
{
  "command": "tell me a joke"
}
```

## Rate Limiting

The command API is rate limited per client IP.

Default values:

```txt
COMMAND_RATE_LIMIT=20
COMMAND_RATE_LIMIT_WINDOW=60
```

This allows 20 command requests per 60 seconds. When the limit is exceeded, the API returns `429 Too Many Requests`.

## Render Deployment

The app uses Gunicorn on Render.

Start command:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

The same command is defined in `Procfile`.

Recommended Render environment variables:

```env
HF_Token=your_hugging_face_token
COMMAND_RATE_LIMIT=20
COMMAND_RATE_LIMIT_WINDOW=60
ALLOWED_HOSTS=localhost,127.0.0.1,python-ai-7qx5.onrender.com,.onrender.com
```

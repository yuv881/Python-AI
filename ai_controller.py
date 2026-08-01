import os
from dotenv import load_dotenv
from speech_engine import speak

# Load environment variables from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_Token")

# Initialize Hugging Face Client
_client = None


def get_hf_client():
    token = os.getenv("HF_Token") or HF_TOKEN
    try:
        from huggingface_hub import InferenceClient
        return InferenceClient(token=token, timeout=10)
    except Exception as e:
        print(f"HF Client Init Error: {e}")
        return None


def ask_ai(prompt, model="moonshotai/Kimi-K3"):
    """Query Hugging Face AI model for a text/chat response."""
    if not prompt:
        return "Please ask a question."

    client = get_hf_client()
    if not client:
        err_msg = "Hugging Face client is not configured. Please check HF_Token in .env."
        speak(err_msg)
        return err_msg

    models_to_try = [
        "Qwen/Qwen2.5-7B-Instruct",
        "meta-llama/Llama-3.2-3B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.3",
        model
    ]

    for model_name in models_to_try:
        # Try chat completion format first with fast response
        try:
            messages = [{"role": "user", "content": prompt}]
            completion = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=250
            )
            if completion and completion.choices:
                result = completion.choices[0].message.content.strip()
                speak(result)
                return result
        except Exception as e_chat:
            # Try text generation format
            try:
                response = client.text_generation(
                    prompt,
                    model=model_name,
                    max_new_tokens=250,
                    return_full_text=False
                )
                if response:
                    result = response.strip()
                    speak(result)
                    return result
            except Exception as e_gen:
                continue

    fallback_msg = "Sorry, I couldn't get a response from the Hugging Face AI model right now."
    speak(fallback_msg)
    return fallback_msg


def load_local_kimi_model(model_name="moonshotai/Kimi-K3"):
    """Load local transformers AutoModel for moonshotai/Kimi-K3."""
    try:
        from transformers import AutoModel, AutoTokenizer
        print(f"Loading local model {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModel.from_pretrained(model_name, trust_remote_code=True, device_map="auto")
        return model, tokenizer
    except Exception as e:
        print(f"Failed to load local model {model_name}: {e}")
        return None, None

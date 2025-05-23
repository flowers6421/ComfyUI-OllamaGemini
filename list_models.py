import os
# import json # Not needed anymore as we're reading from env
import requests
from google import generativeai as genai
from openai import OpenAI

def get_api_keys():
    """
    Retrieves API keys from environment variables.
    Looks for GEMINI_API_KEY and OPENAI_API_KEY.
    """
    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not gemini_api_key:
            print("Warning: GEMINI_API_KEY environment variable not set.")
        if not openai_api_key:
            print("Warning: OPENAI_API_KEY environment variable not set.")

        return gemini_api_key, openai_api_key
    except Exception as e:
        print(f"Error getting API keys from environment variables: {str(e)}")
        return None, None

def get_gemini_models():
    # Default models if API call fails
    default_gemini_models = [
        # Gemini 2.5 Models
        "gemini-2.5-pro-exp-03-25",
        # Gemini 2.0 Models
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash-exp-image-generation",
        # Gemini 1.5 Models
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        # Image Generation Models
        "imagen-3.0-generate-002"
    ]

    gemini_api_key, _ = get_api_keys()
    if not gemini_api_key:
        print("Gemini API key is missing. Using default model list.")
        return default_gemini_models

    try:
        genai.configure(api_key=gemini_api_key)
        models = genai.list_models()
        model_names = [model.name for model in models]
        # Extract just the model name from the full path
        model_names = [name.split('/')[-1] for name in model_names]
        print(f"Gemini models fetched: {len(model_names)} models available")

        # Include common and image generation models that might not be returned by API
        for model in default_gemini_models:
            if model not in model_names:
                model_names.append(model)
        return sorted(model_names)
    except Exception as e:
        print(f"Error fetching Gemini models: {str(e)}")
        print("Using default model list.")
        return default_gemini_models

def get_openai_models():
    # Default models if API call fails
    default_openai_models = [
        # GPT-4 Family
        "gpt-4o-mini",
        "gpt-4o-mini-2024-07-18",
        # GPT-3.5 Family
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo-16k",
        # O1 Family
        "o1-preview",
        "o1-preview-2024-09-12",
        "o1-mini",
        "o1-mini-2024-09-12",
        # DeepSeek Models
        "deepseek-ai/deepseek-r1"
    ]

    _, openai_api_key = get_api_keys()
    if not openai_api_key:
        print("OpenAI API key is missing. Using default model list.")
        return default_openai_models

    try:
        client = OpenAI(api_key=openai_api_key)
        models = client.models.list()
        model_ids = [model.id for model in models.data]
        print(f"OpenAI models fetched: {len(model_ids)} models available")

        # Include common models that might not be returned by API
        for model in default_openai_models:
            if model not in model_ids:
                model_ids.append(model)
        return sorted(model_ids)
    except Exception as e:
        print(f"Error fetching OpenAI models: {str(e)}")
        print("Using default OpenAI model list.")
        return default_openai_models

def get_gemini_image_models():
    """Get models specifically for image generation"""
    return ["gemini-2.0-flash-exp-image-generation", "imagen-3.0-generate-002"]

if __name__ == "__main__":
    print("--- Attempting to retrieve API keys from environment variables ---")
    gemini_key, openai_key = get_api_keys()
    if gemini_key:
        print("Gemini API Key found.")
    if openai_key:
        print("OpenAI API Key found.")
    print("------------------------------------------------------------------")

    print("\n=== Gemini Models ===")
    gemini_models = get_gemini_models()
    for model in gemini_models:
        print(f"Name: {model}")
    print(f"\nTotal Gemini Models listed: {len(gemini_models)}")

    print("\n=== OpenAI Models ===")
    openai_models = get_openai_models()
    for model in openai_models:
        print(f"ID: {model}")
    print(f"\nTotal OpenAI Models listed: {len(openai_models)}")

# import zipfile
# import os
# import shutil
# import requests

# OLLAMA_MODEL = "codellama:7b-instruct"

# def extract_zip(zip_path, out_dir="unzipped_code"):
#     if os.path.exists(out_dir):
#         shutil.rmtree(out_dir)
#     os.makedirs(out_dir, exist_ok=True)

#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(out_dir)
#     return out_dir

# def explain_file_with_ollama(filename, content):
#     prompt = f"""
# Explain in simple language what this code file does.

# File: {filename}

# Code:
# {content[:3000]}
# """

#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": OLLAMA_MODEL,
#                 "prompt": prompt,
#                 "stream": False
#             },
#             timeout=60
#         )
#         return response.json().get("response", "No response")
#     except Exception as e:
#         return f"Error: {str(e)}"

# def explain_single_code_file(filename, content):
#     return explain_file_with_ollama(filename, content)

# def process_zip_and_explain(zip_path):
#     result = {}
#     extracted_path = extract_zip(zip_path)

#     for root, _, files in os.walk(extracted_path):
#         for file in files:
#             if file.endswith((".py", ".js", ".ts", ".java", ".json", ".html", ".css", ".txt")):
#                 path = os.path.join(root, file)
#                 try:
#                     with open(path, "r", encoding="utf-8", errors="ignore") as f:
#                         content = f.read()
#                     result[file] = explain_file_with_ollama(file, content)
#                 except Exception as e:
#                     result[file] = f"Error reading file: {e}"
#     return result



import zipfile
import os
import shutil
import requests
from gtts import gTTS

OLLAMA_MODEL = "codellama:7b-instruct"
STATIC_DIR = "static/audio"

# Make sure the audio directory exists
os.makedirs(STATIC_DIR, exist_ok=True)


def extract_zip(zip_path, out_dir="unzipped_code"):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(out_dir)
    return out_dir


def speak_explanation(text, filename):
    try:
        tts = gTTS(text)
        audio_path = os.path.join(STATIC_DIR, f"{filename}.mp3")
        tts.save(audio_path)
        return f"/static/audio/{filename}.mp3"
    except Exception as e:
        return f"Error generating audio: {e}"


def explain_file_with_ollama(filename, content):
    prompt = f"""
You are an expert code reviewer. Please do the following:

1. Explain in simple terms what this code file does.
2. Suggest 2–3 ways the code can be optimized, refactored, or secured.

File Name: {filename}

Code:
{content[:3000]}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=90
        )
        explanation = response.json().get("response", "No response")
        audio_url = speak_explanation(explanation, filename.replace(".", "_"))
        return {"text": explanation, "audio_url": audio_url}
    except Exception as e:
        return {"text": f"Error: {str(e)}", "audio_url": None}


def explain_single_code_file(filename, content):
    return explain_file_with_ollama(filename, content)


def process_zip_and_explain(zip_path):
    result = {}
    extracted_path = extract_zip(zip_path)

    for root, _, files in os.walk(extracted_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".java", ".json", ".html", ".css", ".txt")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    result[file] = explain_file_with_ollama(file, content)
                except Exception as e:
                    result[file] = {"text": f"Error reading file: {e}", "audio_url": None}
    return result

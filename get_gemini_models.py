# Modulo per trovare tutti i modelli raggiungibili con la tua api key

from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(transport='grpc')

def list_models():
    for i, m in zip(range(5), genai.list_models()):
        print(f"Name: {m.name} Description: {m.description} support: {m.supported_generation_methods}")

if __name__ == "__main__":
    list_models()

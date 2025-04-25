import google.generativeai as genai

genai.configure(api_key="AIzaSyBSAkQe7FSFRCyHQmKVKuKYsX7jG_NQWw0")
for model in genai.list_models():
    print(model.name)

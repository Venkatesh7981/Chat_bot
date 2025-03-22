import google.generativeai as genai

genai.configure(api_key="AIzaSyBCz4zINkwpHpauxwFOZ6FN_FBtfhPJ8a0")

# List available models
models = genai.list_models()
for m in models:
    print(m.name)

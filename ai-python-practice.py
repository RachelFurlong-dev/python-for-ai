user_prompt="What is generative ai"
print(user_prompt)
#a variable to store a string and print to the terminal

ai_models=["GPT", "Phi", "Llama"]
print(ai_models[1])
#A dictionary of ai models and printing a selected model to the terminal

ai_models=["GPT", "Phi", "Llama", "Claude"]

for model in ai_models:
    print("Testing model:", model)
#A loop is useful when I want to process several items

#----------------lesson2--------------------
ai_response = {
    "model": "AI-Model-1",
    "prompt": "What is machine learning?",
    "answer": "Machine learning finds patterns in data.",
    "confidence": 0.8
}

print(ai_response)#prints a python dictionary containing key value pairs from structured data
print(ai_response["answer"])

print(ai_response["confidence"])
print(ai_response["model"])

#Learning how your Python program can receive structured information from an AI system and extract the particular pieces of information it needs.

if ai_response["confidence"] > 0.9: 
    print("High confidence")
else:
    print("low confidence")

#------from dictionary to JSON---------
import json 
json_response = json.dumps(ai_response) 
print(json_response)
print(type(ai_response)) 
print(type(json_response))

"""
AI connection - Imagine:

Python dictionary → JSON → internet → AI service

and:

AI service → JSON → Python program

You have now encountered one of the basic mechanisms behind AI applications.
"""

#------------------LESSON 3 — Functions and AI Workflows----------------


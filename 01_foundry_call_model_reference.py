# 1. GET THE TOOLS NEEDED TO TALK TO AZURE AI
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# 2. WHERE IS MY AI SERVICE?
endpoint = "MY_ENDPOINT"

# 3. WHICH DEPLOYMENT DO I WANT TO USE?
deployment_name = "model-router"

# 4. PROVE TO AZURE THAT I AM AUTHORISED
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "MY_AZURE_SCOPE"
)

# 5. CREATE THE CLIENT THAT TALKS TO THE SERVICE
client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

# 6. SEND A USER MESSAGE TO THE MODEL
completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ],
)

# 7. GET THE MODEL'S RESPONSE AND DISPLAY IT
print(completion.choices[0].message)
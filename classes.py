class Dog:
    def __init__(self,name,breed):
        self.name = name
        self.breed = breed

# Create  dog objects - using positional arguments
dog1 = ("Superdog", "terrier")
dog2 = ("Sillydog", "spaniel")

#or with named arguments
jerry = Dog(name="jerry", breed="labrador")

jerry.breed

#self refers to the current object. Its how an object keeps track of its own data

#-----------------------apis and classes-------------------------------

class APIConfig:
    def __init__(self, api_key, model="gpt-3.5-turbo", max_tokens=100):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.base_url = "https://api.openai.com/v1"


# Create different configurations

# Using positional for required arg, named for optional
dev_config = APIConfig("sk-dev-key", max_tokens=50)

# Using all named arguments (clearest)
prod_config = APIConfig(
    api_key="sk-prod-key",
    model="gpt-4",
    max_tokens=1000
)

# Access the configuration
print(dev_config.model)
print(prod_config.model)
print(prod_config.max_tokens)
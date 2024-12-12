
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()



# Example usage
# Access the variables
database_url = os.getenv("DATABASE_USER")
secret_key = os.getenv("SECRET_KEY")
debug_mode = os.getenv("DEBUG")

print(f"Database URL: {database_url}")
print(f"Secret Key: {secret_key}")
print(f"Debug Mode: {debug_mode}")


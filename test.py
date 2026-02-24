from dotenv import load_dotenv
import os
load_dotenv()
print(api_key=os.getenv("GROQ_API_KEY"))

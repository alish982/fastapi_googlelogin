import os 
from dotenv import load_dotenv

load_dotenv()


CLIET_ID = os.environ.get('client-id', None)
CLINET_SECRET = os.environ.get('client-secret', None)
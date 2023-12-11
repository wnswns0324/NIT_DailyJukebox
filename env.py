from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
creddata = os.getenv("CRED_LOCATION")
firebase_url = os.getenv("FIREBASE_URL")

instagram_username = os.getenv("IG_ID")
instagram_password = os.getenv("IG_PW")

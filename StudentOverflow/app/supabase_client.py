import os
from supabase import create_client, Client
from flask import session, g

from dotenv import load_dotenv


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


supabase_auth: Client = create_client(SUPABASE_URL, ANON_KEY)
supabase_db: Client = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)


supabase = supabase_db

def get_user_from_session():
    return session.get("user")  



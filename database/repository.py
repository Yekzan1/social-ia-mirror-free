from database.connection import get_db
from core.security import verify_password, hash_password
import streamlit as st

class Repository:
    def __init__(self):
        self.client = get_db()

    def get_user_by_username(self, username):
        try:
            response = self.client.table("users").select("*").eq("username", username).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    def get_user_by_credentials(self, identifier, password):
        try:
            # Check username or email
            response = self.client.table("users").select("*").or_(f"username.eq.{identifier},email.eq.{identifier}").execute()
            if response.data:
                user = response.data[0]
                if verify_password(user['password_hash'], password):
                    return user
            return None
        except Exception as e:
            print(f"Auth error: {e}")
            return None

    def create_user(self, username, email, password, role='user'):
        try:
            pwd_hash = hash_password(password)
            data = {
                "username": username,
                "email": email,
                "password_hash": pwd_hash,
                "role": role,
                "xp": 0
            }
            response = self.client.table("users").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def handle_social_login(self, provider):
        username = f"{provider}_user"
        email = f"{provider}@mindloop.io"
        user = self.get_user_by_username(username)
        if not user:
            # Create a mock secure password for social login
            user = self.create_user(username, email, f"social_{provider}_mindloop", role='user')
        return user

    def add_post(self, author_id, content, subject, media_data=None, media_type=None, is_help=False):
        try:
            data = {
                "author_id": author_id,
                "content": content,
                "subject": subject,
                "media_data": media_data,
                "media_type": media_type,
                "is_help_needed": is_help
            }
            response = self.client.table("posts").insert(data).execute()
            
            # Increment XP
            self.client.table("users").update({"xp": "xp + 50"}).eq("id", author_id).execute() # Note: Supabase increment logic varies, might need RPC
            
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error adding post: {e}")
            return None

    def get_feed(self, limit=50):
        try:
            # Supabase join syntax: select("*, users(*)")
            response = self.client.table("posts").select("*, users(username, xp)").order("created_at", desc=True).limit(limit).execute()
            
            # Flatten the result to match existing expected format
            feed = []
            for item in response.data:
                item['author_name'] = item['users']['username']
                item['author_xp'] = item['users']['xp']
                feed.append(item)
            return feed
        except Exception as e:
            print(f"Error fetching feed: {e}")
            return []

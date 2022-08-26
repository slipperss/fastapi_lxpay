from rejson import Path

from src.apps.user.models import User


class Cache:
    def __init__(self, json_client):
        self.json_client = json_client

    async def get_chat_history(self, token: str):
        print(self.json_client.__dir__)
        data = self.json_client.jsonget(str(token), Path.rootPath())
        return data

    async def get_all_user_chats(self, user: User):
        data = self.json_client.jsonget('chats', Path('.chats.members'), str(user.id))
        return data

    async def add_message_to_cache(self, token: str, message_data: dict):
        self.json_client.jsonarrappend(
            str(token), Path('.messages'), message_data)
        print(f"Message ( {message_data['msg']} ) added to {token} cache")

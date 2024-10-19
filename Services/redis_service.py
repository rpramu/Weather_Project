from redis import Redis

import dotenv

dotenv.load_dotenv()


class RedisService:
    """Service class to interact with Redis"""
    def __init__(self, host: str, port: int):
        self.client = Redis(host=host, port=port)

    def get(self, key: str):
        """Get the value for the given key"""
        return self.client.get(key)

    def setex(self, key: str, value: str, ttl: int):
        """Set the value for the given key with an expiry time"""
        self.client.setex(key, ttl, value)

    def publish(self, channel: str, message: str):
        """Publish a message to the given channel"""
        self.client.publish(channel, message)
import redis
import time
import json
import random
from datetime import datetime
from config import REDIS_CONFIG, BUFFER_CONFIG, MESSAGE_CONFIG


class MessageProducer:
    def __init__(self):
        self.redis_client = redis.Redis(**REDIS_CONFIG)
        self.buffer_key = BUFFER_CONFIG['buffer_key']
        self.message_count = 0

    def generate_message(self):
        self.message_count += 1
        message_types = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
        message_templates = [
            'User {user_id} performed {action}',
            'System {component} reported {status}',
            'Database query executed in {time}ms',
            'API endpoint {endpoint} received request',
            'Cache {key} updated successfully'
        ]

        return {
            'id': self.message_count,
            'timestamp': datetime.now().isoformat(),
            'type': random.choice(message_types),
            'message': random.choice(message_templates).format(
                user_id=random.randint(1, 1000),
                action=random.choice(['login', 'logout', 'purchase', 'view']),
                component=random.choice(['auth', 'database', 'cache', 'api']),
                status=random.choice(['healthy', 'degraded', 'error']),
                time=random.randint(10, 500),
                endpoint=random.choice(['/api/v1/users', '/api/v1/products']),
                key=random.choice(['user:123', 'product:456', 'session:789'])
            ),
            'source': f'producer_{random.randint(1, 3)}'
        }

    def send_message(self, message):

        try:
            self.redis_client.lpush(self.buffer_key, json.dumps(message))
            print(f" Sent message #{message['id']}: {message['message']}")
            return True
        except Exception as e:
            print(f" Error sending message: {e}")
            return False

    def run(self):
        # Симуляция цикла отправки сообщений
        print("Starting Message Producer:")
        print(f" Buffer key: {self.buffer_key}")

        try:
            for i in range(MESSAGE_CONFIG['max_messages']):
                message = self.generate_message()
                self.send_message(message)

                buffer_size = self.redis_client.llen(self.buffer_key)
                print(f"    Buffer size: {buffer_size} messages")

                time.sleep(MESSAGE_CONFIG['delay_between_messages'])

        except KeyboardInterrupt:
            print("\n Producer stopped by user")

        finally:
            buffer_size = self.redis_client.llen(self.buffer_key)
            print(f"\n  Final buffer size: {buffer_size} messages")


if __name__ == "__main__":
    producer = MessageProducer()
    producer.run()

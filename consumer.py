import redis
import time
import json
import os
from datetime import datetime
from config import REDIS_CONFIG, BUFFER_CONFIG


class MessageConsumer:
    def __init__(self):
        self.redis_client = redis.Redis(**REDIS_CONFIG)
        self.buffer_key = BUFFER_CONFIG['buffer_key']
        self.batch_size = BUFFER_CONFIG['batch_size']
        self.processing_delay = BUFFER_CONFIG['processing_delay']
        self.timeout = BUFFER_CONFIG['timeout']
        self.processed_count = 0

        self.logs_dir = "application_logs"
        os.makedirs(self.logs_dir, exist_ok=True)

        self.log_files = {
            'INFO': os.path.join(self.logs_dir, "info.log"),
            'WARNING': os.path.join(self.logs_dir, "warning.log"),
            'ERROR': os.path.join(self.logs_dir, "error.log"),
            'DEBUG': os.path.join(self.logs_dir, "debug.log")
        }

        for log_type, log_path in self.log_files.items():
            try:
                with open(log_path, 'a', encoding='utf-8') as f:
                    f.write(f"# Log file initialized at {datetime.now()}\n")
                print(f"  Log file ready: {log_path}")
            except Exception as e:
                print(f"  Failed to initialize {log_path}: {e}")

    def write_to_log(self, message_data):

        try:
            msg_type = message_data.get('type', 'INFO')

            if msg_type not in self.log_files:
                msg_type = 'INFO'

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} | {message_data['source']} | {message_data['message']}\n"

            log_file = self.log_files[msg_type]
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

            return True

        except Exception as e:
            print(f"    Error writing to log: {e}")
            return False

    def process_message(self, message):

        try:
            message_data = json.loads(message)

            log_result = self.write_to_log(message_data)

            if log_result:
                print(f"    Logged to {message_data['type']}.log: {message_data['message'][:60]}...")
            else:
                print(f"    Failed to log: {message_data['message'][:60]}...")

            return True
        except json.JSONDecodeError as e:
            print(f"  Error decoding message: {e}")
            return False

    def process_batch(self, messages):

        if not messages:
            return

        print(f"\n  Processing batch of {len(messages)} messages...")

        success_count = 0
        for message in messages:
            if self.process_message(message=message):
                success_count += 1

        self.processed_count += success_count
        print(f"  Batch processed. Success: {success_count}/{len(messages)}")
        print(f"  Total processed: {self.processed_count} messages")

    def get_batch(self):
        messages = []

        for _ in range(self.batch_size):

            message = self.redis_client.rpop(self.buffer_key)
            if message:
                messages.append(message)
            else:
                break

        return messages

    def get_batch_blocking(self):

        messages = []

        result = self.redis_client.brpop(self.buffer_key, timeout=self.timeout)
        if result:

            messages.append(result[1])

            for _ in range(self.batch_size - 1):
                message = self.redis_client.rpop(self.buffer_key)
                if message:
                    messages.append(message)
                else:
                    break

        return messages

    def run(self):

        print(" Starting Message Consumer...")
        print(f"  Buffer key: {self.buffer_key}")
        print(f"  Batch size: {self.batch_size}")
        print(f"  Processing delay: {self.processing_delay}s")

        try:
            while True:

                buffer_size = self.redis_client.llen(self.buffer_key)
                print(f"    Current buffer size: {buffer_size}")

                messages = []

                if buffer_size >= self.batch_size:
                    messages = self.get_batch()
                else:
                    print("    Waiting for messages...")
                    messages = self.get_batch_blocking()

                if messages:
                    self.process_batch(messages)
                    print(f"    Sleeping for {self.processing_delay} seconds...")

                time.sleep(self.processing_delay)

        except KeyboardInterrupt:
            print(" Consumer stopped by user")
            print(f" Total messages processed: {self.processed_count}")


if __name__ == "__main__":
    consumer = MessageConsumer()
    consumer.run()

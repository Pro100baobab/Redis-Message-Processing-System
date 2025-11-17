REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True
}

BUFFER_CONFIG = {
    'buffer_key': 'message_buffer',
    'batch_size': 5,
    'processing_delay': 4,
    'timeout': 10
}

MESSAGE_CONFIG = {
    'max_messages': 20,
    'delay_between_messages': 2
}
# Redis Message Processing System

A Python-based message processing system using Redis as a message broker. The system consists of a producer that generates messages and a consumer that processes them in batches with logging capabilities.

## 🚀 Features

- **Message Generation**: Create diverse system messages with different types (INFO, WARNING, ERROR, DEBUG)
- **Redis Buffering**: Temporary message storage in Redis List before processing
- **Batch Processing**: Efficient message processing in batches for performance optimization
- **Log Sorting**: Automatic saving of messages to appropriate log files by type
- **Flexible Configuration**: Easy system parameter tuning through configuration file

## 📋 Requirements

- Python 3.7+
- Redis Server
- Libraries: `redis`

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/Pro100baobab/Redis-Message-Processing-System.git
cd redis-message-processing
```

2. Install dependencies:
```bash
pip install redis
```

3. Make sure Redis server is running:
```bash
redis-server
```

## ⚙️ Configuration

All system settings are located in `config.py`:

### Redis Configuration
```python
REDIS_CONFIG = {
    'host': 'localhost',  # Redis host
    'port': 6379,         # Redis port
    'db': 0,              # Database number
    'decode_responses': True  # Response decoding
}
```

### Buffer Configuration
```python
BUFFER_CONFIG = {
    'buffer_key': 'message_buffer',  # Redis List key for messages
    'batch_size': 5,                 # Processing batch size
    'processing_delay': 4,           # Delay between batch processing (sec)
    'timeout': 10                    # Message waiting timeout (sec)
}
```

### Message Configuration
```python
MESSAGE_CONFIG = {
    'max_messages': 20,              # Maximum number of messages
    'delay_between_messages': 2      # Delay between messages (sec)
}
```

## 🚀 Usage

### Starting Producer
```bash
python producer.py
```
The producer will start generating and sending messages to Redis.

### Starting Consumer
```bash
python consumer.py
```
The consumer will start processing messages from Redis and saving them to appropriate log files.

### Parallel Execution
For full system operation, it's recommended to run both components simultaneously (in different terminals).

## 📁 Project Structure

```
redis-message-processing/
├── config.py           # Configuration parameters
├── producer.py         # Message generator
├── consumer.py         # Message processor
├── application_logs/   # Logs directory
│   ├── info.log       # INFO type logs
│   ├── warning.log    # WARNING type logs
│   ├── error.log      # ERROR type logs
│   └── debug.log      # DEBUG type logs
└── README.md          # Documentation
```

## 🔍 Implementation Details

### MessageProducer
- Generates random system messages of various types
- Sends messages to Redis List using LPUSH
- Supports configurable delay between messages
- Displays current buffer size

### MessageConsumer
- Processes messages in batches for efficiency
- Uses combination of RPOP and BRPOP for non-blocking and blocking reads
- Saves messages to log files by type
- Automatically creates log directory and files on startup

### Message Types
- **INFO**: Informational messages
- **WARNING**: Warnings
- **ERROR**: Errors
- **DEBUG**: Debug information

## 📊 Monitoring

The system provides information about:
- Number of sent messages
- Redis buffer size
- Number of processed messages
- Success rate of each batch processing

## 🛠️ Possible Extensions

- Adding monitoring via Redis Pub/Sub
- Implementing multiple consumers
- Adding error reprocessing mechanism
- Integration with log collection systems (ELK Stack)
- Adding performance metrics

## 📝 Notes

- Ensure Redis server is accessible at the configured address
- For production use, configure Redis authentication
- Set up log rotation for long-term usage
- Consider using Redis persistence for reliability

---

# Система обработки сообщений с Redis

Проект представляет собой систему для обработки сообщений с использованием Redis в качестве брокера сообщений. Система состоит из продюсера, генерирующего сообщения, и консьюмера, обрабатывающего их в пакетном режиме с сохранением в логи.

## 🚀 Основные возможности

- **Генерация сообщений**: Создание разнообразных системных сообщений с различными типами (INFO, WARNING, ERROR, DEBUG)
- **Буферизация в Redis**: Временное хранение сообщений в Redis List перед обработкой
- **Пакетная обработка**: Эффективная обработка сообщений пачками для оптимизации производительности
- **Сортировка логов**: Автоматическое сохранение сообщений в соответствующие файлы логов по типу
- **Гибкая конфигурация**: Легкая настройка параметров системы через конфигурационный файл

## 📋 Требования

- Python 3.7+
- Redis Server
- Библиотеки: `redis`

## 🔧 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Pro100baobab/Redis-Message-Processing-System.git
cd redis-message-processing
```

2. Установите зависимости:
```bash
pip install redis
```

3. Убедитесь, что Redis сервер запущен:
```bash
redis-server
```

## ⚙️ Конфигурация

Все настройки системы находятся в файле `config.py`:

### Redis конфигурация
```python
REDIS_CONFIG = {
    'host': 'localhost',  # Хост Redis
    'port': 6379,         # Порт Redis
    'db': 0,              # Номер базы данных
    'decode_responses': True  # Декодирование ответов
}
```

### Конфигурация буфера
```python
BUFFER_CONFIG = {
    'buffer_key': 'message_buffer',  # Ключ Redis List для сообщений
    'batch_size': 5,                 # Размер пакета для обработки
    'processing_delay': 4,           # Задержка между обработкой пакетов (сек)
    'timeout': 10                    # Таймаут ожидания сообщений (сек)
}
```

### Конфигурация сообщений
```python
MESSAGE_CONFIG = {
    'max_messages': 20,              # Максимальное количество сообщений
    'delay_between_messages': 2      # Задержка между сообщениями (сек)
}
```

## 🚀 Использование

### Запуск продюсера
```bash
python producer.py
```
Продюсер начнет генерировать и отправлять сообщения в Redis.

### Запуск консьюмера
```bash
python consumer.py
```
Консьюмер начнет обрабатывать сообщения из Redis и сохранять их в соответствующие файлы логов.

### Параллельный запуск
Для полной работы системы рекомендуется запустить оба компонента одновременно (в разных терминалах).

## 📁 Структура проекта

```
redis-message-processing/
├── config.py           # Конфигурационные параметры
├── producer.py         # Генератор сообщений
├── consumer.py         # Обработчик сообщений
├── application_logs/   # Директория с логами
│   ├── info.log       # Логи типа INFO
│   ├── warning.log    # Логи типа WARNING
│   ├── error.log      # Логи типа ERROR
│   └── debug.log      # Логи типа DEBUG
└── README.md          # Документация
```

## 🔍 Детали реализации

### MessageProducer
- Генерирует случайные системные сообщения различных типов
- Отправляет сообщения в Redis List используя LPUSH
- Поддерживает настраиваемую задержку между сообщениями
- Отображает текущий размер буфера

### MessageConsumer
- Обрабатывает сообщения пачками для эффективности
- Использует комбинацию RPOP и BRPOP для неблокирующего и блокирующего чтения
- Сохраняет сообщения в файлы логов по типам
- Автоматически создает директорию и файлы логов при запуске

### Типы сообщений
- **INFO**: Информационные сообщения
- **WARNING**: Предупреждения
- **ERROR**: Ошибки
- **DEBUG**: Отладочная информация

## 📊 Мониторинг

Система предоставляет информацию о:
- Количестве отправленных сообщений
- Размере буфера в Redis
- Количестве обработанных сообщений
- Успешности обработки каждого пакета

## 🛠️ Возможные расширения

- Добавление мониторинга через Redis Pub/Sub
- Реализация множественных консьюмеров
- Добавление механизма повторной обработки ошибок
- Интеграция с системами сбора логов (ELK Stack)
- Добавление метрик производительности

## 📝 Примечания

- Убедитесь, что Redis сервер доступен по указанному в конфигурации адресу
- Для production использования настройте аутентификацию Redis
- Настройте ротацию логов для долгосрочного использования
- Рассмотрите использование Redis persistence для надежности

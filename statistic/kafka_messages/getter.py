import json
from statistic.kafka_messages.consumer import consumer as kafka_consumer


kafka_consumer.subscribe(['kafka_messages_topic'])

while True:
    try:
        msg = kafka_consumer.poll(timeout=1)
        if msg is not None:
            message_dict = json.loads(msg.value().decode("utf-8"))
            print(message_dict)
    except KeyboardInterrupt:
        print("Kafka consumer is closed")
        kafka_consumer.close()
        break


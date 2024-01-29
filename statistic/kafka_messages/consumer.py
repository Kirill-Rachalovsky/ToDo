from confluent_kafka import Consumer
from dotenv import dotenv_values

env = dotenv_values("../../.env")

conf = {'bootstrap.servers': env['BOOTSTRAP_SERVER'],
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': env['CLUSTER_API_KEY'],
        'sasl.password': env['CLUSTER_API_SECRET'],
        'group.id': 'python_example_group_1',
        'auto.offset.reset': 'earliest'}

consumer = Consumer(conf)

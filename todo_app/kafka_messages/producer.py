import json

from confluent_kafka import Producer
import socket

from dotenv import dotenv_values

env = dotenv_values(".env_docker")

conf = {'bootstrap.servers': env['BOOTSTRAP_SERVER'],
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': env['CLUSTER_API_KEY'],
        'sasl.password': env['CLUSTER_API_SECRET'],
        'client.id': socket.gethostname()}

producer = Producer(conf)

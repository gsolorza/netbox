#!/usr/bin/env python
import pika
from pika import spec
import sys
import json

username = "admin"
password = "admin"
host = "localhost"
queue = "task_queue"


class sendTask:
    def __init__(self, username: str, password: str, host: str, queue: str):
        self.credentials = pika.PlainCredentials(username, password)
        self.host = host
        self.queue = queue

    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=self.credentials)  # type: ignore
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        return self.channel

    def __exit__(self, type: None, value: None, traceback: None):
        if self.connection:
            self.connection.close()


devices = json.dumps(
    {
        "devices": {
            "TP-EP-RT1": {
                "ip": "10.253.8.178",
                "port": 22,
                "protocol": "ssh",
                "username": "lairdadmin",
                "password": "WgU0znN(qhxf",
                "os": "iosxe",
            },
            "TP-Bensalem-RT1": {
                "ip": "10.253.8.177",
                "port": 22,
                "protocol": "ssh",
                "username": "lairdadmin",
                "password": "WgU0znN(qhxf",
                "os": "iosxe",
            },
        }
    }
)

with sendTask(username, password, host, queue) as channel:
    # channel.basic_publish(
    #     exchange="",
    #     routing_key=queue,
    #     body=devices,
    #     properties=pika.BasicProperties(delivery_mode=spec.PERSISTENT_DELIVERY_MODE),
    # )
    # print(" [x] Sent %r" % devices)

    channel.basic_publish(
        exchange="",
        routing_key="backup",
        body="backup",
        properties=pika.BasicProperties(delivery_mode=spec.PERSISTENT_DELIVERY_MODE),
    )

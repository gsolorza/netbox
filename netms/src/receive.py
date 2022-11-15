#!/usr/bin/env python
import pika
import schema
import json
from pprint import pprint
from ciscoNetTools import collect
from requests import request
import db

credentials = pika.PlainCredentials("admin", "admin")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)  # type: ignore
)
channel = connection.channel()
channel.queue_declare(queue="task_queue", durable=True)
channel.queue_declare(queue="backup", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    try:
        payload: dict = json.loads(body.decode())
        devices = schema.GenieBase.parse_obj(payload)
        deviceOutput = collect.inventory(devices)
        pprint(db.create(deviceOutput))
        pprint(deviceOutput)
    except Exception as error:
        print(error)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def backup(ch, method, properties, body):
    try:
        print(body)
    except Exception as error:
        print(error)
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)
channel.basic_consume(queue="backup", on_message_callback=backup)

channel.start_consuming()

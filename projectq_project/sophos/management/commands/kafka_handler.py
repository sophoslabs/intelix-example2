#  Copyright (c) 2019. Sophos Limited
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
import threading
import logging

from kafka import KafkaConsumer, TopicPartition

from client.models import Client, Platform
from event.models import SocketConnection
from localintel.models import SHA
from sophos.Notification import Notification

logger = logging.getLogger(__name__)

LOCK = threading.Lock()
NUMBER_OF_PART = 4
PARTITION_DICT = {}
KAFKA_BROKER = "localhost:9092"

from django.core.management.base import BaseCommand

from sophos.utils import MalwareLookup


def save_to_db(message):
    """
    Save Name, Path, remote_address, sha256, consumer_partition of the event
    """
    sha_in_message = message["columns"].get("sha256", "SOMETHING_RANDOM")
    sha256, created = SHA.objects.get_or_create(sha256=sha_in_message)
    platform, created = Platform.objects.get_or_create(name="Windows")

    client, created = Client.objects.get_or_create(
        ip=message["columns"]["client_ip"], os_platform=platform, os_version="1"
    )  # These IPs have to be created in advance
    socket_connection = SocketConnection.objects.create(sha256=sha256, client=client)

    socket_connection.path = message["columns"].get("path", "RANDOM_PATH")
    socket_connection.name = message["columns"]["name"]
    if message["columns"]["remote_address"] != "0":
        socket_connection.remote_address = message["columns"]["remote_address"]
    socket_connection.remote_port = message["columns"]["remote_port"]
    socket_connection.action = message["action"]
    socket_connection.save()


def submit_for_analysis(message, partition_number):
    """
    Hit intelix query to submit,
    If submit gives you UNKNOWN file, then produce a message with same
    """
    try:
        save_to_db(message)
    except Exception as e:
        logger.exception(str(e))
    if message["columns"].get("sha256") and message["columns"].get("client_ip"):
        lookup_object = MalwareLookup(
            message["columns"].get("sha256"), message["columns"]["client_ip"]
        )
        if lookup_object.score <= 20:
            message = f"SHA256: <a href='http://35.176.243.153:8888/lookup/sample/?sha={lookup_object.sha256}'>{lookup_object.sha256}</a> is shaky for IP {lookup_object.ip_addr}"
            message_slack = f"SHA256: http://35.176.243.153:8888/lookup/sample/?sha={lookup_object.sha256} is shaky for IP {lookup_object.ip_addr}"
            notifier = Notification(message, ["teams"])
            notifier_slack = Notification(message_slack, ["slack"])
            notifier_slack.notify()
            notifier.notify()
    # No need to do anything other than this, lookup_object's __init__ will set everything


def create_consumer_with_partition(partition_number):
    partition = TopicPartition("final", partition_number)

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="my-group"
        # value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
    consumer.assign([partition])
    return consumer


def start_consuming(consumer, partition_number):
    while True:
        for message in consumer:
            if message.value:
                submit_for_analysis(
                    json.loads(message.value.decode("utf-8")), message.partition
                )


class Command(BaseCommand):
    help = "Starts Kafka broker polling"

    def handle(self, *args, **options):
        logger.debug("THREAD POOL CREATED")
        consumer = create_consumer_with_partition(1)
        start_consuming(consumer, 1)

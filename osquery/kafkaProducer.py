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

import os
import logging
from kafka import KafkaProducer
import pygtail
import random

logger = logging.getLogger(__name__)


def partitioner(a, b, c):
    # return random.randint(1,4)
    return 1


def kafkaProducer(filename, kafka_broker, topic):
    pygTail = pygtail.Pygtail(filename)
    lines = pygTail.readlines()

    producer = KafkaProducer(bootstrap_servers=kafka_broker, partitioner=partitioner)
    # Asynchronous by default
    if lines:
        for line in lines:
            future = producer.send(topic, value=bytes(line.strip(), encoding="utf-8"))
        future.get()
        return 1, "All sent"
    return 0, "Nothing to send to Kafka"


if __name__ == "__main__":
    # IP and port of Kafka server
    KAFKA_IP_PORT = os.getenv("KAFKA_IP_PORT")
    # kafka.errors.NoBrokerAvailable handle this
    while 1:
        filename = "osquery/log/osqueryd.results.log"
        result = kafkaProducer(filename, KAFKA_IP_PORT, "final")
        logging.info(result)

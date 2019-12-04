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

import requests
from slack import WebClient


class Notification:

    AVAIL_CHANNELS = ["slack", "teams"]

    def __init__(self, message, channels):
        self.message = message
        if set(channels).issubset(Notification.AVAIL_CHANNELS):
            self.channels = channels
        else:
            different_channel = set(channels).difference(Notification.AVAIL_CHANNELS)
            raise ValueError(
                "Given channel(s) {} is not available yet".format(
                    ",".join(different_channel)
                )
            )

    def notify(self):
        for channel in self.channels:
            if channel == "slack":
                self.notify_slack()
            if channel == "teams":
                self.notify_teams()

    def notify_slack(self):
        token = os.environ["slack_auth"]
        client = WebClient(token=token)
        client.chat_postMessage(
            channel="#randomtesting", text=self.message, as_user=True
        )

    def notify_teams(self):
        url = os.environ["teams_webhook"]
        data = {"title": "Malicious activity detected!!!", "text": self.message}
        requests.post(url, json=data)

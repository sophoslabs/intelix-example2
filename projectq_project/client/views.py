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

from django.shortcuts import render

from client.models import Client
from event.models import SocketConnection


def list_clients(request, platform):
    """list all available clients, delete clients, """
    if request.method == "GET":
        clients = Client.objects.filter(os_platform=platform.capitalize()).order_by(
            "ip"
        )
        context = {"clients": clients.values(), "platform": platform.capitalize()}
        return render(request, "client/client.html", context)


def list_events(request, client):
    events = (
        SocketConnection.objects.filter(client__ip=client)
        .order_by("-created_at")
        .values(
            "name",
            "remote_address",
            "remote_port",
            "sha256_id",
            "sha256__reputation_score",
            "action",
            "created_at",
        )
    )
    context = {"events": events, "client": client, "name": "Clients"}
    return render(request, "client/events.html", context)

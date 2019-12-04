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

import uuid

from django.db import models

from client.models import Client
from localintel.models import SHA
from query.models import Query


class EventStream(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    couch_doc = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)


class SocketConnection(models.Model):
    ACTIONS_CHOICES = (("added", "added"), ("removed", "removed"))
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    path = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=56, null=True, blank=True)
    remote_address = models.GenericIPAddressField(null=True, blank=True)
    remote_port = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sha256 = models.ForeignKey(SHA, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(
        max_length=10, null=True, blank=True, choices=ACTIONS_CHOICES
    )


class DiskOperations(models.Model):
    pass


class Process(models.Model):
    pid = models.CharField(max_length=256, null=True, blank=True)
    path = models.CharField(max_length=256, null=True, blank=True)
    sha256 = models.ForeignKey(SHA, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=256, null=True, blank=True)
    ACTIONS_CHOICES = (("added", "added"), ("removed", "removed"))
    action = models.CharField(
        max_length=10, null=True, blank=True, choices=ACTIONS_CHOICES
    )
    pass

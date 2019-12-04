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

from client.models import Client, Platform


class AnalysisType(models.Model):
    ANALYSIS_TYPE = (
        ("sha", "Malware Cloud sha lookup"),
        ("url", "URL lookup"),
        ("android", "Android Lookup"),
        ("static", "Static Analysis"),
        ("Dynamic", "Dynamic Analysis"),
    )
    type = models.CharField(max_length=20)
    display_name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, blank=True)


class Query(models.Model):
    STATUS_CHOICES = (("active", "active"), ("inactive", "inactive"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.TextField()
    query_name = models.CharField(max_length=20, unique=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    clients = models.ManyToManyField(Client, blank=True)
    platforms = models.ManyToManyField(Platform, blank=True)
    all_host = models.NullBooleanField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

# Generated by Django 2.2.2 on 2019-06-27 14:18

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("localintel", "0001_initial"),
        ("query", "0007_auto_20190627_1418"),
        ("client", "0007_client_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiskOperations",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                )
            ],
        ),
        migrations.CreateModel(
            name="SocketConnection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("path", models.CharField(blank=True, max_length=256, null=True)),
                ("name", models.CharField(blank=True, max_length=56, null=True)),
                ("remote_address", models.GenericIPAddressField(blank=True, null=True)),
                ("remote_port", models.CharField(blank=True, max_length=10, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "action",
                    models.CharField(
                        blank=True,
                        choices=[("added", "added"), ("removed", "removed")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="client.Client"
                    ),
                ),
                (
                    "sha256",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="localintel.SHA",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Process",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pid", models.CharField(blank=True, max_length=256, null=True)),
                ("path", models.CharField(blank=True, max_length=256, null=True)),
                ("username", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "action",
                    models.CharField(
                        blank=True,
                        choices=[("added", "added"), ("removed", "removed")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "sha256",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="localintel.SHA",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventStream",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("couch_doc", models.CharField(max_length=40)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="client.Client"
                    ),
                ),
                (
                    "query",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="query.Query"
                    ),
                ),
            ],
        ),
    ]

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

# Generated by Django 2.2.2 on 2019-06-26 07:59

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("client", "0006_auto_20190626_0750")]

    operations = [
        migrations.CreateModel(
            name="Query",
            fields=[
                ("query", models.TextField()),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "active"), ("inactive", "inactive")],
                        default="active",
                        max_length=20,
                    ),
                ),
                ("all_host", models.BooleanField(null=True)),
                ("clients", models.ManyToManyField(to="client.Client")),
                ("platforms", models.ManyToManyField(to="client.Platform")),
            ],
        )
    ]

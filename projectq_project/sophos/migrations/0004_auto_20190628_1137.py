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

# Generated by Django 2.0.5 on 2019-06-28 11:37

import django.db.models.deletion
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("localintel", "0002_auto_20190627_1451"),
        ("sophos", "0003_sophostoken_validity_duration"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
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
                (
                    "analysis_type",
                    models.CharField(
                        blank=True,
                        choices=[("static", "static"), ("dynamic", "dynamic")],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("report", jsonfield.fields.JSONField()),
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
        migrations.AlterUniqueTogether(
            name="report", unique_together={("sha256", "analysis_type")}
        ),
    ]

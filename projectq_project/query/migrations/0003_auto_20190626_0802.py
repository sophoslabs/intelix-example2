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

# Generated by Django 2.2.2 on 2019-06-26 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("query", "0002_query_query_name")]

    operations = [
        migrations.AlterField(
            model_name="query",
            name="clients",
            field=models.ManyToManyField(null=True, to="client.Client"),
        ),
        migrations.AlterField(
            model_name="query",
            name="platforms",
            field=models.ManyToManyField(null=True, to="client.Platform"),
        ),
    ]

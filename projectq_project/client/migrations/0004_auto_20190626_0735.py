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

# Generated by Django 2.2.2 on 2019-06-26 07:35

from django.db import migrations


def add_platforms(apps, schema_editor):
    Platform = apps.get_model("client", "Platform")
    Platform.objects.bulk_create(
        [Platform(name="Linux"), Platform(name="Mac"), Platform(name="Windows")]
    )


class Migration(migrations.Migration):

    dependencies = [("client", "0003_auto_20190626_0742")]

    operations = [migrations.RunPython(add_platforms)]

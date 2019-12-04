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

from django.db import models


class SHA(models.Model):
    sha256 = models.CharField(max_length=64, primary_key=True, db_index=True)
    reputation_score = models.IntegerField(null=True, blank=True)
    detection_name = models.CharField(max_length=128, null=True, blank=True)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_lookup = models.DateTimeField(auto_now=True)


# class URI(models.Model):
#     domain = models.CharField(max_length=1024, db_index=True, )

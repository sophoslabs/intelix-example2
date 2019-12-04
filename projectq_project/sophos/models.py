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

import datetime

import jsonfield
from django.db import models
from django.utils import timezone

from localintel.models import SHA


class SophosToken(models.Model):
    """Singleton Django Model
    https://gist.github.com/senko/5028413

    Ensures there's always only one entry in the database, and can fix the
    table (by deleting extra entries) even if added via another mechanism.
    Also has a static load() method which always returns the object - from
    the database if possible, or a new empty (default) instance if the
    database is still empty. If your instance has sane defaults (recommended),
    you can use it immediately without worrying if it was saved to the
    database or not.
    Useful for things like system-wide user-editable settings.
    """

    token = models.TextField(primary_key=True)
    validity_duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    # class Meta:
    #     abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(token=self.token).delete()
        super(SophosToken, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    def is_expired(self):
        if self.created_at:
            return timezone.now() > self.created_at + datetime.timedelta(
                seconds=self.validity_duration - 10
            )
        else:
            return True


class Report(models.Model):
    ACTIONS_CHOICES = (("static", "static"), ("dynamic", "dynamic"))
    sha256 = models.ForeignKey(SHA, on_delete=models.CASCADE, null=True, blank=True)
    analysis_type = models.CharField(
        max_length=10, null=True, blank=True, choices=ACTIONS_CHOICES
    )
    report = jsonfield.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    job_id = models.CharField(max_length=90, null=True, blank=True, unique=True)

    class Meta:
        unique_together = ("sha256", "analysis_type")

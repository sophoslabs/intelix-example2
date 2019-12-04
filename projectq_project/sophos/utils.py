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
import logging
import time
import urllib.parse

import requests
from django.utils import timezone

from localintel.models import SHA
from projectq_project.settings import BASE64_CODE, PROXY
from sophos.models import SophosToken

logger = logging.getLogger(__name__)

proxy_dict = {"http": PROXY, "https": PROXY}


def get_auth():
    token = SophosToken.load()
    if token.is_expired():
        url = "https://api.labs.sophos.com/oauth2/token"
        headers = {
            "Authorization": f"Basic {BASE64_CODE}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        r = requests.post(
            url,
            headers=headers,
            data={"grant_type": "client_credentials"},
            proxies=proxy_dict,
        )
        if r.status_code == 200:
            access_token = r.json()["access_token"]
            expiration = r.json()["expires_in"]
            token = SophosToken.objects.create(
                token=access_token, validity_duration=expiration
            )
    return token.token


def get_conviction(score):
    score = int(score)
    if 0 <= score <= 19:
        return "malware"
    elif 20 <= score <= 29:
        return "pua"
    elif 30 <= score <= 69:
        return "unknown"
    elif 70 <= score <= 100:
        return "clean"


class SophosAPI:
    def __init__(self):
        self.url = "https://de.api.labs.sophos.com"
        self.headers = ""
        self._set_headers()

    def _call_api(self):
        raise NotImplementedError()

    def _set_headers(self):
        self.headers = {"Authorization": get_auth()}


class MalwareLookup(SophosAPI):
    def __init__(self, sha256, ip_addr=None):
        self.sha256 = sha256
        self.endpoint = "/lookup/files/v1/"
        super().__init__()
        self.score = ""
        self.detection_name = ""
        self.ip_addr = ip_addr
        self._local_lookup()

    def _call_api(self):
        r = requests.get(
            self.url + self.endpoint + self.sha256,
            headers=self.headers,
            proxies=proxy_dict,
        )
        if r.status_code == 200:
            self.score = r.json().get("reputationScore")
            self.detection_name = r.json().get("detectionName")

            # if self.score < 50:
            #     message = f"SHA256: <a href='http://35.176.243.153:8888/lookup/sample/?sha={self.sha256}'>{self.sha256}</a> is shaky for IP {self.ip_addr}"
            #     message_slack = f"SHA256: http://35.176.243.153:8888/lookup/sample/?sha={self.sha256} is shaky for IP {self.ip_addr}"
            #     notifier = Notification(message, ["teams"])
            #     notifier_slack = Notification(message_slack, ["slack"])
            #     notifier_slack.notify()
            #     notifier.notify()
        else:
            logger.critical(r.status_code)
            logger.critical(r.json())

    def _local_lookup(self):
        sha, created = SHA.objects.get_or_create(sha256=self.sha256)
        if created:
            self._call_api()
            sha.reputation_score = self.score
            sha.detection_name = self.detection_name
            sha.save()

        elif (
            sha.last_lookup
            and sha.reputation_score
            and (timezone.now() < sha.last_lookup + datetime.timedelta(days=90))
            and 80 >= int(sha.reputation_score) <= 20
        ):
            self.score = sha.reputation_score
            self.detection_name = sha.detection_name
        else:
            self._call_api()
            sha.reputation_score = self.score
            sha.detection_name = self.detection_name
            sha.save()


class URILookUp(SophosAPI):
    def __init__(self, uri):
        self.uri = urllib.parse.quote_plus(uri)
        self.endpoint = "/lookup/urls/v1/"
        super().__init__()
        self.risk_level = ""
        self.productivity_category = ""
        self.security_category = ""
        self._call_api()

    def _call_api(self):
        r = requests.get(
            self.url + self.endpoint + self.uri,
            headers=self.headers,
            proxies=proxy_dict,
        )
        if r.status_code == 200:
            self.productivity_category = r.json().get("productivityCategory")
            self.security_category = r.json().get("securityCategory")
            self.risk_level = r.json().get("riskLevel")
        else:
            logger.critical(r.status_code)
            logger.critical(r.json())

    def __str__(self):
        return f"{self.risk_level} - {self.security_category} - {self.productivity_category}"


class FileAnalysis(SophosAPI):
    def __init__(self, actual_file, analysis_type):
        self.endpoint = f"/analysis/file/{analysis_type}/v1"
        self.analysis_type = analysis_type
        super().__init__()
        self.file = actual_file
        self.response = self._call_api()

    def _call_api(self):
        r = requests.post(
            self.url + self.endpoint,
            headers=self.headers,
            proxies=proxy_dict,
            files={"file": self.file},
        )
        return r.json()

    def poll_report(self):
        if self.response.get("jobStatus") == "SUCCESS":
            return self.response
        elif self.response.get("jobStatus") == "IN_PROGRESS":
            job_id = self.response.get("jobId")
            report = GetReport(job_id, self.analysis_type)
            return report.response


class GetReport(SophosAPI):
    def __init__(self, job_id, analysis_type):
        self.job_id = job_id
        self.endpoint = f"/analysis/file/{analysis_type}/v1/reports/"
        super().__init__()
        self.max_wait_time_sec = 900
        self.poll_interval_sec = 5
        self.response = self._call_api()

    def _call_api(self):
        response = requests.get(
            self.url + self.endpoint + self.job_id,
            headers=self.headers,
            proxies=proxy_dict,
            timeout=self.max_wait_time_sec,
        )

        status = response.json().get("jobStatus")
        start_time = time.time()
        time_elapsed = 0

        while (
            status not in ["SUCCESS", "ERROR"]
            and time_elapsed <= self.max_wait_time_sec
        ):
            time.sleep(self.poll_interval_sec)
            response = requests.get(
                self.url + self.endpoint + self.job_id,
                headers=self.headers,
                proxies=proxy_dict,
                timeout=self.max_wait_time_sec,
            )
            status = response.json().get("jobStatus")
            time_elapsed = time.time() - start_time
        return response.json()

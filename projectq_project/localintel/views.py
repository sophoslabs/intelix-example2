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

import hashlib
import json

from django.shortcuts import render

from localintel.models import SHA
from sophos.models import Report
from sophos.utils import (
    MalwareLookup,
    get_conviction,
    URILookUp,
    FileAnalysis,
    GetReport,
)


def shalookup(request, sha=None):
    if request.method == "GET":
        sha = request.GET.get("sha")
        if sha:
            if len(sha) != 64:
                context = {"result": False, "error": "Please enter a valid sha256"}
                return render(request, "lookup/shalookup.html", context)

            else:
                sha_obj = MalwareLookup(sha)
                context = {
                    "result": True,
                    "sha": sha_obj.sha256,
                    "sha_score": sha_obj.score,
                    "sha_detection_name": sha_obj.detection_name,
                    "rating": get_conviction(sha_obj.score).upper(),
                }
        else:
            context = {"result": False}

        return render(request, "lookup/shalookup.html", context)


def uri_lookup(request, uri=None):
    if request.method == "GET":
        uri = request.GET.get("uri")
        if uri:
            uri_obj = URILookUp(uri)
            context = {
                "result": True,
                "url": uri,
                "productivity_category": uri_obj.productivity_category,
                "security_category": uri_obj.security_category,
                "risk_level": uri_obj.risk_level,
            }
        else:
            context = {"result": False}
        return render(request, "lookup/urilookup.html", context)


def analysis_lookup(request):
    context = {}
    if request.method == "POST" and request.FILES["sample"]:
        analysis_type = request.POST["analysis_type"]
        file_ = request.FILES["sample"]
        actual_file = file_.read()
        sha256 = hashlib.sha256(actual_file).hexdigest()
        # create SHA
        sha, _ = SHA.objects.get_or_create(sha256=sha256)

        # create Report entry
        report, _ = Report.objects.get_or_create(
            sha256=sha, analysis_type=analysis_type
        )
        file_analysis = FileAnalysis(actual_file, analysis_type)
        job_id = file_analysis.response.get("jobId")

        report.job_id = job_id
        if file_analysis.response.get("jobStatus") == "IN_PROGRESS":
            pass
        elif file_analysis.response.get("jobStatus") == "SUCCESS":
            job_report = file_analysis.response.get("report")
            if job_report:
                score = job_report.get("score")
                if score:
                    sha.reputation_score = score
                    detection_name = job_report.get("detection")
                    if detection_name:
                        detection_name = detection_name.get("sophos")
                    if detection_name:
                        sha.detection_name = detection_name
                    sha.save()
                    context["score"] = score
                    context["detection_name"] = detection_name
            if not context:
                context = {"report": job_report}
            else:
                context["report"] = job_report
        else:
            pass
        report.report = file_analysis.response
        report.save()

        context["status"] = file_analysis.response.get("jobStatus")
        context["job_id"] = file_analysis.response.get("jobId", None)

    # get all recent 20 jobs
    reports = (
        Report.objects.all()
        .order_by("-updated_at")
        .values(
            "sha256__sha256",
            "sha256__reputation_score",
            "sha256__detection_name",
            "analysis_type",
            "job_id",
            "report",
        )
    )
    if reports.count() > 20:
        reports = (
            Report.objects.all()
            .order_by("-updated_at")
            .values(
                "sha256__sha256",
                "sha256__reputation_score",
                "sha256__detection_name",
                "analysis_type",
                "job_id",
                "report",
            )[:20]
        )

    for report in reports:
        r = json.loads(report["report"])
        if r == {}:
            status = "IN_PROGRESS"
        elif "message" in r:
            status = r["message"]
        else:
            status = r["jobStatus"]
        report["status"] = status

    context["reports"] = reports
    return render(request, "lookup/analysis.html", context=context)


def get_report(request, job_id):
    context = {}
    if request.method == "GET":
        # call report
        reports = Report.objects.filter(job_id=job_id)
        if reports.count() and reports.count() == 1:
            analysis_type = reports[0].analysis_type
            analysed_report = GetReport(job_id, analysis_type)
            sha, _ = SHA.objects.get_or_create(sha256=reports[0].sha256.sha256)

            job_id = analysed_report.response.get("jobId")
            context["job_id"] = job_id

            analysed_report.job_id = job_id
            context["status"] = analysed_report.response.get("jobStatus")

            if analysed_report.response.get("jobStatus") == "IN_PROGRESS":
                pass
            elif analysed_report.response.get("jobStatus") == "SUCCESS":
                job_report = analysed_report.response.get("report")
                if job_report:
                    score = job_report.get("score")
                    if score == 0 or score:
                        sha.reputation_score = score
                        detection_name = job_report.get("detection")
                        if detection_name:
                            detection_name = detection_name.get("sophos")
                        if detection_name:
                            sha.detection_name = detection_name
                        sha.save()
                        context["score"] = score
                        if score:
                            context["rating"] = get_conviction(score).upper()
                        context["detection_name"] = detection_name
                if not context:
                    context = {"report": job_report}
                else:
                    context["report"] = job_report
            else:
                pass
            for report in reports:
                report.report = analysed_report.response
                report.save()

            if job_id:
                report = (
                    Report.objects.filter(job_id=job_id)
                    .order_by("-updated_at")
                    .values(
                        "sha256__sha256",
                        "sha256__reputation_score",
                        "sha256__detection_name",
                        "analysis_type",
                        "report",
                    )
                )
                context["report"] = report[0]
        else:
            context["error"] = "job not found"
            return render(request, "lookup/report.html", context=context)
        return render(request, "lookup/report.html", context=context)

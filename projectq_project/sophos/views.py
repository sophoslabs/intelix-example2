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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report
from .utils import FileAnalysis


# Create your views here.
class SubmitFile(APIView):
    def post(self, request):
        file_content = request.body
        sha256 = hashlib.sha256(request.body).hexdigest()
        report = Report.objects.get(SHA__sha256=sha256)
        analysis_type = report.analysis_type
        if not analysis_type:
            analysis_type = "static"
        analysis_obj = FileAnalysis(file_content, analysis_type)
        report.report = analysis_obj.response
        report.save()
        response_data = {"data": "File Submitted"}
        return Response(
            response_data,
            headers={"Content-Type": "application/json"},
            status=status.HTTP_201_CREATED,
        )

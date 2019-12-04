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

from django.urls import path

import localintel.views

urlpatterns = [
    path("sample/", localintel.views.shalookup, name="sha_lookup"),
    path("sample/<str:sha>/", localintel.views.shalookup, name="sha_lookup"),
    path("uri/", localintel.views.uri_lookup, name="uri_lookup"),
    path("uri/<str:uri>", localintel.views.uri_lookup, name="uri_lookup"),
    path("analysis/", localintel.views.analysis_lookup, name="analysis_lookup"),
    path(
        "analysis/report/<str:job_id>",
        localintel.views.get_report,
        name="analysis_lookup",
    ),
    # path('lookup/sample/<str:sha>', client.views.list_clients,
    #      name='sha_lookup'),
]

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

from django.shortcuts import render

from client.models import Client
from event.utils import get_events_days, get_malicious_events, get_total_events


def home_page(request):
    if request.user.is_authenticated:
        # Event statistics by days
        socket_events, socket_dates = get_events_days(days=7)
        # socket_total = 0
        # for event in socket_events:
        socket_total = sum(socket_events)
        mal_events = get_malicious_events(days=7)
        mal_today = get_malicious_events(days=1)
        total_today = get_total_events(days=1)


        statistics_green_color = "#2BB930"
        statistics_orange_color = "#FF9E27"
        statistics_red_color = "#F25961"

        context = {
            "statistics": {
                "clients": {
                    "clients": Client.objects.filter(status="active").count(),
                    "color": statistics_green_color,
                },
                "samples": {
                    "total": total_today,
                    "malware": mal_today,
                    "color": statistics_orange_color,
                },
                "uri": {"total": 800, "malware": 420, "color": statistics_red_color},
                "event_statistics_days": {
                    "dates": socket_dates,
                    "events": socket_events,
                    "total_events": socket_total,
                    "mal_events": mal_events,
                    # "today_malware": mal_today,
                },
            }
        }
        return render(request, "ui/index.html", context=context)
    else:
        return render(request, "login/login.html")

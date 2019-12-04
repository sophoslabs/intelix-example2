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

from datetime import timedelta

from django.utils.datetime_safe import datetime

from event.models import SocketConnection


def get_events_days(days):
    socket_events = []
    dates = []
    for day in range(days, 0, -1):
        latest_date = datetime.now() - timedelta(days=day - 1)
        former_date = datetime.now() - timedelta(days=day)
        socket_event = SocketConnection.objects.filter(
            created_at__lte=latest_date.date(), created_at__gt=former_date.date()
        ).count()
        if not socket_event:
            socket_event = 1
        socket_events.append(socket_event)
        date_ = latest_date.strftime("%d %b")
        dates.append(date_)
    return socket_events, dates


def get_malicious_events(days):
    latest_date = datetime.now() - timedelta(days=0)
    former_date = datetime.now() - timedelta(days=days)
    mal_count = SocketConnection.objects.filter(
        created_at__lte=latest_date.date(),
        created_at__gt=former_date.date(),
        sha256__reputation_score__lte=20,
    ).count()

    if mal_count:
        return mal_count
    else:
        return 1


def get_total_events(days):
    latest_date = datetime.now() - timedelta(days=0)
    former_date = datetime.now() - timedelta(days=days)
    total_today = SocketConnection.objects.filter(
        created_at__lte=latest_date.date(), created_at__gt=former_date.date()
    ).count()
    if total_today:
        return total_today
    else:
        return 1

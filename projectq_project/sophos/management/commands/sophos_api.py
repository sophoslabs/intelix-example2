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

from django.core.management.base import BaseCommand

from sophos.utils import (
    MalwareLookup,
    get_conviction,
)


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        lookup = MalwareLookup(
            "74e135349aca525b39219e6260e371065f2d0da625cebf54cbc258e5fc89c2bb"
        )

        # lookup2 = URILookUp('https://google.com')
        self.stdout.write(
            self.style.SUCCESS(
                f"{get_conviction(lookup.score)},{lookup.detection_name}"
            )
        )
        # self.stdout.write(self.style.SUCCESS(f"{lookup2}"))

        # report = GetReport('c81e4658395cbcf004f856adcf2828c4', "static")

        # analysis = FileAnalysis("<file_path>", "dynamic")
        # response = analysis.poll_report()

import hashlib
import io
import json
import os.path

from django.db.models import Prefetch
from django.core.management.base import BaseCommand
from core.models import MemberOfParliament, MP2Convocation, Minion2MP2Convocation


class Command(BaseCommand):
    help = "Export all data in JSON Lines format, centered around MPs with nested convocations and minions"

    def add_arguments(self, parser):
        parser.add_argument(
            "output", type=str, help="Output file path for the JSON Lines export"
        )

    def handle(self, *args, **options):
        output_path = options["output"]

        mps = MemberOfParliament.objects.prefetch_related(
            Prefetch(
                "mp2convocation_set",
                queryset=MP2Convocation.objects.select_related("convocation").order_by(
                    "convocation__number"
                ),
            ),
            Prefetch(
                "mp2convocation_set__minion2mp2convocation_set",
                queryset=Minion2MP2Convocation.objects.select_related("minion").order_by(
                    "minion__name", "minion_id"
                ),
            ),
        ).order_by("id")

        exported_count = 0
        buf = io.StringIO()

        for mp in mps:
            mp_data = {
                "mp": {
                    "id": mp.id,
                    "name": mp.name,
                    "link": mp.link,
                    "img": mp.img.name if mp.img else None,
                },
                "convocations": [],
            }

            for mp2conv in mp.mp2convocation_set.all():
                convocation_data = {
                    "convocation": mp2conv.convocation.number,
                    "party": mp2conv.party,
                    "district": mp2conv.district,
                    "date_from": (
                        mp2conv.date_from.isoformat() if mp2conv.date_from else None
                    ),
                    "date_to": (
                        mp2conv.date_to.isoformat() if mp2conv.date_to else None
                    ),
                    "link": mp2conv.link,
                    "minions": [],
                }

                for minion2mp in mp2conv.minion2mp2convocation_set.all():
                    minion_data = {
                        "id": minion2mp.minion.id,
                        "name": minion2mp.minion.name,
                        "paid": minion2mp.paid,
                    }
                    convocation_data["minions"].append(minion_data)

                mp_data["convocations"].append(convocation_data)

            buf.write(json.dumps(mp_data, ensure_ascii=False) + "\n")
            exported_count += 1

        new_bytes = buf.getvalue().encode("utf-8")
        new_hash = hashlib.sha256(new_bytes).hexdigest()

        existing_hash = None
        if os.path.exists(output_path):
            with open(output_path, "rb") as f:
                existing_hash = hashlib.sha256(f.read()).hexdigest()

        if new_hash == existing_hash:
            self.stdout.write(
                f"No changes ({exported_count} MPs); {output_path} left untouched"
            )
            return

        with open(output_path, "wb") as f:
            f.write(new_bytes)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully exported {exported_count} MPs to {output_path}"
            )
        )

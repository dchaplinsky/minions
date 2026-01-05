import json
from django.core.management.base import BaseCommand
from core.models import MemberOfParliament


class Command(BaseCommand):
    help = "Export all data in JSON Lines format, centered around MPs with nested convocations and minions"

    def add_arguments(self, parser):
        parser.add_argument(
            "output", type=str, help="Output file path for the JSON Lines export"
        )

    def handle(self, *args, **options):
        output_path = options["output"]

        mps = MemberOfParliament.objects.prefetch_related(
            "mp2convocation_set__minion2mp2convocation_set__minion"
        ).order_by("id")

        exported_count = 0

        with open(output_path, "w", encoding="utf-8") as f:
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

                # Get all convocations for this MP
                for mp2conv in mp.mp2convocation_set.order_by(
                    "convocation__number"
                ).all():
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

                    # Get all minions for this MP in this convocation
                    for minion2mp in mp2conv.minion2mp2convocation_set.select_related(
                        "minion"
                    ).all():
                        minion_data = {
                            "id": minion2mp.minion.id,
                            "name": minion2mp.minion.name,
                            "paid": minion2mp.paid,
                        }
                        convocation_data["minions"].append(minion_data)

                    mp_data["convocations"].append(convocation_data)

                # Write as a single line in JSON Lines format
                f.write(json.dumps(mp_data, ensure_ascii=False) + "\n")
                exported_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully exported {exported_count} MPs to {output_path}"
            )
        )

from django.core.management.base import BaseCommand
from multiprocessing import Pool
from faker import Faker
from time import time
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import requests
from io import BytesIO
from django.core.files.images import ImageFile
from utils.base_utils import get_model
import random

User = get_model("accounts", "User")
Lottery = get_model("rewards", "Lottery")
fake = Faker()


def create_lottery(vendor):
    with transaction.atomic():
        response = requests.get("https://picsum.photos/512/512")
        response.raise_for_status()

        image_file = ImageFile(BytesIO(response.content), name=f"{fake.slug()}.jpg")

        lottery = Lottery(
            title=fake.sentence(),
            description=fake.text(),
            vendor=vendor,
            price=fake.pydecimal(left_digits=2, right_digits=2, positive=True),
            total_draw=fake.random_int(1, 10),
            winning=fake.pydecimal(left_digits=3, right_digits=2, positive=True),
            expiry_date=timezone.now() + timedelta(hours=random.randint(10, 40)),
            image=image_file,
        )
        lottery.save()
        print(lottery)


class Command(BaseCommand):
    help = "Create Fake Lottery Data"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, nargs="?", default=1)

    def handle(self, *args, **options):
        try:
            start = time()
            vendors = User.objects.filter(option="Vender")
            for _ in range(options["count"]):
                with Pool(processes=8) as pool:
                    pool.map(create_lottery, vendors)
            end = time()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Lotteries Created Successfully in {end - start:.6f}"
                )
            )
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Unknown Exception Occured: {err}"))

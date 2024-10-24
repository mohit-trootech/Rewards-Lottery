from django.core.management.base import BaseCommand
from multiprocessing import Pool
from faker import Faker
from django.contrib.auth import get_user_model
from time import time
from django.db import transaction

model = get_user_model()
fake = Faker()


def create_user(username):
    with transaction.atomic():
        user = model(
            username=username,
            # email="mohit.prajapat@trootech.com",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        user.set_password("password")
        user.save()


class Command(BaseCommand):
    help = "Create Fake User Data"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, nargs="?", default=1)

    def handle(self, *args, **options):
        try:
            start = time()
            usernames = set()
            for _ in range(options["count"]):
                username = fake.user_name()
                while username in usernames:
                    username = fake.user_name()
                usernames.add(username)

            # Use a Pool to limit the number of parallel processes
            with Pool(processes=8) as pool:
                pool.map(create_user, usernames)

            end = time()
            self.stdout.write(
                self.style.SUCCESS(f"User Created Successfully in {end - start:.6f}")
            )
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Unknown Exception Occured: {err}"))

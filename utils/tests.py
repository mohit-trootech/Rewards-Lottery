from faker import Faker
from django.test import TestCase
from utils.constants import Choices
from django.utils.timezone import now
from utils.base_utils import get_model

User = get_model("accounts", "User")
Lottery = get_model("rewards", "Lottery")
fake = Faker()


def fake_indian_phone_number():
    return "+91{number}".format(number=fake.msisdn()[3:])


class BaseTest(TestCase):
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    age = fake.random_int(min=18, max=99)
    phone = fake_indian_phone_number()
    gender = fake.random_element([Choices.MALE.value, Choices.FEMALE.value])
    address = fake.address()
    option = fake.random_element([Choices.VENDER.value, Choices.CUSTOMER.value])
    transaction_type = fake.random_element([Choices.DEBIT.value, Choices.CREDIT.value])
    amount = fake.pydecimal(left_digits=5, right_digits=2)
    title = fake.sentence()
    description = fake.text()
    draw = fake.random_int(1, 10)
    expiry = now()

    def create_user(self):
        """create user instance"""
        return User.objects.create(
            username=self.username,
            email=self.email,
            password=self.password,
            option=self.option,
        )


class BuyerWinnerBaseTest(BaseTest):
    """Buyer Winner Abstract Base Model Test Case"""

    lottery = None
    user = None

    def create_lottery(self):
        """create lottery instance"""
        return Lottery.objects.create(
            title=self.title,
            description=self.description,
            vendor=self.user,
            price=self.amount,
            total_draw=self.draw,
            winning=self.amount * 10,
            expiry_date=self.expiry,
        )

    def setUp(self):
        self.user = self.create_user()
        self.lottery = self.create_lottery()
        return super().setUp()

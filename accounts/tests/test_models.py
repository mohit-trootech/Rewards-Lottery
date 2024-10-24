from utils.base_utils import get_model
from utils.tests import BaseTest

User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")


class UserTest(BaseTest):
    """Test User Model"""

    def create_user(self):
        """Create a user instance"""
        return User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            age=self.age,
            phone=self.phone,
            gender=self.gender,
            address=self.address,
            option=self.option,
        )

    def test_user_creation(self):
        """Test user creation"""
        user = self.create_user()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.age, self.age)
        self.assertEqual(user.phone, self.phone)
        self.assertEqual(user.gender, self.gender)
        self.assertEqual(user.address, self.address)
        self.assertEqual(user.option, self.option)

    def test_user_str(self):
        """Test user string representation"""
        user = self.create_user()
        self.assertEqual(str(user), user.username)


class WalletTest(BaseTest):
    """Test Wallet Model"""

    def create_wallet(self):
        """Create a wallet instance"""
        user = self.create_user()
        return Wallet.objects.get(user=user)

    def test_wallet_creation(self):
        """Test wallet creation"""
        wallet = self.create_wallet()
        self.assertIsInstance(wallet, Wallet)
        self.assertEqual(wallet.user.username, self.username)
        self.assertEqual(wallet.balance, 0)

    def test_wallet_str(self):
        """Test wallet string representation"""
        wallet = self.create_wallet()
        self.assertEqual(
            str(wallet), f"{wallet.user.username}'s Wallet: {wallet.balance}"
        )


class TransactionTest(BaseTest):
    """Test Transaction Model"""

    def create_transaction(self):
        """Create a transaction instance"""
        user = self.create_user()
        return Transaction.objects.create(
            user=user,
            amount=self.amount,
            option=self.transaction_type,
            description=self.description,
        )

    def test_transaction_creation(self):
        """Test transaction creation"""
        transaction = self.create_transaction()
        self.assertIsInstance(transaction, Transaction)
        self.assertEqual(transaction.user.username, self.username)
        self.assertEqual(transaction.amount, self.amount)
        self.assertEqual(transaction.option, self.transaction_type)
        self.assertEqual(transaction.description, self.description)

    def test_transaction_str(self):
        """Test transaction string representation"""
        transaction = self.create_transaction()
        self.assertEqual(
            str(transaction),
            f"{transaction.amount} {transaction.option} {transaction.description}",
        )

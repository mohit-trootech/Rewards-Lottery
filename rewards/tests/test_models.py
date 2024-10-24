from utils.base_utils import get_model
from utils.tests import BaseTest, BuyerWinnerBaseTest


User = get_model("accounts", "User")
Wallet = get_model("accounts", "Wallet")
Transaction = get_model("accounts", "Transaction")
Lottery = get_model("rewards", "Lottery")
Winner = get_model("rewards", "Winner")
Buyer = get_model("rewards", "Buyer")
LotteryCash = get_model("rewards", "LotteryCash")


class LotteryTest(BaseTest):
    """Lottery Models Test Case"""

    user = None
    lottery = None

    def create_lottery(self):
        """create lottery instance"""
        self.user = self.create_user()
        self.lottery = Lottery.objects.create(
            title=self.title,
            description=self.description,
            vendor=self.user,
            price=self.amount,
            total_draw=self.draw,
            winning=self.amount * 10,
            expiry_date=self.expiry,
        )
        return self.lottery

    def get_lottery_cash(self):
        """get lottery cash instance"""
        lottery = self.create_lottery()
        return LotteryCash.objects.get(lottery=lottery)

    def test_lottery_creation(self):
        """test lottery creation"""
        lottery = self.create_lottery()
        self.assertIsInstance(lottery, Lottery)
        self.assertEqual(lottery.title, self.title)
        self.assertEqual(lottery.description, self.description)
        self.assertEqual(lottery.vendor, self.user)
        self.assertEqual(lottery.vendor.option, self.user.option)
        self.assertEqual(lottery.price, self.amount)
        self.assertEqual(lottery.total_draw, self.draw)
        self.assertEqual(lottery.winning, self.amount * 10)
        self.assertEqual(lottery.expiry_date, self.expiry)

    def test_lottery_cash_creation(self):
        """test lottery_cash creation"""
        lottery_cash = self.get_lottery_cash()
        self.assertIsInstance(lottery_cash, LotteryCash)
        self.assertEqual(lottery_cash.amount, 0)
        self.assertEqual(lottery_cash.lottery, self.lottery)

    def test_lottery_str(self):
        """test lottery string representation"""
        lottery = self.create_lottery()
        self.assertEqual(str(lottery), lottery.slug)

    def test_lottery_cash_str(self):
        """test lottery_cash string representation"""
        lottery_cash = self.get_lottery_cash()
        self.assertEqual(
            str(lottery_cash), f"{lottery_cash.amount} in {lottery_cash.lottery}"
        )


class BuyerTest(BuyerWinnerBaseTest):
    """Buyer Models Tests Case"""

    def create_buyer(self):
        """create buyer instance"""
        buyer = Buyer.objects.create(
            user=self.user,
            lottery=self.lottery,
            amount=self.amount,
        )
        return buyer

    def test_buyer_creation(self):
        """Test Buyer Creation"""
        buyer = self.create_buyer()
        self.assertIsInstance(buyer, Buyer)
        self.assertEqual(buyer.user, self.user)
        self.assertEqual(buyer.lottery, self.lottery)
        self.assertEqual(buyer.amount, self.amount)

    def test_buyer_str(self):
        """Test Buyer String Representation"""
        buyer = self.create_buyer()
        self.assertEqual(
            str(buyer), f"{buyer.user} bought {buyer.amount} in {buyer.lottery}"
        )


class WinnerTest(BuyerWinnerBaseTest):
    """Winner Model Test Case"""

    def create_winner(self):
        """create winner instance"""
        return Winner.objects.create(
            user=self.user,
            lottery=self.lottery,
            amount=self.amount,
        )

    def test_winner_creation(self):
        """test winner creation"""
        winner = self.create_winner()
        self.assertIsInstance(winner, Winner)
        self.assertEqual(winner.user, self.user)
        self.assertEqual(winner.lottery, self.lottery)
        self.assertEqual(winner.amount, self.amount)

    def test_winner_str(self):
        """test winner string representation"""
        winner = self.create_winner()
        self.assertEqual(
            str(winner), f"{winner.user} won {winner.amount} in {winner.lottery}"
        )

from datetime import datetime
import pytest

from src.parser import Transaction


class TestTransaction:
    def test_ctor_basicTransaction_withoutForeignCurrency(self):
        # act
        testee = Transaction(
            category="Essen & Trinken",
            merchant="Restaurant ABC",
            date=datetime(2025, 7, 31),
            time="12:30",
            location="Zürich",
            amount=25.50
        )

        # assert
        assert testee.category == "Essen & Trinken"
        assert testee.merchant == "Restaurant ABC"
        assert testee.date == datetime(2025, 7, 31)
        assert testee.time == "12:30"
        assert testee.location == "Zürich"
        assert testee.amount == 25.50
        assert testee.foreignAmount is None
        assert testee.foreignCurrency is None

    def test_ctor_transactionWithForeignCurrency_withForeignCurrency(self):
        # act
        testee = Transaction(
            category="Shopping",
            merchant="Amazon.de",
            date=datetime(2025, 7, 22),
            time="20:05",
            location=None,
            amount=285.05,
            foreignAmount=297.00,
            foreignCurrency="EUR"
        )

        # assert
        assert testee.amount == 285.05
        assert testee.foreignAmount == 297.00
        assert testee.foreignCurrency == "EUR"
        assert testee.hasForeignCurrency is True

    def test_ctor_transactionWithoutOptional_withoutOptionalFieldsAndForeignCurrency(self):
        # act
        testee = Transaction(
            category="Essen & Trinken",
            merchant="Café",
            date=datetime(2025, 7, 28),
            time=None,
            location=None,
            amount=10.00
        )

        # assert
        assert testee.time is None
        assert testee.location is None
        assert testee.hasForeignCurrency is False

    def test_ctor_transactionWithMerchant_Description(self):
        # act
        testee = Transaction(
            category="Essen & Trinken",
            merchant="My Lunch Place",
            date=datetime(2025, 7, 31),
            time="13:14",
            location="Olten",
            amount=4.30
        )

        # assert
        assert testee.description == "My Lunch Place"

    def test_ctor_payment_negativeAmount(self):
        # act
        testee = Transaction(
            category="Einlagen",
            merchant="Ihre Zahlung - Danke",
            date=datetime(2025, 7, 22),
            time=None,
            location=None,
            amount=-157.95
        )

        # assert
        assert testee.amount == -157.95

    def test_ctor_zeroAmount_error(self):
        with pytest.raises(ValueError, match="amount cannot be zero"):
            Transaction(
                category="Test",
                merchant="Test",
                date=datetime(2025, 7, 31),
                time=None,
                location=None,
                amount=0.0
            )

    def test_ctor_foreignAmountWithoutCurrency_error(self):
        """Test that foreign amount without currency raises error."""
        with pytest.raises(
            ValueError,
            match="Foreign currency must be specified"
        ):
            Transaction(
                category="Shopping",
                merchant="Shop",
                date=datetime(2025, 7, 22),
                time=None,
                location=None,
                amount=100.00,
                foreignAmount=105.00,
                foreignCurrency=None
            )

    def test_ctor_transaction_stringified(self):
        # act
        testee = Transaction(
            category="Essen & Trinken",
            merchant="Restaurant",
            date=datetime(2025, 7, 31),
            time="12:30",
            location="Zürich",
            amount=25.50,
            foreignAmount=27.00,
            foreignCurrency="EUR"
        )

        # assert
        reprStr = repr(testee)
        assert "category='Essen & Trinken'" in reprStr
        assert "merchant='Restaurant'" in reprStr
        assert "31.07.2025" in reprStr
        assert "12:30" in reprStr
        assert "Zürich" in reprStr
        assert "amountChf=25.5" in reprStr
        assert "EUR 27.0" in reprStr

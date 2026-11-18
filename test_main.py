
from pathlib import Path
from tempfile import TemporaryDirectory

from main import (
    AddressBook,
    Record,
    load_data,
    save_data,
)


def test_persistence():
    with TemporaryDirectory() as folder:
        filename = str(Path(folder) / "test_addressbook.pkl")

        # First launch: no saved file
        book = load_data(filename)
        assert isinstance(book, AddressBook)
        assert len(book.data) == 0

        # Add contacts
        john = Record("John")
        john.add_phone("1234567890")
        john.add_phone("5555555555")
        john.add_birthday("15.05.1990")
        book.add_record(john)

        jane = Record("Jane")
        jane.add_phone("9876543210")
        book.add_record(jane)

        # Save address book
        save_data(book, filename)
        assert Path(filename).exists()

        # Simulate a new application session
        restored_book = load_data(filename)

        # Verify restored contacts
        assert len(restored_book.data) == 2
        assert restored_book.find("John") is not None
        assert restored_book.find("Jane") is not None

        # Verify restored phones
        restored_john = restored_book.find("John")

        assert len(restored_john.phones) == 2
        assert restored_john.find_phone("1234567890") is not None
        assert restored_john.find_phone("5555555555") is not None

        # Verify restored birthday
        assert str(restored_john.birthday) == "15.05.1990"

        # Verify editing and saving again
        restored_john.edit_phone(
            "1234567890",
            "1112223333"
        )

        save_data(restored_book, filename)
        final_book = load_data(filename)

        assert (
            final_book.find("John")
            .find_phone("1112223333") is not None
        )

        print("All persistence tests passed!")


if __name__ == "__main__":
    test_persistence()

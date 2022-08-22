"""
Test file for the core of the memory store
"""
import unittest
from core import MemoryStore

class TestCRUD(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        # Initialize system under test
        self.sut = MemoryStore()

    def test_basic_set(self):
        # Should be able to set a key
        self.sut.set("test_1", 0)
        self.assertEqual(0, self.sut.state["test_1"])

    def test_set_twice(self):
        # Should be able to override a key
        self.sut.set("test_2", 0)
        self.sut.set("test_2", 1)
        self.assertEqual(1, self.sut.state["test_2"])

    def test_basic_get(self):
        # Should be able to get a key through the getter method
        self.sut.set("test_3", "Test")
        self.assertEqual("Test", self.sut.get("test_3"))

    def test_error_on_key_error(self):
        # Should get an error when a key is not present
        self.assertRaises(KeyError, lambda : self.sut.get("test_4"))

    def test_unset(self):
        # Should be able to unset a key
        # First set and check it is there
        self.sut.set("test_5", "somevalue")
        self.assertEqual("somevalue", self.sut.get("test_5"))
        # Now remove it
        self.sut.unset("test_5")
        # And we should raise an error here
        self.assertRaises(KeyError, lambda : self.sut.get("test_5"))
        self.assertNotIn("test_5", self.sut.state)


class TestAnalysis(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        # Initialize system under test
        self.sut = MemoryStore()

        # Fill the store with some basic data
        self.sut.set("Key1", 1)
        self.sut.set("Key2", "test")
        self.sut.set("Key3", 1.00000001)
        self.sut.set("Key4", True)
        self.sut.set("Key5", 1)

    def test_count_correctly(self):
        # Test whether the store counts the values correctly
        self.assertEqual(2, self.sut.count_equal_to(1))
        self.assertEqual(1, self.sut.count_equal_to("test"))
        self.assertEqual(1, self.sut.count_equal_to(1.00000001))
        self.assertEqual(1, self.sut.count_equal_to(True))
        self.assertEqual(0, self.sut.count_equal_to("NoneExistent"))


class TestTransactions(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        # Initialize system under test
        self.sut = MemoryStore()

        # Fill the store with some basic data
        self.sut.set("Key1", "test1")
        self.sut.set("Key2", "test2")
        self.sut.set("Key3", "test3")

    def test_transaction_commit(self):
        # Test whether a commit modifies the state
        self.sut.start_transaction()

        self.sut.set("Key2", "test_modified")
        self.sut.set("NewKey", "test_new")

        # Test correct value within transaction
        self.assertEqual("test_modified", self.sut.get('Key2'))
        self.assertEqual("test_new", self.sut.get('NewKey'))

        self.sut.commit_transaction()

        # Test correct value after transaction
        self.assertEqual("test_modified", self.sut.get('Key2'))
        self.assertEqual("test_new", self.sut.get('NewKey'))

    def test_transaction_rollback(self):
        # Test whether a rollback reverts the state to before the start of
        # the transaction
        self.sut.start_transaction()

        self.sut.set("Key2", "test_modified")
        self.sut.set("NewKey", "test_new")

        # Test correct value within transaction
        self.assertEqual("test_modified", self.sut.get('Key2'))
        self.assertEqual("test_new", self.sut.get('NewKey'))

        self.sut.rollback_transaction()

        # Test correct value after rollback
        self.assertEqual("test2", self.sut.get('Key2'))
        self.assertRaises(KeyError, lambda : self.sut.get('NewKey'))

    def test_cannot_rollback_committed_transaction(self):
        # Should not be able to rollback a transaction that is already committed
        self.sut.start_transaction()
        self.sut.set('Key2', "test_modified")
        self.sut.commit_transaction()

        # This should raise and the state should be as modified in the transaction
        self.assertRaises(RuntimeError, lambda : self.sut.rollback_transaction())
        self.assertEqual("test_modified", self.sut.get('Key2'))

    def test_cannot_commit_rollbacked_transaction(self):
        # Should not be able to commit a transaction that is has been rollbacked
        self.sut.start_transaction()
        self.sut.set('Key2', "test_modified")
        self.sut.rollback_transaction()

        # This should raise and the state should not be modified by the transaction
        self.assertRaises(RuntimeError, lambda : self.sut.commit_transaction())
        self.assertEqual("test2", self.sut.get('Key2'))

"""
This file implements the requested key value store
"""

class MemoryStore:
    """Key value store
    """
    def __init__(self) -> None:
        self.state = {}
        self.state_before_transaction = None

    def set(self, key: str, value: str | int | float | bool):
        """Sets a key in the memory store with the given value

        Args:
            key (str): The key to set in the store
            value (str | int | float | bool): The value to set
        """
        self.state[key] = value

    def get(self, key: str) -> str | int | float | bool:
        """Gets the value that is set at the provided key

        Args:
            key (str): The key to retrieve

        Raises:
            KeyError: Thrown when the key does not exist

        Returns:
            str | int | float | bool: The value currently stored at the key
        """
        if key not in self.state:
            raise KeyError(f"Could not find \"{key}\" in the memory store")

        return self.state[key]

    def unset(self, key: str):
        """Unset the given key by completely removing it from the state

        Args:
            key (str): The key to remove

        Raises:
            KeyError: When the key is not present
        """
        if key not in self.state:
            raise KeyError(f"Could not find \"{key}\" in the memory store")

        del self.state[key]

    def count_equal_to(self, value: str | int | float | bool) -> int:
        """Count the number of keys with the given value. This operation
        iterates over all the values and is O(N) in complexity. Higher performance
        could be obtained by adding a reverse dict, but this complicates the
        implementation. This can be an engineering decision

        Args:
            value (str | int | float | bool): The value to count

        Returns:
            int: The number of occurences
        """
        count = 0

        for (_, iteration_value) in self.state.items():
            if type(iteration_value) == type(value) and iteration_value == value:
                count += 1

        return count

    def start_transaction(self):
        """Start a new transaction. Multiple transactions are not supported.

        Raises:
            RuntimeError: Raised when a transaction is already running
        """
        if self.state_before_transaction is not None:
            raise RuntimeError("A transaction is already running")

        self.state_before_transaction = self.state.copy()

    def rollback_transaction(self):
        """Rollback the current transaction

        Raises:
            RuntimeError: Raised when there is no transaction ongoing
        """
        if self.state_before_transaction is None:
            raise RuntimeError("There is no transaction to rollback")

        self.state = self.state_before_transaction
        self.state_before_transaction = None

    def commit_transaction(self):
        """Commit the current transaction

        Raises:
            RuntimeError: Raised when there is not transaction ongoing
        """
        if self.state_before_transaction is None:
            raise RuntimeError("There is no transaction to commit")

        self.state_before_transaction = None

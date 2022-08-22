"""
This file contains the main CLI for the memory key store

Requires python version 10 to run
"""
from core import MemoryStore

def handle_input(cli_input: str, store: MemoryStore) -> bool:
    """Helper function to handle the command line input

    Args:
        cli_input (str): The cli input string
        store (MemoryStore): The memory store to act on

    Returns:
        bool: Whether the terminal should accept a new command
    """
    command, *args = cli_input.split()

    match command.upper():
        case "END":
            return False
        case "SET":
            if len(args) != 2:
                print("error: Expected two arguments: key, value")
                return True
            store.set(args[0], args[1])

        case "UNSET":
            if len(args) != 1:
                print("error: Expected one argument: key")
                return True
            try:
                store.unset(args[0])
            except KeyError:
                return True

        case "GET":
            if len(args) != 1:
                print("error: Expected one argument: key")
                return True
            try:
                print(store.get(args[0]))
            except KeyError:
                print("NULL")

        case "NUMEQUALTO":
            if len(args) != 1:
                print("error: Expected one argument: value")
                return True
            print(store.count_equal_to(args[0]))

        case "BEGIN":
            try:
                store.start_transaction()
            except RuntimeError:
                print("error: Transaction in progress")

        case "ROLLBACK":
            try:
                store.rollback_transaction()
            except RuntimeError:
                print("error: No transaction")

        case "COMMIT":
            try:
                store.commit_transaction()
            except RuntimeError:
                print("error: No transaction")

        case _:
            print("error")
    return True




def main():
    """
    Main function to scope variables
    """
    store = MemoryStore()

    while True:
        cli_input = input("> ")
        if not handle_input(cli_input, store):
            break

if __name__ == "__main__":
    main()

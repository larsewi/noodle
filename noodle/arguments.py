import argparse
import commands


def parse_args():
    parser = argparse.ArgumentParser(description="Simple secret management")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug messages",
    )

    subparsers = parser.add_subparsers(title="commands")

    encrypt = subparsers.add_parser("encrypt", help="encrypt a message")
    encrypt.set_defaults(action=lambda _: commands.encrypt())

    decrypt = subparsers.add_parser("decrypt", help="decrypt a message")
    decrypt.set_defaults(action=lambda _: commands.decrypt())

    decrypt = subparsers.add_parser("recipient", help="manage recipient")
    decrypt.add_argument("--add", nargs="+", metavar="USER", help="add recipient")
    decrypt.add_argument("--remove", nargs="+", metavar="USER", help="remove recipient")
    decrypt.set_defaults(action=lambda _: commands.decrypt())

    return parser.parse_args()

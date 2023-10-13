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
    encrypt.add_argument("--file", default=None, metavar="PATH", help="file to encrypt (or - for stdin)")
    encrypt.set_defaults(action=lambda args: commands.encrypt(args.file))

    decrypt = subparsers.add_parser("decrypt", help="decrypt a message")
    decrypt.add_argument("--file", default=None, metavar="PATH", help="file to decrypt (or - for stdin)")
    decrypt.set_defaults(action=lambda args: commands.decrypt(args.file))

    recipient = subparsers.add_parser("recipient", help="manage recipient")
    recipient.add_argument("--add", nargs="+", metavar="USER", help="add recipient")
    recipient.add_argument("--remove", nargs="+", metavar="USER", help="remove recipient")
    recipient.set_defaults(action=lambda _: commands.decrypt())

    return parser.parse_args()

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

    encrypt = subparsers.add_parser("encrypt", help="encrypt a file")
    encrypt.add_argument("--file", default=None, metavar="PATH", help="file to encrypt (or - for stdin)")
    encrypt.set_defaults(action=lambda args: commands.encrypt(args.file))

    decrypt = subparsers.add_parser("decrypt", help="decrypt a file")
    decrypt.add_argument("--file", default=None, metavar="PATH", help="file to decrypt (or - for stdin)")
    decrypt.set_defaults(action=lambda args: commands.decrypt(args.file))

    recipient = subparsers.add_parser("access", help="manage access")
    recipient.add_argument("--permit", nargs="+", metavar="USER", help="give access to a user")
    recipient.add_argument("--revoke", nargs="+", metavar="USER", help="revoke user access")
    recipient.add_argument("--file", default=None, metavar="PATH", help="file to manage")
    recipient.set_defaults(action=lambda _: commands.decrypt())

    return parser.parse_args()

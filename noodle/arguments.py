import argparse
import commands


def parse_args():
    parser = argparse.ArgumentParser(description="Simple secret management")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug messages",
    )
    parser.add_argument(
        "--work-dir", default=".", metavar="PATH", help="work directory"
    )

    subparsers = parser.add_subparsers(title="commands")

    registry = subparsers.add_parser("registry", help="rebel registry")
    registry.set_defaults(action=lambda args: commands.registry(args.work_dir))

    encrypt = subparsers.add_parser("encrypt", help="encrypt a file")
    encrypt.add_argument("--file", default=None, metavar="PATH", help="file to encrypt")
    encrypt.add_argument(
        "--recipients",
        default=None,
        nargs="+",
        metavar="REBEL",
        help="rebel to encrypt for",
    )
    encrypt.set_defaults(
        action=lambda args: commands.encrypt(args.file, args.recipients, args.work_dir)
    )

    decrypt = subparsers.add_parser("decrypt", help="decrypt a file")
    decrypt.add_argument("--file", default=None, metavar="PATH", help="file to decrypt")
    decrypt.set_defaults(action=lambda args: commands.decrypt(args.file, args.work_dir))

    return parser.parse_args()

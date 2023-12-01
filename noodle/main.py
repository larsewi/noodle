import logging as log
from arguments import parse_args
import prompter
import commands
from utils import NOODLE_HEADER


def main():
    print(NOODLE_HEADER)
    args = parse_args()
    log.basicConfig(
        format="%(levelname)8s: %(message)s",
        level=log.DEBUG if args.debug else log.INFO,
    )

    actions = {
        "encrypt a file": (lambda: commands.encrypt(work_dir=args.work_dir)),
        "decrypt a file": (lambda: commands.decrypt(work_dir=args.work_dir)),
        "list registry": (lambda: commands.registry(work_dir=args.work_dir)),
        "tell me a joke": (lambda: commands.joke()),
    }

    if "action" in args:
        args.action(args)
    else:
        action = prompter.select("What do you want to do?", actions.keys())
        if action:
            actions[action]()

    print()

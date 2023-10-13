import logging as log
from arguments import parse_args
import prompter
import commands


NOODLE_HEADER = """
 ------------------------------------------------------------------------------
|                        _   _                 _ _                             |
|                       | \ | |               | | |                            |
|                       |  \| | ___   ___   __| | | ___                        |
|                       | . ` |/ _ \ / _ \ / _` | |/ _ \\                      |
|                       | |\  | (_) | (_) | (_| | |  __/                       |
|                       |_| \_|\___/ \___/ \__,_|_|\___|                       |
|                                                                              |
|                  *** Encryption not taken too seriously ***                  |
|                                                                              |
 ------------------------------------------------------------------------------
"""


def main():
    print(NOODLE_HEADER)
    args = parse_args()
    log.basicConfig(
        format="%(levelname)8s: %(message)s",
        level=log.DEBUG if args.debug else log.INFO,
    )

    actions = {
        "encrypt a file": (lambda: commands.encrypt()),
        "decrypt a file": (lambda: commands.decrypt()),
        "manage user access": (lambda: commands.access()),
        "tell me a joke": (lambda: commands.joke()),
    }

    if "action" in args:
        args.action(args)
    else:
        action = prompter.select("What do you want to do?", actions.keys())
        if action:
            actions[action]()

    print()

import logging as log
from arguments import parse_args
import prompter


NOODLE_HEADER = """
                         _   _                 _ _
                        | \ | |               | | |
                        |  \| | ___   ___   __| | | ___
                        | . ` |/ _ \ / _ \ / _` | |/ _ \\
                        | |\  | (_) | (_) | (_| | |  __/
                        |_| \_|\___/ \___/ \__,_|_|\___|

                     *** Encryption not taken seriously ***

 ------------------------------------------------------------------------------
|                                                                              |
|   Why did the Rebel Alliance use Noodle to protect their data from the       |
|   Empire?                                                                    |
|                                                                              |
|   Because they wanted to make sure their plans for defeating the Dark Side   |
|   didn't end up on the Dark Web!                                             |
|                                                                              |
|   Remember, even in a galaxy far, far away, data security is essential!      |
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
    if "action" in args:
        args.action(args)
    else:
        prompter.select("What's up?", ["Hanging out", "Chilling", "Not much..."])

import sys
import subprocess
import logging as log
import prompter


def encrypt(filename=None):
    print("encrypt")


def decrypt(filename=None):
    if filename is None:
        filename = prompter.file_picker(
            "What file do you want to decrypt?", ".", ".gpg"
        )

    if filename is None:
        log.info("Aborted decryption: no file picked ...")
        return

    if filename == "-":
        input = sys.stdin.read()
        process = subprocess.run(
            ["gpg", "--decrypt"],
            input=input,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="ascii",
        )
    else:
        process = subprocess.run(
            ["gpg", "--decrypt", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="ascii",
        )

    if process.returncode != 0:
        log.error(f"Failed to encrypt {filename if filename != '-' else 'from stdin'}")

    log.debug(process.stderr)
    print(process.stdout)


def access():
    print("recipient")


def joke():
    print(
        """    Why did the Rebel Alliance use Noodle to protect their data from the
    Empire?

    Because they wanted to make sure their plans for defeating the Dark Side
    didn't end up on the Dark Web!

    Remember, even in a galaxy far, far away, data security is essential!"""
    )

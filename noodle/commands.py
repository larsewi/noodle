import sys
import subprocess
import logging as log
import prompter

def encrypt(filename=None):
    print("encrypt")


def decrypt(filename=None):
    if filename is None:
        filename = prompter.file_picker("What file do you want to decrypt?", ".")
        print(filename)
        assert False

    if filename == "-":
        input = sys.stdin.read()
        process = subprocess.run(["gpg", "--decrypt"], input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="ascii")
    else:
        process = subprocess.run(["gpg", "--decrypt", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="ascii")

    if process.returncode != 0:
        log.error(f"Failed to encrypt {filename if filename != '-' else 'from stdin'}")

    log.debug(process.stderr)
    print(process.stdout)


def access():
    print("recipient")

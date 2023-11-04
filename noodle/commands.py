import os
import sys
import subprocess
import logging as log
import prompter


def add():
    pass

def remove():
    pass

def edit():
    pass


def _xxcrypt(method, infile):
    assert method in ("encrypt", "decrypt")

    if infile is None:
        include = [".gpg"] if method == "decrypt" else []
        exclude = [".gpg"] if method == "encrypt" else []
        infile = prompter.file_picker(
            f"What file do you want to {method}?", ".", include, exclude
        )
        if infile is None:
            log.info(f"Aborted {method}ion: No file picked")
            return
    assert infile is not None

    if method == "encrypt":
        outfile = f"{infile}.gpg"
    elif filename.endswith(".gpg"):
        outfile = filename[: -len(".gpg")]
    else:
        log.error("Aborted decryption: Expected '.gpg' extension")
        return

    log.debug(f"{method}ing '{infile}'")
    args = ["gpg", f"--{method}='{infile}'"]
    process = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="ascii",
    )

    if process.returncode != 0:
        log.error(f"Failed to {method} {infile}")
    log.debug(process.stderr)

    log.debug(f"Writing {method}ed data to file {outfile}")
    with open(outfile, "w") as f:
        f.write(process.stdout)

    log.debug(f"Deleting input file {input}")
    os.remove(infile)


def encrypt(filename=None):
    _xxcrypt("encrypt", filename)


def decrypt(filename=None):
    _xxcrypt("decrypt", filename)


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

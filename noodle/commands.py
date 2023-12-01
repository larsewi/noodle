import os
import sys
import subprocess
import logging as log
import prompter
import glob


def _execute(command):
    log.debug(f"Executing command: {' '.join(command)}")
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="ascii",
    )
    if process.returncode != 0:
        log.error(f"Command '{' '.join(command)}' failed: {process.stderr}")
        exit(1)
    if process.stderr:
        log.debug(process.stderr)
    return process.stdout


def _registry(work_dir="."):
    rebels = glob.glob(os.path.join(work_dir, ".pub-keys", "*.asc"))
    for rebel in rebels:
        stdout = _execute(["gpg", "--show-keys", "--with-colons", rebel])
        records = stdout.splitlines()
        user_id = None
        fingerprint = None
        for record in records:
            record = record.split(":")
            if record[0] == "uid":
                user_id = record[9]
            elif record[0] == "fpr":
                fingerprint = record[9]
        if user_id is not None and fingerprint is not None:
            yield (user_id, fingerprint)


def registry(work_dir="."):
    for rebel in _registry(work_dir=work_dir):
        print(*rebel)


def encrypt(filename=None, recipients=None, work_dir="."):
    if filename is None:
        filename = prompter.file_picker(
            f"What file do you want to encrypt?", dir=work_dir, exclude=[".gpg"]
        )
        if filename is None:
            log.info(f"Aborted encryption: No file picked")
            return
    assert filename is not None

    if recipients is None:
        pass

    source = os.path.join(work_dir, filename)
    dest = f"{source}.gpg"

    log.debug(f"Encrypting file '{source}'")
    stdout = _execute(["gpg", f"--encrypt='{source}'"])

    log.debug(f"Writing encrypted data to file '{dest}'")
    with open(f"{dest}", "w") as f:
        f.write(stdout)

    log.debug(f"Deleting input file {source}")
    os.remove(source)
    return 0


def decrypt(filename=None, work_dir="."):
    pass


def joke():
    print(
        """    Why did the Rebel Alliance use Noodle to protect their data from the
    Empire?

    Because they wanted to make sure their plans for defeating the Dark Side
    didn't end up on the Dark Web!

    Remember, even in a galaxy far, far away, data security is essential!"""
    )

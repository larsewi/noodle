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


def _check_result(command):
    try:
        subprocess.check_call(command + [">/dev/null 2>&1"])
    except subprocess.CalledProcessError:
        return False
    return True


def _registry(work_dir="."):
    files = glob.glob(os.path.join(work_dir, ".pub-keys", "*.asc"))
    for file in files:
        stdout = _execute(["gpg", "--show-keys", "--with-colons", file])
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
            yield (user_id, fingerprint, os.path.basename(file))


def registry(work_dir="."):
    for rebel in _registry(work_dir=work_dir):
        print(*rebel)


def encrypt(filename=None, recipients=None, work_dir="."):
    # Select file to encrypt
    if filename is None:
        filename = prompter.file_picker(
            f"What file do you want to encrypt?", dir=work_dir, exclude=[".gpg"]
        )
        if filename is None:
            log.info(f"Aborted encryption: No file picked")
            return
    assert filename is not None

    # Get rebels in registry
    rebels = [" ".join(rebel) for rebel in list(_registry(work_dir=work_dir))]
    if rebels is None:
        log.info(
            f"Aborted encryption: No rebels present in '{os.path.join(work_dir, '.pub-keys')}'"
        )
        return

    # Select rebels to encrypt for
    if recipients is None:
        recipients = prompter.multi_select(
            f"What rebels should be able to decrypt the file?",
            choices=rebels,
        )

    # Check that rebels are in the keyring
    for recipient in recipients:
        if not _check_result(["gpg", f"--list-keys={recipient[1]}"]):
            log.info(f"Adding missing recipient {recipient[1]}")
            _execute(["gpg", f"--import={recipient[2]}"])

    recipient_files = (
        os.path.join(work_dir, ".pub-keys", rebel.split(" ")[-1])
        for rebel in recipients
    )

    source = os.path.join(work_dir, filename)
    dest = f"{source}.gpg"

    log.debug(f"Encrypting file '{source}'")
    stdout = _execute(
        [
            "gpg",
            f"--encrypt='{source}'",
            f"--hidden-recipient-file={','.join(recipient_files)}",
        ]
    )

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

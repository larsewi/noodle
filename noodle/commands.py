import os
import subprocess
import logging as log
import prompter
import glob
import gnupg


def _execute(command):
    log.debug(f"Executing command: {' '.join(command)}")
    process = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="ascii",
        env=os.environ
    )
    if process.returncode != 0:
        log.error(f"Command '{' '.join(command)}' failed:")
        for line in process.stderr.splitlines():
            log.error(line)
        exit(1)
    if process.stderr:
        for line in process.stderr.splitlines():
            log.debug(line)
    return process.stdout


def _check_result(command):
    try:
        subprocess.check_call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="ascii", env=os.environ)
        return True
    except subprocess.CalledProcessError:
        return False


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


def encrypt(secret=None, recipients=None, work_dir="."):
    gpg = gnupg.GPG()

    # Select file to encrypt
    if secret is None:
        secret = prompter.file_picker(
            f"What file do you want to encrypt?", dir=work_dir, exclude=[".gpg"]
        )
        if secret is None:
            log.info(f"Aborted encryption: No file picked")
            return
    assert secret is not None

    files = glob.glob(os.path.join(work_dir, ".pub-keys", "*.asc"))
    for file in files:
        key = gpg.import_keys_file(file)
        log.info(f"Imported keys {', '.join(key.fingerprints)} from file {file}")

    rebels = (x for x in gpg.list_keys())
    for rebel in rebels:
        print(rebel)

    return

    if recipients is None:
        recipients = prompter.multi_select(
            f"What rebels should be able to decrypt the file?",
            choices=rebels,
        )
    recipients = (x.split(' ') for x in recipients)


    # Select rebels to encrypt for

    # Check that rebels are in the keyring
    command = ["gpg", "--encrypt", "--sign", "--armor"]
    for name, fingerprint, filename in recipients:
        if not _check_result(["gpg", "--list-keys", name]):
            log.debug(f"Adding missing recipient {name} {fingerprint}")
            path = os.path.join(work_dir, '.pub-keys/', filename)
            _execute(["gpg", "--import", path])
            _execute(["gpg", "--quick-sign-key", fingerprint, name])
            command.extend(["-r", name])

    source = os.path.join(work_dir, secret)
    command.append(source)
    dest = f"{source}.gpg"

    log.info(f"Encrypting file '{source}'")
    stdout = _execute(command)

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

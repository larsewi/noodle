set -e
set -x

rm -rf tests/out

########################################

echo "Generating public key for alice"
export GNUPGHOME=tests/out/alice/
mkdir -p $GNUPGHOME
chmod 700 $GNUPGHOME
gpg --yes \
    --batch \
    --pinentry-mode loopback \
    --passphrase '' \
    --quick-generate alice ed25519 default

echo "Exporting public key for alice"
mkdir -p tests/out/.pub-keys
gpg --armor --export alice > tests/out/.pub-keys/alice.asc

########################################

echo "Generating public key for bob"
export GNUPGHOME=tests/out/bob/
mkdir -p $GNUPGHOME
chmod 700 $GNUPGHOME
gpg --yes \
    --batch \
    --pinentry-mode loopback \
    --passphrase '' \
    --quick-generate bob ed25519 default

echo "Exporting public key for alice"
mkdir -p tests/out/.pub-keys
gpg --armor --export bob > tests/out/.pub-keys/bob.asc

########################################

echo "Creating a rebel secret"
echo "This is a rebel secret" > tests/out/secret.txt

########################################

echo "Encrypting secret for alice and bob"
export GNUPGHOME=tests/out/alice/
python3 noodle --work-dir tests/out --debug encrypt --file tests/secret.txt

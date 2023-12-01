set -e
set -x

# Clean-up
rm -rf $GNUPGHOME
rm -rf tests/.pub-keys
rm -f tests/secret.txt

# Generate public keys
export GNUPGHOME=tests/.gnupg
gpg --yes \
    --batch \
    --pinentry-mode loopback \
    --passphrase '' \
    --quick-generate alice ed25519 default
gpg --yes \
    --batch \
    --pinentry-mode loopback \
    --passphrase '' \
    --quick-generate bob ed25519 default

# Export public keys
mkdir -p tests/.pub-keys
gpg --armor --export alice > tests/.pub-keys/alice.asc
gpg --armor --export bob > tests/.pub-keys/bob.asc

echo "This is a secret" > tests/secret.txt

# python3 noodle encrypt --file tests/secret.txt

# Clean-up
rm -rf $GNUPGHOME
rm -rf tests/.pub-keys
rm -f tests/secret.txt
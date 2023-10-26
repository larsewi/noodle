set -e
set -x

export GNUPGHOME="`pwd`/.gnupg"

gpg --yes \
    --batch \
    --pinentry-mode 'loopback' \
    --passphrase '' \
    --quick-generate 'insecure' 'ed25519' 'default'

rm -rf $GNUPGHOME

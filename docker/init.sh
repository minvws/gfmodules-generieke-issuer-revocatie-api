#!/usr/bin/env bash

set -e

echo "➡️ Generating issuer JWK"
if [ ! -f secrets/issuer-jwk.json ]; then
  python -m app.gen_jwk secrets/issuer-jwk.json
fi

echo "➡️ Creating the configuration file"
if [ -e app.conf ]; then
    echo "⚠️ Configuration file already exists. Skipping."
else
    cp app.conf.example app.conf
fi

echo "Migrating"
tools/./migrate_db.sh

echo "Start main process"
python -m app.main

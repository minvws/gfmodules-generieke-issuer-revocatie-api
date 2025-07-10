#!/usr/bin/env bash

set -e

echo "➡️ Generating TLS certificates"
tools/./generate_certs.sh

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

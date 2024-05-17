#!/usr/bin/env bash

export DOCKER_CONTEXT=dietpi

LOCK_FILE="$(pwd)/PDFtools.lock"
cd /home/dietpi/Applications/PDFtools
flock -n $LOCK_FILE ./scripts/change-detector.sh >> /var/log/deploy-pdftools.log 2>&1

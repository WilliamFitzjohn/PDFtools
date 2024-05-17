#!/usr/bin/env bash

LOCK_FILE="$(pwd)/PDFtools.lock"
cd /home/dietpi/Applications/PDFtools
flock -n $LOCK_FILE ./scripts/change-detector.sh >> /home/dietpi/Logs/deploy-pdftools.log 2>&1

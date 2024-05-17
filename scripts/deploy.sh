#!/usr/bin/env bash
git pull
BUILD_VERSION=$(git rev-parse HEAD)
echo "$(date --utc +%FT%TZ): Releasing new api version. $BUILD_VERSION"
echo "$(date --utc +%FT%TZ): Removing old release..."
docker compose down
echo "$(date --utc +%FT%TZ): Removed."
echo "$(date --utc +%FT%TZ): Deploying new release..."
docker compose up -d --build --no-deps --scale api=1 --no-recreate api
echo "$(date --utc +%FT%TZ): Deployed. $BUILD_VERSION"
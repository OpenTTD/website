#!/bin/sh

set -ex

# Install latest Ruby requirements (most are baked in the devcontainer, but check for updates)
bundle install
bundle clean --force

# Install latest Python requirements
pip install -r requirements.txt

# Fetch the latest downloads
python -m fetch_downloads

# Ensure the git submodule is initialized
git submodule update --init

#!/bin/bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install textlint
npm install -g textlint
npm install -g textlint-filter-rule-comments
npm install -g textlint-rule-preset-ja-technical-writing

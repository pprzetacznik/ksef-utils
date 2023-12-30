#!/bin/bash

set -xe

# export TESTS_MARKERS="e2e and not ignore"
# export TESTS_MARKERS="functional and not ignore"
export TESTS_MARKERS=${TESTS_MARKERS:-"current and not ignore"}

python \
  -m pytest \
  tests \
  -m "$TESTS_MARKERS" \
  --cov-report term \
  --cov=ksef_utils \
  -svvv

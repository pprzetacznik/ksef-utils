# KSEF utils

## Installing package from source

```Bash
$ cd ksef-utils
$ pip install -e .
```

## Run tests

```Bash
$ mkvirtualenv ksef
(ksef) $ pip install -r requirements.txt
(ksef) $ pytest -svvv
```

## Set up secrets

Log in to https://ksef-test.mf.gov.pl/web/ and generate your individual `KSEF_TOKEN`.

```Bash
#!/bin/bash

export KSEF_ENV="test"
export KSEF_TOKEN="..."
export KSEF_NIP="..."
```

## OpenAPI

```
/openapi/gtw/svc/api/KSeF-common.yaml
/openapi/gtw/svc/api/KSeF-batch.yaml
/openapi/gtw/svc/api/KSeF-online.yaml
```

## Marks

Run all e2e/functional/current tests
```
$ pytest -svvv tests/test_ksef.py -m "e2e and not ignore"
$ pytest -svvv tests/test_ksef.py -m "functional and not ignore"
$ pytest -svvv tests/test_ksef.py -m "current and not ignore"
$ ./run_tests.sh
```

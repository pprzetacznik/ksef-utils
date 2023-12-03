# KSEF utils

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
export KSEF_SESSION="..."
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
$ pytest -svvv test_ksef.py -m e2e
$ pytest -svvv test_ksef.py -m functional
$ pytest -svvv test_ksef.py -m current
```

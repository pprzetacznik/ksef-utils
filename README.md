# KSeF utils

[![ksef-utils Release](https://github.com/pprzetacznik/ksef-utils/actions/workflows/release.yml/badge.svg)](https://github.com/pprzetacznik/ksef-utils/actions/workflows/release.yml)
[![ksef-utils Test](https://github.com/pprzetacznik/ksef-utils/actions/workflows/test.yml/badge.svg)](https://github.com/pprzetacznik/ksef-utils/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/ksef-utils.svg)](https://pypi.org/project/ksef-utils/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ksef-utils)](https://pypi.org/project/ksef-utils/)
[![Documentation Status](https://readthedocs.org/projects/ksef-utils/badge/?version=latest)](https://ksef-utils.readthedocs.io/en/latest/?badge=latest)

This project contains Python utilities and example requests that can be helpful when integrating with Polish central invoicing system called [Krajowy System e-Faktur (KSeF)](https://www.podatki.gov.pl/ksef/).

## Installation

### Creating python virtual environment

See [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) documentation.

```Bash
$ mkvirtualenv ksef
$ workon ksef
(ksef) $
```

### Installing package from source

```Bash
(ksef) $ git clone https://github.com/pprzetacznik/ksef-utils.git
(ksef) $ cd ksef-utils
(ksef) $ pip install -e .
```

### Installing package from PyPI

```Bash
(ksef) $ pip install ksef-utils
```

## Run tests

### Set up secrets

Log in to https://ksef-test.mf.gov.pl/web/ and generate your individual `KSEF_TOKEN`.

```Bash
#!/bin/bash

export KSEF_TOKEN="..."
export KSEF_ENV="test"
export KSEF_NIP="..."
export KSEF_SIGN_CERT_PATH="cert.pem"
export KSEF_SIGN_KEY_PATH="privkey.pem"
export KSEF_SIGN_CA_PATH="cert.pem"
```

### Generate test cert

```Bash
KSEF_NIP=${KSEF_NIP:-2222222222}
KSEF_SUBJECT="/CN=John Doe/SN=Doe/GN=John/O=My Corp/C=PL/L=Lesser Voivodeship/serialNumber=NIP-${KSEF_NIP}/description=John Doe NIP-${KSEF_NIP}"
openssl req -x509 \
  -nodes \
  -subj "${KSEF_SUBJECT}" \
  -days 365 \
  -newkey rsa \
  -keyout $KSEF_SIGN_KEY_PATH \
  -out $KSEF_SIGN_CERT_PATH
```

### Run pytest framework

```Bash
(ksef) $ pip install -r requirements.txt
(ksef) $ pytest -svvv
```

### Markers

Run all e2e/functional/current tests
```
(ksef) $ pytest -svvv tests/test_ksef.py -m "e2e and not ignore"
(ksef) $ pytest -svvv tests/test_ksef.py -m "functional and not ignore"
(ksef) $ pytest -svvv tests/test_ksef.py -m "current and not ignore"
(ksef) $ ./run_tests.sh
(ksef) $ TESTS_MARKERS="init_signed and functional and not ignore" ./run_tests.sh
```

## Example

See [tests/test_e2e.py](tests/test_e2e.py) for detailed examples of usage.

```Python
from ksef_utils.server import KSEFServer, KSEFService
from ksef_utils.config import TestConfig, DemoConfig, ProdConfig

config = TestConfig()
server = KSEFServer(config)
service = KSEFService(service)

invoice_data = {
    # ...
    # see tests/conftest.py for example json invoice
}

session_token = service.init_signed()
response_send_invoice = service.send_invoice(**invoice_data)
```

## Using cli utilities

```
(ksef) $ python -m ksef_utils --identifier 1111111111 --identifier_type NIP --working_directory .
(ksef) $ pip install .
(ksef) $ which ksef-utils
(...)/.envs/bin/ksef-utils
(ksef) $ ksef-utils --identifier 1111111111 --identifier_type PESEL --working_directory .
```

## OpenAPI

```
/openapi/gtw/svc/api/KSeF-common.yaml
/openapi/gtw/svc/api/KSeF-batch.yaml
/openapi/gtw/svc/api/KSeF-online.yaml
```

## Publish new release

```Bash
$ git tag v1.0
$ git push origin v1.0
```

## Building documentation

```Bash
(ksef) $ sphinx-build -M html docs docs_build
```

## KSEF references

* https://www.podatki.gov.pl/ksef/
* https://ksef-test.mf.gov.pl/web/
* https://www.youtube.com/watch?v=dnBGO6IPtzA

## Contributing

* https://www.conventionalcommits.org/en/v1.0.0/

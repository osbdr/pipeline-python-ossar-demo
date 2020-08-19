# pipeline-python-demo

Beispiel einer Pipeline, die folgendes kann:
- Outdated Check
- Code Format mit `black` überprüfen
- Sortierung der Imports mit `isort` überprüfen
- Run OSSAR (Microsoft Security Code Analysis)
- Tests ausführen
- Security Check mit `bandit`
- Erstellung eines Docker Images

Die Dependencies werden mit Renovate aktualisiert. Mehr Infos: https://github.com/renovatebot/renovate

> **Hinweis**: 
> - `pip list --outdated` endet unabhängig vom Ergebnis immer mit Exit Code `0`, damit die Pipeline entsprechend reagiert wurde der Befehl im Folgenden erweitert.

```
name: Standard Pipeline

on:
  pull_request:
    branches: '**'
  push:
    branches:
      - develop
  schedule:
    - cron: '0 20 * * 5'

jobs:
  outdated:
    runs-on: ubuntu-latest
    if: startsWith(github.head_ref, 'renovate') == false
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: pip install
      run: pip install -r requirements.txt --user

    - name: outdated
      run: pip list --outdated --not-required --user | grep . && echo "there are outdated packages" && exit 1 || echo "all packages up to date"

  black:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: pip install
      run: pip install -r requirements.txt

    - name: black
      run: black --check .

  isort:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: pip install
      run: pip install -r requirements.txt

    - name: isort
      run: isort --check .

  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: pip install
      run: pip install -r requirements.txt 

    - name: test
      run: python -m unittest discover

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.8

    - name: pip install bandit
      run: pip install bandit==1.6.2

    - name: bandit
      run: bandit -r *.py -f json -o report.json

    - name: show report
      if:  ${{ success() || failure() }}
      run: cat report.json

    - name: upload report
      if:  ${{ success() || failure() }}
      uses: actions/upload-artifact@v2
      with:
        name: Bandit Security Report
        path: report.json

  docker:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: docker build
      run: docker build -t python-demo .
```

## Referenzen
- pip list: https://pip.pypa.io/en/stable/reference/pip_list/
- black: https://github.com/psf/black
- isort: https://github.com/timothycrosley/isort
- bandit: https://pypi.org/project/bandit/

- Docker Pipeline: https://partner.bdr.de/gitlab/kfe-devops/docker-demo

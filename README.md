# pre-commit-shell

[![CI](https://github.com/jameswoolfenden/pre-commit-shell/actions/workflows/ci.yml/badge.svg)](https://github.com/jameswoolfenden/pre-commit-shell/actions/workflows/ci.yml)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/jameswoolfenden/pre-commit-shell/master/LICENSE)
[![release](https://img.shields.io/github/release/jameswoolfenden/pre-commit-shell.svg)](https://github.com/jameswoolfenden/pre-commit-shell/releases)

pre-commit-shell is a [pre-commit](https://github.com/pre-commit/pre-commit) hook that wraps [shellcheck](https://www.shellcheck.net/) to lint shell scripts.

Table of Contents
-----------------

  * [Requirements](#requirements)
  * [Install](#install)
  * [Contributing](#contributing)
  * [License](#license)
  * [Author](#author)

Requirements
------------
  pre-commit-shell requires the following to run:

  * [pre-commit](https://pre-commit.com)
  * [shellcheck](https://www.shellcheck.net/)


Install
---------

1. create .pre-commit-config.yaml in your git project
2. pre-commit install
3. enjoy it

example .pre-commit-config.yaml as following:

```yaml
repos:
  - repo: https://github.com/jameswoolfenden/pre-commit-shell
    rev: v1.0.6
    hooks:
      - id: shell-lint
        args: [--format=json]
```
Contributing
------------

To contribute to pre-commit-shell, clone this repo locally and commit your code on a separate branch.


Author
------

> GitHub [@jameswoolfenden](https://github.com/jameswoolfenden)

Originally by [@detailyang](https://github.com/detailyang).


License
-------

pre-commit-shell is licensed under the [MIT](https://github.com/jameswoolfenden/pre-commit-shell/blob/master/LICENSE) license.

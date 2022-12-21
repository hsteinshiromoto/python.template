# Python Project Template

This is a [cookiecutter](https://github.com/audreyr/cookiecutter) template for a typical Python project following modern packaging conventions.

[![Build Status](https://github.com/hsteinshiromoto/python.template/actions/workflows/ci.yml/badge.svg)](https://github.com/hsteinshiromoto/python.template/actions/workflows/ci.yml)

## Features

* [x] [Poetry](https://poetry.eustace.io/) for dependency management


## Usage

Install `cookiecutter` and generate a project:

```
$ pip install cookiecutter
$ cookiecutter gh:hsteinshiromoto/python.template -f
```

Cookiecutter will ask you for some basic info (your name, project name, python package name, etc.) and generate a base Python project for you.
Once created, run the code formatter to updates files based on your chosen names:

## Updates

Run the update tool, which is generated inside each project:

```
$ bin/update
```

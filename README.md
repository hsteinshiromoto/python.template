[![DOI](https://zenodo.org/badge/580578142.svg)](https://zenodo.org/badge/latestdoi/580578142)
[![Build Status](https://github.com/hsteinshiromoto/python.template/actions/workflows/ci.yml/badge.svg)](https://github.com/hsteinshiromoto/python.template/actions/workflows/ci.yml)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hsteinshiromoto/python.template?style=flat)
![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)


# Python Project Template

This is a [cookiecutter](https://github.com/audreyr/cookiecutter) template for a typical Python project following modern packaging conventions.

**Table of Contents**

- [Python Project Template](#python-project-template)
  - [Features](#features)
  - [Usage](#usage)
  - [Adding CI files](#adding-ci-files)
  - [Create repository structure for a machine learning project](#create-repository-structure-for-a-machine-learning-project)


## Features

* [x] [Poetry](https://poetry.eustace.io/) for dependency management
* [x] Docker for development.
* [x] Github actions for CI.
* [x] VSCode as IDE.


## Usage

Install `cookiecutter` using
```bash
$ pip install cookiecutter
```
and generate a project:

```bash
$ cookiecutter gh:hsteinshiromoto/python.template -f
```

Cookiecutter will ask you for some basic info (your name, project name, python package name, etc.) and generate a base Python project for you.

## Adding CI files

To add CI files to your project, run the following command:

```bash
$ make ci
```

## Create repository structure for a machine learning project

To create a repository structure for a machine learning project, run the following command:

```bash
$ make structure r=machine_learning
```
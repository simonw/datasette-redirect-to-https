# datasette-redirect-to-https

[![PyPI](https://img.shields.io/pypi/v/datasette-redirect-to-https.svg)](https://pypi.org/project/datasette-redirect-to-https/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-redirect-to-https?include_prereleases&label=changelog)](https://github.com/simonw/datasette-redirect-to-https/releases)
[![Tests](https://github.com/simonw/datasette-redirect-to-https/workflows/Test/badge.svg)](https://github.com/simonw/datasette-redirect-to-https/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-redirect-to-https/blob/main/LICENSE)

Datasette plugin that redirects all non-https requests to https

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-redirect-to-https

## Usage

Usage instructions go here.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-redirect-to-https
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest

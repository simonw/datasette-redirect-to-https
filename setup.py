from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-redirect-to-https",
    description="Datasette plugin that redirects all non-https requests to https",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-redirect-to-https",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-redirect-to-https/issues",
        "CI": "https://github.com/simonw/datasette-redirect-to-https/actions",
        "Changelog": "https://github.com/simonw/datasette-redirect-to-https/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_redirect_to_https"],
    entry_points={"datasette": ["redirect_to_https = datasette_redirect_to_https"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio", "asgi-lifespan"]},
    python_requires=">=3.6",
)

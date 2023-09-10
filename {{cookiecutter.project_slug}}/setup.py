import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

docs_extras = [
    "Sphinx >= 3.0.0",  # Force RTD to use >= 3.0.0
    "docutils",
    "pylons-sphinx-themes >= 1.0.8",  # Ethical Ads
    "pylons_sphinx_latesturl",
    "repoze.sphinx.autointerface",
    "sphinxcontrib-autoprogram",
]

# This call to setup() does all the work
setup(
    name="{{ cookiecutter.project_slug }}",
    version="0.1.0",
    description="{{ cookiecutter.project_short_description }}",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.github.com/{{ cookiecutter.user_name }}/{{ cookiecutter.project_slug }}",
    author="{{ cookiecutter.full_name }}",
    author_email="{{ cookiecutter.email }}",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: {{cookiecutter.python_major_version}}",
        "Programming Language :: Python :: {{cookiecutter.python_major_version}}.{{cookiecutter.python_minor_version}}",
    ],
    packages=["python.template"],
    include_package_data=True,
    extras_require={"docs": docs_extras},
)

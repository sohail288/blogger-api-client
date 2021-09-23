import re
from pathlib import Path

from setuptools import find_packages, setup

version_string = re.search(r"""__version__\s*=\s*['"]([^'"]+)['"]""", Path("blogger_client/__init__.py").read_text())
long_description = Path('README.md').read_text()


if version_string is None:
    raise SystemExit("Missing version string in blogger_client/__init__.py.")


setup(
    name="blogger_client",
    version=version_string.group(1),
    packages=find_packages(exclude=["tests"]),
    install_requires=["requests", "google-auth-oauthlib"],
    python_requires=">=3.7"
)

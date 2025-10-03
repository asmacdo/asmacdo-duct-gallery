"""Setup configuration for con-duct-gallery."""
from setuptools import setup, find_packages

setup(
    name="con-duct-gallery",
    version="0.1.0",
    description="Gallery markdown output generator for duct executions",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "con-duct[all]",
    ],
    entry_points={
        "console_scripts": [
            "con-duct-gallery=src.cli:main",
        ],
    },
)

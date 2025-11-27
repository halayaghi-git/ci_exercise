"""Setup script for the ci_exercise package."""

from setuptools import setup, find_packages

setup(
    name="ci_exercise",
    version="1.0.0",
    description="A sample project demonstrating CI/CD with GitHub Actions",
    author="DevOps Student",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

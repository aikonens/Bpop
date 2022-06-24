from setuptools import setup
import io

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Bpop",
    packages=["Bpop"],
    version="1.0.0",
    description="Boltzmann weight calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Santeri Aikonen",
    author_email="santeri.aikonen@gmail.com",
    url="https://github.com/aikonens/Bpop",
    keywords=["compchem", "Boltzmann", "informatics", "thermochemistry"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["argparse", "pandas"],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"": ["*.csv"]},
)

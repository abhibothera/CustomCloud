from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="topsis-Algorithm",
    version="2.0.0",
    description="A Python package to get ranks of dataset using TOPSIS (UCS633).",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Pulkitg64/TOPSIS-in-Python",
    author="Pulkit Gupta",
    author_email="pulkitgupta64@gmail.com",
    packages=["topsis_algo"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "weather-reporter=weather_reporter.cli:main",
        ]
    },
)
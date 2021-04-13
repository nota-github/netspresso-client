import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netspresso_cli",
    version="0.1.0",
    author="Nota Inc.",
    author_email="nota_dev@nota.ai",
    description="deep-learning-model compression framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires= [
        "boto3==1.17.38",
        "botocore==1.20.38",
        "certifi==2020.12.5",
        "chardet==4.0.0",
        "idna==2.10",
        "jmespath==0.10.0",
        "numpy==1.20.1",
        "pandas==1.2.3",
        "python-dateutil==2.8.1",
        "pytz==2021.1",
        "PyYAML==5.4.1",
        "requests==2.25.1",
        "s3transfer==0.3.6",
        "six==1.15.0",
        "tqdm==4.59.0",
        "urllib3==1.26.4"
    ],

    entry_points={
        'console_scripts':[
            'netspresso-cli=netspresso_cli.main:main',
        ],
    },
)

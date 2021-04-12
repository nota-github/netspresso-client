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
    packages=setuptools.find_packages(where="netspresso_cli"),
    python_requires=">=3.7",
)
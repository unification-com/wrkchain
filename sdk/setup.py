import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="workchain",
    version="0.0.2",
    author="Unification Foundation",
    author_email="hello@unification.com",
    description="Bring up a Workchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unification-com/workchain",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

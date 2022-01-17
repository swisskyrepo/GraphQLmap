import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graphqlmap",
    version="0.0.1",
    description="scripting engine to interact with a GraphQL endpoint for pentesting purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swisskyrepo/GraphQLmap",
    packages=setuptools.find_packages(),
    scripts=["bin/graphqlmap"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
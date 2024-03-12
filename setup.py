from setuptools import setup, find_packages
import platform


with open("README.md", "r") as fh:
    long_description = fh.read()

dependencies = ['httpx', 'urllib3']

if platform.system() == "Windows":
    dependencies.append('pyreadline3')
else:
    dependencies.append('readline')

setup(
    name="graphqlmap",
    version="0.0.1",
    description="scripting engine to interact with a GraphQL endpoint for pentesting purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swisskyrepo/GraphQLmap",
    packages=find_packages(include=['graphqlmap', 'graphqlmap.*']),
    entry_points={
        'console_scripts': [
            'graphqlmap = graphqlmap.cli:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=dependencies,
)
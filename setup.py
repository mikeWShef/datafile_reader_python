import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="rr_python_file_reader",
    version="0.0.1",
    author="Mike Watson",
    author_email="m.watson@rivelinrail.com",
    description=("Python package for reading tribometer files"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikeWShef/datafile_reader_python",
    project_urls={
        "Bug Tracker": "https://github.com/mikeWShef/datafile_reader_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)
import setuptools

with open ("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="hotboxer-bajaco",
        version="0.0.2",
        author="bajaco",
        author_email="admin@agyx.org",
        description="A CLI hotkey manager for Openbox",
        long_description=long_description,
        long_description_markdown_type="text/markdown",
        url="https://github.com/bajaco/hotbox",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6', 
        )

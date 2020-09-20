import setuptools

with open ("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="hotbox-bajaco",
        version="0.0.1",
        author="bajaco",
        author_email="admin@agyx.org",
        description="A CLI hotkey manager for Openbox",
        long_description=long_description,
        long_description_markdown_type="text/markdown",
        url="https://github.com/bajaco/hotbox",
        package_data={
            "": ["*.json", "*.ini"],
            },
        packages=setuptools.find_packages(),
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6', 
        entry_points={
            'console_scripts': [
                'hotbox=hotbox:main',
                ],
            }

        )

import setuptools

long_description = "Siehe Readme"

setuptools.setup(
    name="PythonSprachassistent",
    version="0.0.3",
    author="e4rdx",
    description="Ein Sprachassistent fuer Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)

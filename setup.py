import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="de_mwaa_tips",
    version="0.0.1",
    author="Herculano Cunha",
    author_email="herculanocm@outlook.com",
    description="Data Engineer tips for Airflow",
    download_url='https://github.com/herculanocm/mwaa-tips/archive/master.zip',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords='AWS MWAA tips',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['urllib3','slack-sdk==3.21.3', 'boto3']
)
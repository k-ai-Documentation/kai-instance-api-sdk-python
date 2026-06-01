import setuptools

setuptools.setup(
    name="kai_sdk_python",
    version="20260601",
    author="KAI",
    author_email="support@wats.ai",
    description="KAI Studio Python SDK",
    packages=setuptools.find_packages(),
    install_requires=["httpx==0.28.0"],
    python_requires=">=3.12",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/k-ai-Documentation/kai-instance-api-sdk-python",
)

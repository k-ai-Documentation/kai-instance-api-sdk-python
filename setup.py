import setuptools

setuptools.setup(
    name="kai_sdk_python",
    version="20250210",
    author="KAI",
    author_email="support@wats.ai",
    description="sdk KAI python",
    packages=setuptools.find_packages(),
    install_requires=['httpx==0.27.2'],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/k-ai-Documentation/sdk-python'
)

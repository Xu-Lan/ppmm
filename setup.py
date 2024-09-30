from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
setup(
    name="ppmm",
    version="1.1.4",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'ppmm': ['data.json'],
    },
    entry_points={
        'console_scripts': [
            'mm=ppmm.cli:cli',
            'ppmm=ppmm.cli:cli',
        ],
    },
    install_requires=[
        'click',
    ],
    author="XuLan",
    author_email="xuzn@msn.com",
    description="A simple pip mirror management tool",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
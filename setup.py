from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='WhyCrash',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'rich',
        'questionary',
    ],
    description='A highly automatic AI error handler and code fixer using OpenRouter and Minimax.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/WhyCrash', # Update this when you have a github repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

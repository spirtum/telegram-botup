from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='telegram-botup',
    version='0.8.0',
    author='Dima Shebotinov',
    author_email='groovestreetmagic@gmail.com',
    description='Telegram bot API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['botup'],
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=[
        'Click',
        'requests'
    ],
    extras_require={
        'socks': ['pysocks'],
        'redis': ['redis']
    },
    entry_points={
        'console_scripts': ['botup=botup.cli:cli'],
    },
    project_urls={
        'Source Code': 'https://github.com/spirtum/telegram-botup'
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)

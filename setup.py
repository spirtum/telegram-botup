from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='telegram-botup',
    version='0.5.1',
    author='Dima Shebotinov',
    author_email='groovestreetmagic@gmail.com',
    description='Library for development Telegram bots',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['botup'],
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=[
        'Click',
        'requests',
        'redis'
    ],
    entry_points={
        'console_scripts': ['botup=botup.cli:cli'],
    },
    project_urls={
        'Source Code': 'https://bitbucket.org/dimashebo/telegram-botup'
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)

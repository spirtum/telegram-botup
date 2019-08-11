from setuptools import setup, find_packages

setup(
    name='telegram-botup',
    version='0.3.0',
    author='Dima Shebotinov',
    author_email='groovestreetmagic@gmail.com',
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

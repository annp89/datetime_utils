from setuptools import setup

setup(
    name='datetime_utils',
    version='0.1',
    license='MIT',
    packages=[
        'datetime_utils',
    ],
    url='https://github.com/annp89/datetime_utils',
    author='Ann Paul',
    author_email='ann.mpaul@gmail.com',
    description='Python functions for common operations on datetime instances.',
    install_requires=[
        'pytz>=2014.10',
    ],
    classifiers=[
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='python datetime pytz timezone timedelta arithmetic round floor period conversion',
    test_suite='nose.collector',
    tests_require=[
        'coverage==3.7.1',
        'nose>=1.3.0',
    ],
)

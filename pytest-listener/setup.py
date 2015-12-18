import sys
import logging

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

classifiers = [
    'License :: OSI Approved :: MIT License',
    'Development Status :: 5 - Production/Stable',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Testing',
    'Topic :: Utilities',
    'Intended Audience :: Developers',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]

long_description = open("README.rst").read()

pytest_args = []


class PyTest(TestCommand):

    def initialize_options(self):
        TestCommand.initialize_options(self)

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s %(message)s', level='DEBUG')

        # import here, cause outside the eggs aren't loaded
        import pytest

        pytest_args.extend(['--cov', 'pytest_listener',
                            '--cov-report', 'xml',
                            '--cov-report', 'html',
                            '--junitxml', 'junit.xml',
                            ])
        errno = pytest.main(pytest_args)
        sys.exit(errno)


def main():
    # Gather trailing arguments for pytest, this can't be done using setuptools' api
    global pytest_args
    if 'test' in sys.argv:
        pytest_args = sys.argv[sys.argv.index('test') + 1:]
        if pytest_args:
            sys.argv = sys.argv[:-len(pytest_args)]

    install_requires = ['six',
                        'pytest']

    tests_require = ['pytest-cov',
                     ]

    entry_points = {
        'pytest11': [
            'listener = pytest_listener',
        ]
    }

    setup(
        name='pytest-listener',
        description='A simple network listener',
        long_description=long_description,
        version='1.0.0',
        url='https://github.com/manahl/pytest-plugins',
        license='MIT license',
        platforms=['unix', 'linux'],
        author='Tim Couper',
        author_email='drtimcouper@gmail.com',
        classifiers=classifiers,
        install_requires=install_requires,
        tests_require=tests_require,
        cmdclass={'test': PyTest},
        packages=find_packages(exclude='tests'),
        entry_points=entry_points,
    )

if __name__ == '__main__':
    main()
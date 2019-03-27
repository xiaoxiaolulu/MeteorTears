# -*- coding:utf-8 -*-
import io
import os
import sys
from shutil import rmtree
from setuptools import Command, find_packages, setup


about = {}
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'lib', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'requests',
    'contextlib2',
    'colorama',
    'xlrd',
    'xlwt',
    'pyyaml',
    'pymysql'
]


class UploadCommand(Command):

    user_options = []

    @staticmethod
    def status(s):
        print("\033[0;32m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Publishing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    license=about['__license__'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    packages=find_packages(exclude=["testhtml", "WorkFlow", 'workFlow_cases']),
    package_data={
        '': ["README.md"],
        'lib': ["template/*"],
    },
    keywords='HTTP api test.yaml requests',
    install_requires=install_requires,
    extras_require={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    entry_points={
        'console_scripts': [
            'runner=run:run',
        ]
    },
    cmdclass={
        'upload': UploadCommand
    }
)

#!/usr/bin/env python
"""setup.py for shorah."""
import glob
import sys
import os
import shutil

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command.develop import develop
from setuptools.command.install import install


def move_files():
    """Identify the build directory and copy executables into src/shorah."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(base_dir, 'bin')
    diri_exe = os.path.join(bin_dir, 'diri_sampler')
    
    for exe in ['b2w', 'diri_sampler', 'fil']:
        exe_file = os.path.join(bin_dir, exe)
        if not os.path.exists(exe_file):
            sys.exit(f'No executable {exe} found in {bin_dir}. Build first.')
        shu = shutil.copy(exe_file, 'src/shorah/bin')


class CustomDevelop(develop):
    """Subclassing develop to install files in the correct location."""
    def run(self):
        move_files()
        develop.run(self)


class CustomInstall(install):
    """Subclassing develop to install files in the correct location."""
    def run(self):
        move_files()
        install.run(self)


class PyTest(TestCommand):
    """Subclass TestCommand to run python setup.py test."""
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    use_scm_version=True,
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    install_requires=['setuptools_scm'],
    tests_require=['pytest', 'flake8', 'pep257'],
    cmdclass={
        'test': PyTest,
        'install': CustomInstall,
        'develop': CustomDevelop
        },
    name='ShoRAH',
    description='SHOrt Reads Assembly into Haplotypes',
    url='http://github.com/cbg-ethz/shorah',
    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},  # tell setuptools packages are under src
    entry_points={'console_scripts': ['shorah = shorah.cli:main']},
    license='GPL 3.0',
    long_description='''
    ShoRAH is designed to analyse genetically heterogeneous samples. It provides error correction,
    local haplotype reconstruction, and estimation of the frequency of the different genetic variants
    present in a mixed sample.
    ''',
    project_urls={
        'Documentation': 'http://cbg-ethz.github.io/shorah',
        'Source': 'https://github.com/cbg-ethz/shorah',
    },
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        # Pick your license as you wish (should match "license" above)
        'License :: GPL 3.0',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6']
)

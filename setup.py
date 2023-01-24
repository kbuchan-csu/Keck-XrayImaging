from setuptools import setup, findpackages

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering',
    'Topic :: System :: Hardware',
    'Topic :: Thorlabs',
    'Operating System :: POSIX :: Linux'
]

PACKAGES = [
    'keck',
    'keck/control',
    'keck/UI'
]

LONG_DESCRIPTION = ''

setup(name = 'keck-xrayimaging',
      version = '0.0',
      url = 'https://github.com/AartHauk/Keck-XrayImaging.git',
      license = 'GNU',
      author = 'Andrew Kane',
      author_email = 'kaneaw@colostate.edu',
      description = 'A program to control the xray imaging motors for the Keck project',
      long_description = LONG_DESCRIPTION,
      platforms = ['Linux'],
      packages = PACKAGES,
      install_requires = ['pystage_apt>=0.4'],
      classifiers = CLASSIFIERS,
      python_requires = '>=3',
      data_files = [('',['LICENSE.txt'])],
      zip_safe = False
)
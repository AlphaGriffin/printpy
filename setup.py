#!/usr/bin/env python3
#
# Copyright (C) 2017-2018 Alpha Griffin
# @%@~LICENSE~@%@

"""Alpha Griffin Python setuptools build script.

@author lannocc

@see    https://packaging.python.org/en/latest/distributing.html
@see    https://github.com/pypa/sampleproject

Some of this script logic also taken from:
        https://github.com/google/protobuf
"""

# FIXME / note to self:
#  read more at https://caremad.io/posts/2013/07/setup-vs-requirement/
#  -- to integrate fully pip



# -------------------------------------------------------------------------------------
#
# CUSTOMIZE THIS SECTION
#   All the variables defined here should be customized for your project.
#

NS      = 'ag'                          # namespace / meta-package folder
NAME    = 'print'                       # should match source package name in NS folder
COMMAND = 'printpy'                     # command name may be different than package name
REQUIRE = [                             # package dependencies
            #'ag.logging',
          ]

DESC    = 'Printing utilities for Python'
TAGS    = 'utilities'                   # space-separated list of keywords

AUTHOR  = 'ruckusist'                   # name or alias of author
EMAIL   = 'ruckusist@alphagriffin.com'  # email of author

URL     = 'http://alphagriffin.com'
LICENSE = 'AG'                          # type of license
COPY    = '2018 Alpha Griffin'          # copyright

CLASS   = [
    # @see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Topic :: Utilities',
]


#
# END CUSTOMIZATION AREA
# -------------------------------------------------------------------------------------







#################
# !!! WARNING !!!
# !!! WARNING !!!
#################
# THINK CAREFULLY BEFORE CHANGING ANYTHING BELOW THIS LINE

from setuptools import setup, find_packages, Command
from codecs import open
from os.path import join, splitext, dirname
from os import sep, walk
from distutils.dep_util import newer


def findversion(root, name, up=0):
    '''versioning strategy taken from http://stackoverflow.com/a/7071358/7203060'''

    import re
    vfile = join(root.replace('.', sep), name, "__version__.py")
    for i in range(up):
        vfile = join('..', vfile)
    vmatch = re.search(r'^__version__ *= *["\']([^"\']*)["\']', open(vfile, "rt").read(), re.M)
    if vmatch:
        version = vmatch.group(1)
        print ("Found %s.%s version %s" % (root, name, version))
        return version
    else:
        raise RuntimeError("Expecting a version string in %s." % (vfile))


def findnamespaces(package):
    ns = []

    dot = package.find('.')
    while dot > 0:
        ns.append(package[:dot])
        dot = package.find('.', dot+1)

    return ns



if __name__ == '__main__':

    setup(
        name=(NS+'.'+NAME),
        version=findversion(NS, NAME),
        license=LICENSE,
        namespace_packages=findnamespaces(NS), # home for our libraries
        packages=find_packages(exclude=['tests']),
        author=AUTHOR,
        author_email=EMAIL,
        description=DESC,
        long_description=open('README.rst').read(),
        url=URL,
        classifiers=CLASS,
        keywords=TAGS,

        # run-time dependencies
        install_requires=REQUIRE,

        extras_require={
        },

        package_data={
        },

        data_files=[],

        entry_points={
        },
    )

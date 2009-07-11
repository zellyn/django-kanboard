import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-kanboard",
    version = "0.1",
    url = 'http://github.com/zellyn/django-kanboard',
    license = 'BSD',
    description = "A simple Kanban board for Django apps.",
    long_description = read('README.rst'),

    author = 'Zellyn Hunter',
    author_email = 'zellyn@gmail.com',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = ['setuptools'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business :: Groupware',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-urlmodel',
    version='0.12',
    packages=['urlmodel'],
    include_package_data=True,
    license='MIT',
    description='Rich URLs for Django models.',
    long_description=README,
    url='https://github.com/jleeothon/urlmodel',
    author='Johnny Lee',
    author_email='jleeothon@outlook.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['django'],
    tests_require=['django'],
)

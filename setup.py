from setuptools import setup
from rainbowtests import __version__

setup(
    name='django-rainbowtests',
    version=__version__,
    description="A colorful Django Test Runner.",
    long_description=open('README.rst').read(),
    author='Brad Montgomery',
    author_email='brad@bradmontgomery.net',
    url='https://github.com/bradmontgomery/django-rainbowtests',
    license='MIT',
    packages=['rainbowtests'],
    include_package_data=True,
    package_data={'': ['README.rst', 'LICENSE.txt']},
    zip_safe=False,
    install_requires=['django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

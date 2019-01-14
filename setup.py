"""
    Setup file for this module
"""
from setuptools import setup

setup(
    name='easy-kubernetes',
    version='0.1.0',
    packages=["easy_kubernetes"],
    url='https://github.com/GoDllkE/python-api-kubernetes',
    download_url=('https://github.com/GoDllkE/Easy-Kubernetes/archive/master.zip'),
    description='A python module to interact with kubernetes REST API.',
    author='Gustavo Toledo de Oliveira',
    author_email='gustavot53@gmail.com',
    keywords=[
        'kubernetes', 'origin', 'easy-kubernetes', 'kubernetes api',
        'python kubernetes', 'kubectl.py'
    ],
    install_requires=[
        'requests>=1.10.8'
    ],
    classifiers=[
        # Development status
        'Development Status :: 3 - Beta',

        # Intention
        'Intended Audience :: Developers',

        # Os requirement
        'Operating System :: OS Independent',

        # License
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Languages
        'Natural Language :: Portuguese (Brazilian)',

        # Supported versions
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only'
    ],
    project_urls={
        'Source': 'https://github.com/GoDllkE/python-api-kubernetes',
        'Documentation':
        'https://github.com/GoDllkE/python-api-kubernetes/docs',
        'Tracker': 'https://github.com/GoDllkE/python-api-kubernetes/issues'
    },
    long_description="""
    Easy-Kubernetes
========================
This module has purpose to create easy and fast ways to communicate with the API from kubernetes, allowing the developer to create and manage their own data with their own way. Python is a great language and very well used for DevOps Automantions. With it, creating a kubernetes module will easy many steps and automantions allowing a better infrastructure automation or management with great performance.
This version requires Python 3 or later; a Python 2 version is not available... yet.

Features
========================
- Handle kubernetes through your python script.
- Free to manage the data from kubernetes API on your own way.
- There's functions to manage it too, if you don't like the previous ideia.
- Simplify most of the kubernetes client functions to simple and unique interactions.
- Simple code, simple functions, simple management. Keep simple!

Installation
============
To install easy-kubernetes from PYPI:


    $ pip install easy-kubernetes

To install easy-kubernetes manually (please download the source code from either
PYPI_ or Github_ first):

    $ python setup.py install

Usage
========
To use easy-kubernetes, just import this module with:

    $ from kubernetes import kubernetes

Then, create a instance of the class with the functionality you desire:

    # Cria instancia com dados de acesso ao clusterK8s
    $ k8s_config = kubernetes.config(url=<k8s_master_url>, token=<serviceaccount_token>)
    
    # Cria instancia para funcionalidades prontas do k8s
    $ k8s_tools = kubernetes.tools()
    
    # Cria instancia com chamadas para REST API 
    $ k8s = kubernetes.core(configuration=k8s_config)

After this, you will be able to use and explore all functionalities.

Enjoy!


Citing
======
Please cite the following paper if you use easy-kubernetes in a published work:

Gustavo Toledo, Tiago Albuquerque. "Easy-Kubernetes: Improving kubernetes auto-management through Python 3", 2018

.. _PYPI: https://pypi.python.org/pypi/Easy-Kubernetes
.. _Github: https://github.com/GoDllkE/python-api-kubernetes
    """)
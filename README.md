Easy-Kubernetes
========================
Status: **[in development]**

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

    # Create an instance of k8s access data 
    $ k8s_config = kubernetes.config(url=<k8s_master_url>, token=<serviceaccount_token>)
    
    # Create an instance of k8s functionalities
    $ k8s_tools = kubernetes.tools()
    
    # Create an instance of k8s core functionalities (REST API calls) 
    $ k8s = kubernetes.core(configuration=k8s_config)

After this, you will be able to use and explore all functionalities. For example:

    # Retrieve all namespaces from clusterK8s
    print(k8s.get_namespaces())
    
Ou
    
    # Retrieve all pods from a certain namespace on clusterK8s
    print(k8s.get_pods('default')
    
Where, 'default' is a namespace inside the clusterK8s


Enjoy!


Citing
======
Please cite the following paper if you use easy-kubernetes in a published work:

Gustavo Toledo. "Easy-Kubernetes: Improving kubernetes auto-management through Python 3", 2019


PYPI: https://pypi.python.org/pypi/Easy-Kubernetes

Github: https://github.com/GoDllkE/python-api-kubernetes
    
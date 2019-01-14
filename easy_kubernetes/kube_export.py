import os
import sys
import json
import yaml
import base64
import getopt

# Suppress SSL Warning
import urllib3
urllib3.disable_warnings()

# Local import
from easy_kubernetes import kubernetes

# ----------------------------------------------------------------------------------------- #
# Control
verbose = False
environment = None

# Em casos de execução sem parametros
if len(sys.argv) <= 1:
    print("Erro: Parametro 'clusterk8s' não informado.")
    exit(0)

# ClusterK8s or some execution option
options, args = getopt.getopt(sys.argv[1:], 'v', ['clusterk8s=', 'verbose'])

for opt, value in options:
    if opt in ['--clusterk8s']:
        if 3 >= len(value) <= 4:
            environment = value
    elif opt in ['-v', '--verbose']:
        verbose = True
    else:
        continue

# Check clusterk8s parameter
if environment is None:
    print("Erro: Parametro 'clusterk8s' inválido ({0}).".format(environment))
    exit(0)

# Load content
file = None
if os.path.isfile('/etc/easy_kubernetes/token.yaml'):
    file = yaml.load(open('/etc/easy_kubernetes/token.yaml', 'r').read())
elif os.path.isfile('easy_kubernetes/easy_kubernetes/token.yaml'):
    file = yaml.load(open('easy_kubernetes/easy_kubernetes/token.yaml', 'r').read())
elif os.path.isfile('easy_kubernetes/token.yaml'):
    file = yaml.load(open('easy_kubernetes/token.yaml', 'r').read())
else:
    file = yaml.load(open('resources/token.yaml', 'r').read())

# Load configurations
url = file['clusters'][environment]['url']
token = file['clusters'][environment]['token']
service_account = file['clusters'][environment]['serviceaccount']

# Instantiate extension objects
k8s_tools = kubernetes.tools()
k8s_config = kubernetes.config(host=url, token=token)

# Instantiate core object
k8s = kubernetes.core(configuration=k8s_config)

# ----------------------------------------------------------------------------------------- #
# TODO
# Create output dict
data = dict()
data.setdefault('services', [])

# Start gathering valid namespaces
valid_namespaces = []
namespaces = k8s.get_namespaces()
for namespace in namespaces['items']:
    if 'liv' in namespace['metadata']['name'] or 'default' in namespace['metadata']['name']:
        valid_namespaces.append(namespace['metadata']['name'])

# Insert env-data into our dict output
env_data = k8s.get_configmap('default', 'env-data')
data['services'].append(dict(name='occ', type='occ', base_endpoint=env_data['data']['OCC_BASE_URL']))

# Start asking for applications (pod)
applications = []
for namespace in valid_namespaces:
    if verbose:
        print("{0}:".format(namespace))
    # Get all pods
    deployments = k8s.get_deployments(namespace)['items']

    # Get all secrets
    secrets = k8s.get_secrets(namespace)['items']

    for deployment in deployments:
        if verbose:
            print("\t{0}".format(deployment['metadata']['name']))
        # Retrieve ingress from pod name
        app_ingress = k8s.get_ingress(namespace, deployment['metadata']['name'])

        # Retrieve list of secrets from pod name
        secret_list = []
        for secret in secrets:
            if deployment['metadata']['name'] in secret['metadata']['name']:
                # Check secret type for specialized properties
                if 'db-oracle' in secret['metadata']['name']:
                    secret_list.append(dict(
                        type="db-oracle",
                        username=base64.b64decode(secret['data']['username']).decode("utf-8"),
                        password=base64.b64decode(secret['data']['password']).decode("utf-8"),
                        servicename=base64.b64decode(secret['data']['servicename']).decode("utf-8"),
                        host=base64.b64decode(secret['data']['host']).decode("utf-8"),
                        port=base64.b64decode(secret['data']['port']).decode("utf-8")
                    ))
                elif 'redis' in secret['metadata']['name']:
                    secret_list.append(dict(
                        type="redis",
                        username=base64.b64decode(secret['data']['username']).decode("utf-8"),
                        password=base64.b64decode(secret['data']['password']).decode("utf-8"),
                        host=base64.b64decode(secret['data']['host']).decode("utf-8"),
                        port=base64.b64decode(secret['data']['port']).decode("utf-8")
                    ))
                elif 'db-mongo' in secret['metadata']['name']:
                    secret_list.append(dict(
                        type="db-mongo",
                        username=base64.b64decode(secret['data']['username']).decode("utf-8"),
                        password=base64.b64decode(secret['data']['password']).decode("utf-8"),
                        database=base64.b64decode(secret['data']['database']).decode("utf-8"),
                        host=base64.b64decode(secret['data']['host']).decode("utf-8"),
                        port=base64.b64decode(secret['data']['port']).decode("utf-8")
                    ))
                elif 'rabbit-mq' in secret['metadata']['name']:
                    secret_list.append(dict(
                        type="redis",
                        username=base64.b64decode(secret['data']['username']).decode("utf-8"),
                        password=base64.b64decode(secret['data']['password']).decode("utf-8"),
                        host=base64.b64decode(secret['data']['host']).decode("utf-8"),
                        port=base64.b64decode(secret['data']['port']).decode("utf-8")
                    ))
                else:
                    # No inclusion at secret_list
                    continue
                # Secret type check end
            # Looping secrets
        # Secret_list generates

        # InnerJoin form pods to secrets

        # Missing property:
        # base_endpoint="{0}/{1}".format(app_ingress['spec']['rules'][0]['host'],app_ingress['spec']['rules'][0]['http']['paths'][0]['backend']['serviceName']),

        data['services'].append(dict(
            name=deployment['metadata']['name'],
            type='microservice',
            base_endpoint='<ingress-host>/<ingress-context>',
            resources=secret_list
        ))
        # End of input of microservice in data
    # End of looping deployments
# End of lopping namespaces

# ----------------------------------------------------------------------------------------- #
#
print(json.dumps(data, indent=2))
exit(0)

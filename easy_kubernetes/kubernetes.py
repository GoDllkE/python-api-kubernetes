import json
import requests


class tools:
    def __init__(self):
        pass

    def generate_configmap(self, name: str = None, content: dict = None):
        return dict(apiVersion='v1', kind="Configmap", items=content, metadata=dict(name=name))

    def generate_secret(self, name: str = None, content: dict = None):
        return dict(apiVersion='v1', kind='Secret', type='Opaque', data=content, metadata=dict(name=name))

    def generate_namespace(self, name: str = None):
        return dict(apiVersion='v1', kind='Namespace', metadata=dict(name=name))

    def generate_pod(self, name: str = None, content: dict = None):
        return dict(apiVersion='v1', kind='Pod', metadata=dict(name=name), spec=content)

    def generate_ingress(self, name: str = None, content: dict = None, status: dict = None):
        return dict(apiVersion='v1', kind='Ingress', metadata=dict(name=name), spec=content, status=status)


class config:
    def __init__(self, host: str = None, token: str = None):
        self.url = host
        self.token = token

    def get_url(self):
        return self.url.lower().strip(' ')

    def get_token(self):
        return self.token.strip(' ').strip('\n')


class core:
    def __init__(self, configuration: config = None):
        self.url = configuration.get_url()
        self.token = configuration.get_token()

    def __get_url(self, host: str = None):
        if host is None:
            return self.url
        else:
            return host.lower().strip(' ')

    def __get_token(self, token: str = None):
        if token is None:
            return self.token
        else:
            return token.strip(' ')

    # ============================================================================== #
    #   Methods/Functions                                                            #
    #   Where all the magic is located                                               #
    # ============================================================================== #
    #
    def api_comunicator(type_action):
        def action_decotator(func):
            def func_wrapper(*args):
                """
                    Decorator that ensurer the proper http method is made based on type_action parameter call.
                :param args: Receive N values, but only use those:
                    :host:          Receive a URL with host and context right to the endpoint desired
                    :token:         Receive a token for K8S REST API access.
                    :json_config:   When there's a need to pass a body content, use this parameter to send the body in
                    python dict form.
                :return: Return a dict
                """
                try:
                    host = func(*args)[1]
                    token = func(*args)[2]
                    json_config = func(*args)[3]

                    if type_action in ["get", "put", "patch", "post", "delete"]:
                        if type_action == "get":
                            header = {
                                'Accept': 'application/json',
                                'Authorization': 'Bearer {0}'.format(token)
                            }
                            response = requests.get(host, verify=False, headers=header)
                            return json.loads(response.content.decode('utf-8'))
                        elif type_action == "patch":
                            header = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/merge-patch+json',
                                'Authorization': 'Bearer {0}'.format(token)
                            }
                            response = requests.patch(host, verify=False, headers=header, json=json_config)
                            return json.loads(response.content.decode('utf-8'))
                        elif type_action == "put":
                            header = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {0}'.format(token)
                            }
                            response = requests.put(host, verify=False, headers=header, json=json_config)
                            return json.loads(response.content.decode('utf-8'))
                        elif type_action == "post":
                            header = {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer {0}'.format(token)
                            }
                            response = requests.post(host, verify=False, headers=header, json=json_config)
                            return json.loads(response.content.decode('utf-8'))
                        elif type_action == "delete":
                            pass
                    else:
                        print("==> Invalid type of action! ({0})".format(type_action))
                        exit(1)
                except (ConnectionError, TimeoutError, ValueError, SystemError) as corno:
                    print("==> Erro: {0}".format(corno))
                    exit(1)

            return func_wrapper

        return action_decotator

    # ============================================================================== #
    #   Resources
    # ============================================================================== #
    # Namespace
    #
    @api_comunicator("get")
    def get_namespace(self, namespace: str = None):
        host = '{0}/api/v1/namespaces/{1}'.format(self.__get_url(), namespace)
        return self, host, self.token, None

    @api_comunicator("get")
    def get_namespaces(self):
        host = '{0}/api/v1/namespaces'.format(self.__get_url())
        return self, host, self.token, None

    @api_comunicator("post")
    def create_namespace(self, namespace: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}'.format(self.__get_url(), namespace)
        return self, host, self.token, payload

    @api_comunicator("patch")
    def patch_namespace(self, namespace: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}'.format(self.__get_url(), namespace)
        return self, host, self.token, payload

    @api_comunicator("put")
    def replace_namespace(self, namespace: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}'.format(self.__get_url(), namespace)
        return self, host, self.token, payload

    @api_comunicator("delete")
    def delete_namespace(self, namespace: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}'.format(self.__get_url(), namespace)
        return self, host, self.token, payload

    # ============================================================================== #
    # Pod
    #
    @api_comunicator("get")
    def get_pod(self, namespace: str = None, pod: str = None):
        host = '{0}/api/v1/namespaces/{1}/pods/{2}'.format(self.__get_url(), namespace, pod)
        return self, host, self.token, None

    @api_comunicator("get")
    def get_pods(self, namespace: str = None):
        host = '{0}/api/v1/namespaces/{1}/pods'.format(self.__get_url(), namespace)
        return self, host, self.token, None

    @api_comunicator("post")
    def create_pod(self, namespace: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/pods'.format(self.__get_url(), namespace)
        return self, host, self.token, payload

    @api_comunicator("patch")
    def patch_pod(self, namespace: str = None, pod: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/pods/{2}'.format(self.__get_url(), namespace, pod)
        return self, host, self.token, payload

    @api_comunicator("put")
    def replace_pod(self, namespace: str = None, pod: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/pods/{2}'.format(self.__get_url(), namespace, pod)
        return self, host, self.token, payload

    @api_comunicator("delete")
    def delete_pod(self, namespace: str = None, pod: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/pods/{2}'.format(self.__get_url(), namespace, pod)
        return self, host, self.token, payload

    # ============================================================================== #
    # Ingress
    #
    @api_comunicator("get")
    def get_ingress(self, namespace: str = None, ingress: str = None):
        host = '{0}/apis/extensions/v1beta1/namespaces/{1}/ingresses/{2}'.format(self.__get_url(), namespace, ingress)
        return self, host, self.token, None

    @api_comunicator("get")
    def get_ingresses(self, namespace: str = None):
        host = '{0}/apis/extensions/v1beta1/namespaces/{1}/ingresses'.format(self.__get_url(), namespace)
        return self, host, self.token, None

    @api_comunicator("post")
    def create_ingress(self, namespace: str = None, payload: dict = None):
        host = '{0}/apis/extensions/v1beta1/namespaces/{1}/ingresses'.format(self.__get_url(), namespace)
        return self, host, self.token, payload

    @api_comunicator("patch")
    def patch_ingress(self, namespace: str = None, ingress: str = None, payload: dict = None):
        host = '{0}/apis/extensions/v1beta1/namespaces/{1}/ingresses/{2}'.format(self.__get_url(), namespace, ingress)
        return self, host, self.token, payload

    @api_comunicator("put")
    def replace_ingress(self, namespace: str = None, ingress: str = None, payload: dict = None):
        host = '{0}/apis/extensions/v1beta1/namespaces/{1}/ingresses/{2}'.format(self.__get_url(), namespace, ingress)
        return self, host, self.token, payload

    @api_comunicator("delete")
    def delete_ingress(self, namespace: str = None, ingress: str = None, payload: dict = None):
        host = '{0}/apis/extensions/v1beta1/namespaces/{1}/ingresses/{2}'.format(self.__get_url(), namespace, ingress)
        return self, host, self.token, payload

    # ============================================================================== #
    # Services
    #
    @api_comunicator("get")
    def get_service(self, namespace: str = None, service: str = None):
        host = '{0}/api/v1/namespaces/{1}/services/{2}'.format(self.__get_url(), namespace, service)
        return self, host, self.token, None

    @api_comunicator("get")
    def get_services(self, namespace: str = None):
        host = '{0}/api/v1/namespaces/{1}/services'.format(self.__get_url(), namespace)
        return self, host, self.token, None

    @api_comunicator("post")
    def create_service(self, namespace: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/services'.format(self.__get_url(), namespace)
        return self, host, self.token, payload

    @api_comunicator("patch")
    def patch_service(self, namespace: str = None, service: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/services/{2}'.format(self.__get_url(), namespace, service)
        return self, host, self.token, payload

    @api_comunicator("put")
    def replace_service(self, namespace: str = None, service: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/services/{2}'.format(self.__get_url(), namespace, service)
        return self, host, self.token, payload

    @api_comunicator("delete")
    def delete_service(self, namespace: str = None, service: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/services/{2}'.format(self.__get_url(), namespace, service)
        return self, host, self.token, payload

    # ============================================================================== #
    # Configmap
    #
    @api_comunicator("get")
    def get_configmap(self, namespace: str = None, configmap: str = None):
        host = '{0}/api/v1/namespaces/{1}/configmaps/{2}'.format(self.__get_url(), namespace, configmap)
        return self, host, self.token, None

    @api_comunicator("get")
    def get_configmaps(self, namespace: str = None):
        host = '{0}/api/v1/namespaces/{1}/configmaps'.format(self.__get_url(), namespace)
        return self, host, self.token, None

    @api_comunicator("post")
    def create_configmap(self, namespace: str = None, configmap: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/configmaps/{2}'.format(self.__get_url(), namespace, configmap)
        return self, host, self.token, payload

    @api_comunicator("patch")
    def patch_configmap(self, namespace: str = None, configmap: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/configmaps/{2}'.format(self.__get_url(), namespace, configmap)
        return self, host, self.token, payload

    @api_comunicator("put")
    def replace_configmap(self, namespace: str = None, configmap: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/configmaps/{2}'.format(self.__get_url(), namespace, configmap)
        return self, host, self.token, payload

    @api_comunicator("delete")
    def delete_configmap(self, namespace: str = None, configmap: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/configmaps/{2}'.format(self.__get_url(), namespace, configmap)
        return self, host, self.token, payload

    # ============================================================================== #
    # Secret
    #
    @api_comunicator("get")
    def get_secret(self, namespace: str = None, secret: str = None):
        host = '{0}/api/v1/namespaces/{1}/secrets/{2}'.format(self.__get_url(), namespace, secret)
        return self, host, self.token, None

    @api_comunicator("get")
    def get_secrets(self, namespace: str = None):
        host = '{0}/api/v1/namespaces/{1}/secrets'.format(self.__get_url(), namespace)
        return self, host, self.token, None

    @api_comunicator("post")
    def create_secret(self, namespace: str = None, secret: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/secrets/{2}'.format(self.__get_url(), namespace, secret)
        return self, host, self.token, payload

    @api_comunicator("patch")
    def patch_secret(self, namespace: str = None, secret: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/secrets/{2}'.format(self.__get_url(), namespace, secret)
        return self, host, self.token, payload

    @api_comunicator("put")
    def replace_secret(self, namespace: str = None, secret: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/secrets/{2}'.format(self.__get_url(), namespace, secret)
        return self, host, self.token, payload

    @api_comunicator("delete")
    def delete_secret(self, namespace: str = None, secret: str = None, payload: dict = None):
        host = '{0}/api/v1/namespaces/{1}/secrets/{2}'.format(self.__get_url(), namespace, secret)
        return self, host, self.token, payload

    # ============================================================================== #
    # Deployment
    #
    @api_comunicator("get")
    def get_deployment(self, namespace: str = None, deployment: str = None):
        host = '{0}/apis/apps/v1/namespaces/{1}/deployments/{2}'.format(self.__get_url(), namespace, deployment)
        return self, host, self.token, None

    @api_comunicator("get")
    def get_deployments(self, namespace: str = None):
        host = '{0}/apis/apps/v1/namespaces/{1}/deployments'.format(self.__get_url(), namespace)
        return self, host, self.token, None

    @api_comunicator("post")
    def create_deployment(self, namespace: str = None, payload: dict = None):
        host = '{0}/apis/apps/v1/namespaces/{1}/deployments'.format(self.__get_url(), namespace)
        return self, host, self.token, payload

    @api_comunicator("patch")
    def patch_deployment(self, namespace: str = None, deployment: str = None, payload: dict = None):
        host = '{0}/apis/apps/v1/namespaces/{1}/deployments/{2}'.format(self.__get_url(), namespace, deployment)
        return self, host, self.token, payload

    @api_comunicator("put")
    def replace_deployment(self, namespace: str = None, deployment: str = None, payload: dict = None):
        host = '{0}/apis/apps/v1/namespaces/{1}/deployments/{2}'.format(self.__get_url(), namespace, deployment)
        return self, host, self.token, payload

    @api_comunicator("delete")
    def delete_deployment(self, namespace: str = None, pod: str = None, payload: dict = None):
        host = '{0}/apis/apps/v1/namespaces/{1}/deployments/{2}'.format(self.__get_url(), namespace, pod)
        return self, host, self.token, payload

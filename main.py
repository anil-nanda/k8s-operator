import kopf
import pykube


# @kopf.on.login()
# def custom_login_fn(**kwargs):
#     """
#     The custom_login_fn function is used to determine how the operator will authenticate with the Kubernetes API.
#     If we are running in a development environment, then we want to use our local kubeconfig file.
#     Otherwise, if we are running in a production environment (i.e., on OpenShift), then we want to use the service account token.
#     :param **kwargs: Pass a variable number of keyword arguments to the function
#     :return: A function
#     """
#     if EnvConfig.ENV == "dev":
#         return kopf.login_with_kubeconfig(**kwargs)
#     else:
#         return kopf.login_with_service_account(**kwargs)
@kopf.on.create("pluto.dev.io", "v1alpha1", "microservices")
def create_fn(spec, **kwargs):
    kube_api = pykube.HTTPClient(pykube.KubeConfig.from_file())
    deployment = pykube.Deployment(kube_api, {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'spec': {
            'replicas': spec['replicas'],
            'selector': {
                'matchLabels': spec['labels'],
            },
            'template': {
                'metadata': {
                    'labels': spec['labels'],
                },
                'spec': {
                    'containers': [
                        {
                            'name': kwargs['body']['metadata']['name'],
                            'image': spec['image'],
                            'env': spec.get('env', []),
                        },
                    ],
                },
            },
        },
    })
    kopf.adopt(deployment)
    deployment.create()
    return {'message': 'Deployment created'}

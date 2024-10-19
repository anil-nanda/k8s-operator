import kopf
import pykube


@kopf.on.login()
def custom_login_fn(**kwargs):
    """
    The custom_login_fn function is used to determine how the operator will authenticate with the Kubernetes API.
    If we are running in a development environment, then we want to use our local kubeconfig file.
    Otherwise, if we are running in a production environment (i.e., on OpenShift), then we want to use the service account token.

    :param **kwargs: Pass a variable number of keyword arguments to the function
    :return: A function
    """
    if EnvConfig.ENV == "dev":
        return kopf.login_with_kubeconfig(**kwargs)
    else:
        return kopf.login_with_service_account(**kwargs)

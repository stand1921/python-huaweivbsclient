"""OpenStackClient plugin for Huawei VBS Service."""


from osc_lib import utils


DEFAULT_API_VERSION = '1'
API_VERSION_OPTION = 'os_huaweivbs_api_version'
API_NAME = 'huaweivbs'
API_VERSIONS = {
    '1': 'huaweivbsclient.client_v1.Client',
}
ENDPOINT = 'https://vbs.cn-north-1.myhwclouds.com'


def make_client(instance):
    """Returns a Huawei VBS service client."""
    tenant_id = instance._auth_ref._data['token']['project']['id']
    token = instance._auth_ref.auth_token

    version = instance._api_version[API_NAME]
    try:
        version = int(version)
    except ValueError:
        version = float(version)

    client = utils.get_client_class(
        API_NAME,
        version,
        API_VERSIONS)
    instance.setup_auth()
    return client(
        token=token,
        tenant_id=tenant_id,
        endpoint=ENDPOINT)


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-huaweivbs-api-version',
        metavar='<huaweivbs-api-version>',
        default=utils.env(
            'OS_HUAWEIVBS_API_VERSION',
            default=DEFAULT_API_VERSION),
        help=('Huawei VBS API version, default=' +
              DEFAULT_API_VERSION +
              ' (Env: OS_HUAWEIVBS_API_VERSION)'))
    return parser

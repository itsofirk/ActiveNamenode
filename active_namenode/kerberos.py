from os import environ
from sys import platform
from base64 import b64decode
from subprocess import Popen, PIPE
from requests_kerberos import HTTPKerberosAuth, DISABLED

DEFAULT_KRB5_LOCATION = '/etc/krb5.conf'


def set_credentials(principal, b64_password, krb5_location=DEFAULT_KRB5_LOCATION):
    """
    this function performs a `kinit` with the given user
    :param principal: e.g. username@domain.dom
    :param b64_password: base64 encoded password
    :param krb5_location: kerberos config file
    :return void
    """
    environ['KRB5_CONFIG'] = krb5_location
    kinit = Popen(['kinit', principal], stdin=PIPE)
    kinit.communicate(b64decode(b64_password))


def get_token(principal, b64_password, krb5_location=DEFAULT_KRB5_LOCATION):
    if platform == 'win32':
        return HTTPKerberosAuth(
            principal=f'{principal}:{b64decode(b64_password)}',
            mutual_authentication=DISABLED, force_preemptive=True)
    else:
        set_credentials(principal, b64_password, krb5_location)
        return HTTPKerberosAuth(principal=principal, mutual_authentication=DISABLED)

from application.external_sources.email.client import EmailClient
from application.external_sources.smsc.client import SMSCClient
from application.external_sources.wapico.client import WapicoClient


def get_email_client() -> EmailClient:
    return EmailClient()


def get_smsc_client() -> SMSCClient:
    return SMSCClient()


def get_wapico_client() -> WapicoClient:
    return WapicoClient()

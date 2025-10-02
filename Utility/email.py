import json

import requests
from Utility import Helper
from Utility import configs


def send_template_mail(to: list[str], subject: str, content_variables: dict[str, str], template_id: int,
                       cc: list[str] = None) -> int:
    """ **Sending pre-build template e-mail **

    :param subject: email subject
    :param template_id: template id, see WorkFlowEngine app -> emailtemplate table
    :param content_variables: dictionary of template variables
    :param cc: list of username
    :param to: list of username
    :return: http status code
    """

    # checking inputs
    for username in to:
        assert isinstance(username, str)
        assert username is not None

    if cc:
        for username in cc:
            assert isinstance(username, str)
            assert username is not None

    assert isinstance(subject, str)
    assert subject is not None

    assert isinstance(content_variables, dict)

    # An empty dictionary is not a problem
    for key, value in content_variables.items():
        assert isinstance(key, str)
        assert isinstance(value, str)

    assert template_id is not None
    assert isinstance(template_id, int)

    # making email addresses
    domain = configs.Miscellaneous.EIT_EMAIL_DOMAIN
    to_emails_address = [f"{Helper.FixUsername(username, False, True).username}{domain}" for username in to]

    cc_emails_address = None
    if cc:
        cc_emails_address = [f"{Helper.FixUsername(username, False, True).username}{domain}" for username in cc]

    url = configs.SEND_MAIL("TEST_SERVER", template_id)
    payload = {
        "to"               : to_emails_address,
        "cc"               : cc_emails_address,
        "subject"          : subject,
        "content-variables": content_variables,
    }

    # api
    req = requests.post(
        url,
        data={
            "data": json.dumps(payload)
        }
    )
    return req.status_code

# servers
servers = {
    "TEST_SERVER": "192.168.20.52",
    "MAIN_SERVER": "192.168.20.81",
    "ERFAN" :"192.168.70.100",
}


class Miscellaneous:
    """miscellaneous"""
    EIT_EMAIL_DOMAIN = "@iraneit.com"


class Port:
    """projects ports
    notice that project's ports in TEST_SERVER and MAIN_SERVER
    are the same"""
    PROCESS_MANAGEMENT_PORT = "50000"
    DOCUMENTATION_PORT = "27000"
    PORTAL = "23000"
    # test purposes
    TEMP_PORT = "12000"
    HR = "14000"


# api uri
SEND_MAIL = lambda server, template_id: f"http://{servers.get(server)}:{Port.PROCESS_MANAGEMENT_PORT}/ProcessManagement/WorkflowEngine/api/templates/{template_id}/send-email/"
INSERT_ARTICLE = lambda server: f"http://{servers.get(server)}:{Port.DOCUMENTATION_PORT}/KMS/api/v1/article"
DELETE_ARTICLES = lambda server: f"http://{servers.get(server)}:{Port.DOCUMENTATION_PORT}/KMS/api/v1/article/delete-articles-start-with"
GET_ARTICLES_ENGLISH_TITLE_START_WITH = lambda server, pattern: f"http://{servers.get(server)}:{Port.DOCUMENTATION_PORT}/KMS/api/v1/article/articles-start-with/{pattern}"
UPDATE_ARTICLE_CONTENT = lambda server: f"http://{servers.get(server)}:{Port.DOCUMENTATION_PORT}/KMS/api/v1/article"
PUT_DOCUMENT = lambda server: f"http://{servers.get(server)}:{Port.PORTAL}/Cartable/api/v1/documents/"
PUT_DOCUMENT_FLOW = lambda server: f"http://{servers.get(server)}:{Port.PORTAL}/Cartable/api/v1/document-flows/"
TEAMS = lambda server: f"http://{servers.get(server)}:{Port.HR}/HR/api/v1/teams/"
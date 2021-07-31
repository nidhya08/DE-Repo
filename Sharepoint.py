# Import required packages
import sys
import requests
import os

# from requests_ntlm import HttpNtlmAuth
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

# Read filename (relative path) from command line
fileName = sys.argv[1]
username = os.environ['office365_username']
password = os.environ['office365_password']

# Enter your SharePoint site and target library
sharePointUrl = os.environ['sharepoint_url']
folderUrl = os.environ['office365_id']

# Sets up the url for requesting a file upload
requestUrl = sharePointUrl + '/_api/web/getfolderbyserverrelativeurl(\'' + folderUrl + '\')/Files/add(url=\'' + fileName + '\',overwrite=true)'

# Read in the file that we are going to upload
file = open(fileName, 'rb')
ctx_auth = AuthenticationContext(url=requestUrl)
if ctx_auth.acquire_token_for_user(username=username,
                                   password=password):
    ctx = ClientContext(requestUrl, ctx_auth)
    target_list = ctx.web.lists.get_by_title("Documents")
    info = FileCreationInformation()
    file_name = "Book.xlsx"
    path = "{0}/data/{1}".format(os.path.dirname(__file__), file_name)
    with open(path, 'rb') as content_file:
        info.content = content = content_file.read()
    info.url = file_name
    info.overwrite = True
    upload_file = target_list.root_folder.files.add(info)
    ctx.execute_query()
uploadResult = requests.post(requestUrl, auth=HttpNtlmAuth('Domain\\' + username, password), headers=headers,
                             data=file.read())

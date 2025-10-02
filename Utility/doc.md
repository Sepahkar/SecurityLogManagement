# Utility Component Documentation

## Introduction

In the codebase, there is a module called `Utility` that is used across all services to provide common functionalities such as authentication, API service calls, and more. This module contains reusable functions that help streamline development and ensure consistency across the project.

## Usage

To use the `Utility` module, you need to import the required functions from the appropriate path.

### Authentication related funcitons package

Here is and example of what you need to import for authenticate and authorize a user

first in your view file import the following,

```python
# app/views.py
from Utility.Authentication.Utils import (
    V1_PermissionControl as permission_control,
    V1_get_data_from_token as get_token_data,
    V1_find_token_from_request as find_token
  
)
```

`permission_control`: This function is used as a decorator to control access to specific functions(Django Views). It ensures that only authorized users can access certain endpoints or functionalities.

`get_token_data`: This function is used to extract data from the authentication token. For example, you can retrieve the username, email, full name, and other related information from the token.

`find_token`: This function is used to locate the authentication token from the incoming request. The token is typically found in the request headers, and this function extracts and returns it.

#### Example Usage

Below is an example of how to use the above functions in a function called auth_gateway:

```python
@permission_control
def auth_gateway(request):
    
    token = find_token(request)
    personnel = get_token_data(token, "username")
    picture_name = get_token_data(token, "user_user_image_name")
    email = get_token_data(token, "user_Email").lower()
    full_name = get_token_data(token, "user_FullName")
    is_admin = False
    profile = profile_url(picture_name)

    personnel_user_record = User.objects.filter(Personnel=personnel).first()
```

#### Code Explanation

`token = find_token(request)`:
This line extracts the authentication token from the incoming request.

`personnel = get_token_data(token, "username")`:
This line retrieves the username from the token.

`picture_name = get_token_data(token, "user_user_image_name")`:
This line retrieves the user's profile picture name from the token.

`email = get_token_data(token, "user_Email").lower()`:
This line retrieves the user's email address from the token and converts it to lowercase.

`full_name = get_token_data(token, "user_FullName")`:
This line retrieves the user's full name from the token.

`is_admin = False`:
This line defines a boolean variable to check whether the user is an administrator.

`profile = profile_url(picture_name)`:
This line constructs the URL for the user's profile picture.


#### Additional Information

For more details about what data is returned by the find_token_from_Data function and the keys of the returned data, refer to the relevant module.




### APIManager Package Documentation


The `APIManager` package provides various functionalities for managing documents and user information within the system. It includes submodules for Portal and HR operations. Below is a detailed description of the operational functions available in each submodule.

#### Portal Submodule

##### `register_document.py`

- **Function: `v1`**
  - **Description**: Registers a document with the given parameters and returns a dictionary containing the document details.
  - **Parameters**:
    - `app_doc_id` (int): Application Document ID.
    - `priority` (str): Priority of the document.
    - `doc_state` (str): State of the document.
    - `document_title` (str): Title of the document.
    - `app_code` (str): Application code.
    - `owner` (str): Owner of the document.
  - **Returns**: A dictionary with a success message and document data.

##### `send_document.py`

- **Function: `ver1`**
  - **Description**: Sends a document to specified inbox owners and returns a dictionary with the status for each recipient.
  - **Parameters**:
    - `doc_id` (int): Document ID.
    - `sender` (str, optional): Sender's email. Default is "e.rezaee@eit".
    - `inbox_owners` (list[str], optional): List of recipient emails. Default is `["m.sepahkar@eit", "a.ahmadi@eit"]`.
  - **Returns**: A dictionary with the status and data for each inbox owner.

##### `update_document.py`

- **Function: `v1`**
  - **Description**: Updates document fields for a given document ID.
  - **Parameters**:
    - `doc_id` (int): Document ID.
    - `doc_fields` (dict): Dictionary of document fields to update.
  - **Returns**: Updated document data (Here for mocking purposes just return True).

##### `update_document_flow.py`

- **Function: `v1`**
  - **Description**: Updates document flow fields for a given document flow ID.
  - **Parameters**:
    - `doc_flow_id` (int): Document Flow ID.
    - `doc_flow_fields` (dict): Dictionary of document flow fields to update.
  - **Returns**: Updated document flow data (Here for mocking purposes just return True).

#### HR Submodule

##### `get_all_roles.py`

- **Function: `v1`**
  - **Description**: Returns a list of all roles with detailed information.
  - **Returns**: A list of dictionaries, each containing role details such as RoleId, RoleName, and other attributes.

##### `get_all_user.py`

- **Function: `v3`**
  - **Description**: Returns minimal information for all users, optimized for speed.
  - **Returns**: A list of dictionaries with UserName, FullName, and StaticPhotoURL.

##### `get_multiple_user_info.py`

- **Function: `v1`**
  - **Description**: Retrieves detailed information for multiple users.
  - **Parameters**:
    - `users` (list, optional): List of usernames. Default is `["m.sepahkar", "e.rezaee"]`.
  - **Returns**: A list of dictionaries with detailed user information.

##### `get_single_user_info.py`

- **Function: `v1`**
  - **Description**: Retrieves simple information for a single user.
  - **Parameters**:
    - `username` (str, optional): Username. Default is "m.sepahkar@eit".
  - **Returns**: A dictionary with simple user information.

##### `get_single_user_full_info.py`

- **Function: `v1`**
  - **Description**: Retrieves full information for a single user.
  - **Parameters**:
    - `username` (str, optional): Username, with or without `@eit`. The function will handle it.
  - **Returns**: A dictionary with the user's full information, including personal details, phone numbers, team roles, and educational history .

##### `get_team_manager.py`

- **Function: `v2`**
  - **Description**: Retrieves the manager of a specified team.
  - **Parameters**:
    - `teamcode` (str, optional): Team code. Default is "MIS".
    - `ManagerType` (str, optional): Type of manager to retrieve. Default is "GeneralManager".
  - **Returns**: The manager's email address.

##### `get_teams.py`

- **Function: `v1`**
  - **Description**: Returns a static list of teams for testing purposes.
  - **Parameters**:
    - `active_in_service` (bool, optional): Filter for active in service. Default is `True`.
    - `active_in_evaluation` (bool, optional): Filter for active in evaluation. Default is `True`.
  - **Returns**: A list of dictionaries with team data.

- **Function: `v2`**
  - **Description**: Retrieves team data using the HR API.
  - **Parameters**:
    - `active_in_service` (bool): Is active in book service?
    - `active_in_evaluation` (bool): Is active in evaluation?
  - **Returns**: A list of dictionaries with team data.

#### Alerts

- **Non-Operational Functions**: Several functions in the module are marked with `raise Exception("DO NOT USE")`. These functions are not operational and should not be used in production code.


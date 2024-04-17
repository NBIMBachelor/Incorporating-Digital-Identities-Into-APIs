# Incorporating-Digital-Identities-Into-APIs

## Entra-ID setup
**Prerequisites:**
- Entra account.
- Three groups: Admin, Developers and Financial Staff.
- Privileges to create new app registrations. 

**Setup:** \
The following setup has to be repeated for each group in Entra, give names fitting to the groups.
1. Go to `Applications` -> `App registrations` -> `New registration`. Give the registration a name, leave `Supported account types` at default value. In `Redirect URI` set platform to `Web` and the URL to `https://oauth.pstmn.io/v1/callback`. Then press `register`.
2. In the new tab select `Manifest`. Change `"accessTokenAcceptedVersion": null`, to `"accessTokenAcceptedVersion": 2` and press `Save`.
4. Next is to expose the API and add a scope, go to `Expose an API` and press `Add a scope`, then press `save and continue`, leaving the default value as is. Give the scope a name (which matches the scope set in the AWS authorizer for Admins: scope.admin, Developers: scope.dev and Financial Staff: scope.finance), description, admin consent, and set who can consent to `Admins and users`, finally click `Add scope`.
6. Go to `Certificates & Secrets` -> `Client secrets` -> `New client secret`, give a description, and leave the rest as is. Note down the value of the secret, as it cannot be checked later.
7. Go to `Applications` -> `Enterprise applications` -> `name of Application just created` -> `Users and groups` -> `Add user/group` -> under `Users and groups` press `None Selected` and add the group that matches the scope for this application, press `Select` and then `Assign`.
8. Go to `Properties` and set `Assignment required?` to `yes` -> `Save`.

##Information needed from Entra setup for AWS setup and requesting tokens:
1. For each of the three apps, go to `Applications` -> `App registrations` -> Select the app in question and note down the `Application (client) ID` (This will be used as the audience for the AWS JWT authorizer and for getting a token).
2. For one of the apps, go to `Applications` -> `App registrations` -> Select one of the apps and note down the  `Directory (tenant) ID` (This will be used as the issuer for the AWS JWT authorizer and for getting a token. They all have the same Directory ID)
3. For each of the three apps, go to `Applications` -> `App registrations` -> Select the app in question -> `Expose an API` and copy the value of the scope.

## AWS setup
**Prerequisites:**
-  AWS Account.
-  Permissions to create resources.
-  Application (Client) ID from the 3 Entra apps.
-  Directory (tenant) ID from one of the apps

**Setup:**
1. Download the CloudFormation template from this repo.
3. Go to CloudFormation in AWS and make sure it is set to  region: `US East(N. Virginia) us-east-1`, as the CloudFront part of the CloudFormation template is only supported in this region.
4. Select `Create stack` -> `Upload a template file` -> `Choose file` and select the downloaded CloudFormation template -> `Next`.
5. Enter a stack name as you wish and select `Next`.
6. Fill out the parameter fields with the information they ask for and select `Next`.
7. Select `Submit`.

## Getting a token
**Prerequisites:**
- Have Postman installed.

1. In Postman go to the `Authorization` tab.
2. For `Type` select `OAuth 2.0`.
3. Make sure `Grant Type` is set to `Authorization Coode`
4. Make sure the `Authorize using browser` is checked.
5. In `Auth URL` input https://login.microsoftonline.com/<Directory (tenant) ID>/oauth2/v2.0/authorize
6. In `Access Token URL` input https://login.microsoftonline.com/<Directory (tenant) ID>/oauth2/v2.0/token
7. In `Client ID` input the Application (Client) ID for the application you want a token from (If you want a token that can access the endpoint for Financial Staff, use the Client ID from the Financial Staff app).
8. In `Client Secret` input the client secret that was saved from earlier for the application you want a token from (If you want a token that can access the endpoint for Financial Staff, use the scope and Client ID from the Financial Staff app).
9. In `Scope`input the scope for the application you want a token from (If you want a token that can access the endpoint for Financial Staff, use the Client ID from the Financial Staff app).
10. Press `Get New Access Token` and follow the authentication process. When the authentication process is finished a token should be given. Note down the token.

## Using the API
**Prerequisites:**
- An access token from the step above.

1. To find the URL for the API go to CloudFront in AWS, select the CloudFront distribution and copy the URL under `Distribution domain name`.
2. In Postman make a new GET request using the URL just found. Append one of the three endpoints to the URL: /transactions, /employees or /devprojects. The access for the different endpoints are as shown in the table.

| Group            | devprojects         | employees           | transactions        |
|------------------|---------------------|---------------------|---------------------|
| Admin            | :heavy_check_mark:  | :heavy_check_mark:  | :heavy_check_mark:  |
| Developer        | :heavy_check_mark:  | :x:                 | :x:                 |
| Financial Staff  | :x:                 | :x:                 | :heavy_check_mark:  |

3.  In the `Header` tab add a header called `Authorization` and add the access token obtained earlier as the `Value`.
4.  Then press `Send` to send the request.

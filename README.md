# Incorporating Digital Identities Into APIs

This guide provides a setup for integrating digital identities into API authentication and authorisation using AWS and Entra ID

## Table of Contents
- [Entra ID Setup](#entra-id-setup)
  - [Prerequisites](#prerequisites)
  - [Setup for End Users](#setup-for-end-users)
  - [Setup for Machine-Machine](#setup-for-machine-machine)
- [Information needed from Entra setup for AWS setup and requesting tokens](#information-needed-from-Entra-setup-for-AWS-setup-and-requesting-tokens)
- [AWS setup](#aws-setup)
- [Getting a token](#getting-a-token)
  - [End users](#end-users)
  - [Machine-Machine](#machine-machine)
- [Using the API](#using-the-api)

## Entra-ID setup

### Prerequisites
- An active Entra account.
- Three groups: Admin, Developers, and Financial Staff.
- Permissions to create app registrations.
- A subscription to Workload Identities.

### Setup for End Users
Repeat these steps for each user group, adjusting names and scopes appropriately:
1. **App Registration**:
   - Navigate to `Applications` -> `App registrations` -> `New registration`.
   - Name your registration.
   - Under `Select platform` select `Web`, and the URL to `https://oauth.pstmn.io/v1/callback`.
   - Click `Register`.
2. **Edit Manifest**:
   - In the application tab go to `Manifest`
   - Change `"accessTokenAcceptedVersion": null` to `"accessTokenAcceptedVersion": 2`.
   - Click `Save`.
3. **API Exposure and Scope**:
   - Under `Expose an API` -> `Add a scope` -> `Save and continue`.
   - Give the scope a name based on the group.
      - For admin: scope.admin.
      - For developers: scope.dev.
      - For financial staff: scope.finance.
   - Set `Who can consent?` to `Admins and Users`.
   - For the rest of the mandatory fields type something that fits.
   - Click `Add scope`
4. **Client Secrets**:
   - Go to `Certificates & Secrets` ->  `New client secret`.
   - Give the secret a fitting name.
   - Click `Add`
   - Save the generated secret as it's shown only once.
5. **User and Group Assignments**:
   - Go to `Applications` -> `Enterprise applications` -> name of Application just created -> `Users and groups` -> `Add user/group` -> `None Selected`.
   - Select the correct group according to the current application. For the admin application choose the admin group and so on. Then click `Assign`.
   - Go to `Properties` and set `Assignment required?` to `Yes` then click `Save`.

### Setup for Machine-Machine
1. **App Registration**:
   - Navigate to `Applications` -> `App registrations` -> `New registration`.
   - Name your registration. Leave everything else at default values.
   - Click `Register`.
2. **Edit Manifest**:
   - In the application tab go to `Manifest`
   - Change `"accessTokenAcceptedVersion": null` to `"accessTokenAcceptedVersion": 2`.
   - Click `Save`.
3. **API Exposure and Scope**:
   - Under `Expose an API` -> `Add a scope` -> `Save and continue`.
   - Leave everything else at default. No need to fill out the name and other details that it asks for.
4. **Client Secrets**:
   - Go to `Certificates & Secrets` ->  `New client secret`.
   - Give the secret a fitting name.
   - Click `Add`
   - Save the generated secret as it's shown only once.
5. **Conditional Access**:
   - Go to `Protection` -> `Conditional Access` -> `Named Location` -> `+ IP ranges location`
   - Give the location a name and make sure `Mark as trusted location` is selected.
   - Click the `+` and add a IPv4 and IPv6 address that fits for the machine that will be requesting tokens from the application. In our case 129.240.0.0/15 and 2001:0700:0300:0000:0000:0000:0000:0000/44 was used, being NTNU's subnets. Then press `Create`.
   - Go to `Overview` -> `Create new policy`.
   - Give it a name.
   - Under `Users or workload identites` select `Workoad identitites` in the drop down menu. Check the box for `Select service principals` and under select choose the name of the application created in the steps above.
   - Under `Target resources` select `All cloud apps`.
   - Under `Conditions` -> `Locations` set `Configure` to yes and under `Exclude` add the location made in the earlier steps.
   - Under `Grant` select `Block access`.
   - Set `Enable policy` to On and click `Create`.

## Information needed from Entra setup for AWS setup and requesting tokens
1. For each of the four apps, go to `Applications` -> `App registrations` -> Select the app in question and note down the `Application (client) ID` (This will be used as the audience for the AWS JWT authorizer and for getting a token).
2. For one of the apps, go to `Applications` -> `App registrations` -> Select one of the apps and note down the  `Directory (tenant) ID` (This will be used as the issuer for the AWS JWT authorizer and for getting a token. All the APPs have the same Directory ID).
3. For each of the three end-user apps, go to `Applications` -> `App registrations` -> Select the app in question -> `Expose an API` and copy the scope value.
4. For the machine-machine app, go to `Applications` -> `App registrations` and note down the value in the `Application ID URI`.

## AWS setup
### Prerequisites
-  AWS Account with permissions to create resources.
-  Application (Client) ID from the 4 Entra apps.
-  Directory (tenant) ID from one of the apps.

### Setup
1. Download the CloudFormation template from this Git repository.
3. Go to CloudFormation in AWS and make sure region is set to: `US East(N. Virginia) us-east-1`, as the CloudFront part of the CloudFormation template is only supported in this region.
4. Select `Create stack` -> `Upload a template file` -> `Choose file` and select the downloaded CloudFormation template -> `Next`.
5. Enter a stack name as you wish.
6. Fill out the parameter fields with the information that is asked for and select `Next`.
7. Select `Submit`.

## Getting a token
### Prerequisites
- Have Postman or other tool to request tokens. (This guide shows how to do it with postman)

**End users**
1. In Postman, go to the `Authorization` tab.
2. For `Type` select `OAuth 2.0`.
3. Make sure `Grant Type` is set to `Authorization Code`
4. Make sure the `Authorize using browser` is checked.
5. In `Auth URL` input https://login.microsoftonline.com/<Directory (tenant) ID>/oauth2/v2.0/authorize
6. In `Access Token URL` input https://login.microsoftonline.com/<Directory (tenant) ID>/oauth2/v2.0/token
7. In `Client ID` input the Application (Client) ID for the application you want a token from (If you want a token that can access the endpoint for Financial Staff, use the Client ID from the Financial Staff app).
8. In `Client Secret` input the client secret that was saved from earlier for the application you want a token from (If you want a token that can access the endpoint for Financial Staff, use the scope and Client ID from the Financial Staff app).
9. In `Scope` input the scope for the application you want a token from (If you want a token that can access the endpoint for Financial Staff, use the Client ID from the Financial Staff app).
10. Press `Get New Access Token` and follow the authentication process. When the authentication process is finished, a token should be given. Note down the token.

**Machine-Machine**
1. Make a POST request in Postman.
2. Under `Body` select `x-www-form-urlencoded`.
3. 1. Add a new field called `grant_type` with the value `client_credentials`.
   2. Add a new field called `client_id` in the value add the Application (client) ID for the machine-machine application.
   3. Add a new field called `client_secret` in the value add the client secret for the machine-machine application.
   4. Add a new field called `scope` in the value add the Application ID URI gotten from the machine-machine application.
4. Press `Send` to get an access token. 

## Using the API
**Prerequisites:**
- An access token from the step above.

1. To find the URL for the API, go to CloudFront in AWS, select the CloudFront distribution and copy the URL under `Distribution domain name`.
2. In Postman, make a new GET request using the URL just found. Append one of the three endpoints to the URL: /transactions, /employees or /devprojects. The access for the different endpoints are as shown in the table.

| Group            | /devprojects        | /employees          | /transactions       | /schedule           |
|------------------|---------------------|---------------------|---------------------|---------------------|
| Admin            | :heavy_check_mark:  | :heavy_check_mark:  | :heavy_check_mark:  | :x: 
| Developer        | :heavy_check_mark:  | :x:                 | :x:                 | :x: 
| Financial Staff  | :x:                 | :x:                 | :heavy_check_mark:  | :x: 
| Machine          | :x:                 | :x:                 | :x:                 | :heavy_check_mark:  

3.  In the `Header` tab, add a header called `Authorization` and add the access token obtained earlier as the `Value`.
4.  Then press `Send` to send the request.

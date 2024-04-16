# Incorporating-Digital-Identities-Into-APIs

## AWS setup

## Entra-ID setup
**Prerequisites:**
- Entra account.
- Groups within Entra that can be assigned to different applications to limit who can access them.
- Admin privileges. 

**Setup:**
1. Go to `Applications` -> `App registrations` -> `New registration`. Give the registration a name, leave Supported accounts at default value. In `Redirect URI` set platform to `Web` and the URL to `https://oauth.pstmn.io/v1/callback`. Then finally register.
2. In the new tab select `Manifest`. Change `"accessTokenAcceptedVersion": null`, to `"accessTokenAcceptedVersion": 2`.
4. Next is to add a scope, go to `Expose an API` and press `Add a scope`, then press `save and continue`, leaving the default value as is.
5. To create a scope go to `Expose an API`, select `Add scope`. Give the scope a name (which matches AWS endpoint that the scope should work for), description, admin consent, and set who can consent to Admins and users.
6. Go to `Certificates & Secrets` -> `Client secrets` -> `New client secret`, give a description, and leave the rest as is. Note down the value of the secret as it cannot be checked later.
7. Go to `Applications` -> `Enterprise applications` -> `name of Application` just created -> `Users and groups` -> `Add user/group` and add the group that matches the scope for this app.
8. Go to `Applications` -> `Enterprise applications` -> `name of Application` just created -> `Properties` and set `Assignment required?` to `yes`.

This needs to be repeated for each endpoint in AWS that requires its own scope to be accessed.

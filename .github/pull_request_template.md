New User alerts should only be added by members of the ArduPilot Dev Team.

Because User Alerts are reserved for serious issues in ArduPilot that need to be communicated to all users, the following checklist has been developed
to ensure that User Alerts are accurate.

Checklist for adding a new User Alert or editing an existing User Alert:

1. Ensure it meets the definition of "User Alert". See https://ardupilot.org/dev/docs/user-alerts-developer.html for details
2. Create a new User Alert, using the ``template.json`` (in the root directory). The User Alert file must be placed in the ``alerts`` folder
   and use the pattern ``UA00001.json``, ``UA00002.json``, etc for the filename.
3. A 2nd member of the Dev Team must be tagged for review of the User Alert. This should be someone with enough technical understanding of the issue to confirm the
   details.
4. A 3rd member of the Dev Team must be tagged to confirm this process has been followed and that the fields in the User Alert json file are valid.
   The person will merge the PR.
   
A PR can be either the creation of a new User Alert or the addition of extra information (such as a new version of ArduPilot that fixes the issue).

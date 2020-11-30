
FAQ
***

Where do I get a token from?
----------------------------
You generate an API token by logging into EPIC and then look for the "API Token" section on the `Accounts -> Credentials <https://epic.zenotech.com/accounts/#credentials>`_ page.


What about uploading/downloading data?
--------------------------------------
At the time we don't support uploading and downloading data directly via the API. This is because it is more efficient to transfer your data directly to the data store without going via EPIC.
To do this any S3 compatable tool or SDK can be used, for example boto3. Search for data in the EPIC knowledge base to find details on how to do this.
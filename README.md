# Banking_System_API
 
### Api service for banking management operations writen on DRF  


### System and database configuration
```shell
git clone https://github.com/tkachuk2291/Banking_System_API.git
```

```shell
python3 -m venv venv  
``` 
```shell
source venv/bin/activate  
```
```shell
pip install -r requirements.txt  
```
### Setting up Environment Variables
```shell
touch .env  
```
### Example of environment variables
``` 
 .env.sample 
     ↓
     ↓
     ↓
 
```
**Example Env file ([Here you can generate a random key for Django Secret Key](https://djecrety.ir/))**

```
USERS_SECRET_KEY=your_secret_key_here
DEBUG=your choise format True|False
```

**Logging system** 
```
Attention! Execute the two commands below in the console or click the green button next to the commands,
 without this the logs and migrations will not work.
```
```shell
mkdir -p banking_operations/logs
mkdir -p user_account/logs
```

**Run migration to create database**
```shell
python manage.py migrate  
```
**Run Server**
```shell
python manage.py runserver 8001  
```
```
Documantation Postman
```
Please familiarize yourself with the[ documentation for Banking System](https://app.getpostman.com/run-collection/34236566-6de45ffd-5fe9-4284-a458-9edb348e5585?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D34236566-6de45ffd-5fe9-4284-a458-9edb348e5585%26entityType%3Dcollection%26workspaceId%3D787d7e3e-0ca8-4cef-a1ea-1177714682e1
) in Postman.
For convenience, all endpoints, test data, and practical hints are available there at a glance

**Please note that if you exceed the limit, the throttling system will limit you, to change it, specify your values in the settings** 
```
Current settings:
'anon': '15/day',
'user': '5/minute'
```

```
A logging system is implemented throughout the project.  
Note that you can find logs in two places, namely in the banking system application.
If the errors relate to banking operations and
 the user_account application If the errors relate to user or account creation
```

```
Quick start
```

```
1. Create a user account first from endpoints create_user_profile/
2. Go to endpoint token/ with body |login and password|
2.1 Copy access-token and go to the billing account endpoint, specify data in body (examples are in Postman in documentation).
3. Paste the |Bearer generated token| into the header and create a new billing account
4. use the |Bearer generated token| in all endpoints.
5. Familiarize yourself with the documentation in the Postman 
6. If you want see debug set it to True in env file
```






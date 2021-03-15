# User registration and Stripe Integration
User registration is managed by Django. Stripe is a payment infrastructure for the internet.
## Clone repo using command:
```bash
git clone <repo_url>
```
## Install Dependencies:
```bash
sudo apt install mysql-server
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```
## Create Virtual environment and install requirements using requirements.txt:
```
virtualenv -p python3 <environment_name>
source <environment_name>/bin/activate
pip install -r requirements.txt 
```
## Stripe account
1. Create account on stripe and then copy your publishable and secret key from Developers Api keys section.
2. Create .env file at the project root and set values for variables PUBLISHABLE_KEY, SECRET_KEY, DJSTRIPE_WEBHOOK_SECRET=whsec_xxx, DB_USER and DB_PASSWORD.
3. In profile_page.html, setup your own publishable key in Stripe function.
4. Create products on stripe account. 
## Djstripe
djstripe is used to get all the products that have been created by you
## Run the given command to get stripe product.
```
python manage.py djstripe_sync_plans_from_stripe
``` 
## Run migration commands and createsuperuser for setting up  database:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
## Run the Server using below command and then navigate to the [link](http://127.0.0.1:8000/)
```
python manage.py runserver
```
## Usage
After Navigating to the web, the homepage will get rendered, where you have to register first. Then, You will be logged in immediately to your profile page.  
At profile page you'll see the product that's been already selected for you.  
Next step is a payment, To test you can use card number 4242 4242 4242 4242 then you can choose any cvv and 5 digit pin code.  
Finally, you're done and then click on subscribe button. It will take few seconds and will navigate to completion page. Where it will tell you that your payment is successful and it will also shows the trial ends date.   
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
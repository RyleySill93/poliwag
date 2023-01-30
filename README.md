### Create a new Poliwag:
- Find and replace poliwag -> yourprojectname and Poliwag -> Yourprojectname
- Update favicon-32x32.png to your favicon
- Update logo.svg to your logo

### Setting up environment for first time
- install:
  - python (3.9.4)
  - nvm (16.3.2)
  - pyenv
  - virtualenv
  - postgres

#### Setup initially:  
create a virtual environment: `pyenv virtualenv 3.10.1 poliwag`. 
create a .python-version file in the root. input: `poliwag`

Grab sample .env file and copy into project root: `poliwag/.env`  

pip install -r requirements.txt
Troubleshooting:
- `LDFLAGS="-L$(brew --prefix openssl@1.1)/lib" CFLAGS="-I$(brew --prefix openssl@1.1)/include" pip install cryptography==3.2.1`

Create the database user and database  
`make setup-db`

(Optional) Seed the database with production data  
`make restore-db`

Start backend:  
`make dev-backend`

Install node modules:
`yarn install` or `npm install`

Start frontend:  
`make dev-frontend`

Grab ssh keys from dev@poliwag.com google drive

If in pycharm:
mark `backend` as sources root

Navigate to http://localhost:3000/login

### Helpful commands:
Check out the Makefile for a bunch of helpful commands. Some that are 
worth calling out -> 

Get into a django shell  
`make shell`

SSH into environment 
`make ssh`

### Tests
There is currently no CI/CD setup for this repository since it has just been
the two of us. 

The most complete tests are happy path full API on both of the main application flows:  
`make test-api`  
Would recommend checking these tests out to understand the API flows from a user perspective.


### Deployed environments:
Deployed environments are running:
Backend via gunicorn / unvicorn workers  
Nginx as a reverse proxy in front of backend server  
Frontend production built and served from CDN (cloudfront)  

To enter:
1) `make ssh`  
2) Select environment at prompt and continue through prompt
3) enter command: `poliwag` once on server
4) shell, environment, database access available in this directory `/var/www/poliwag/`


#### Production environment:
https://app.poliwag.com/

#### Sandbox environment:
https://app.sandbox.poliwag.com/

### Vendors:
- Slack
  - Application event alerting
- AWS
  - Infrastructure
- Sendgrid
  - Sending transactional email
Twilio
  - Sending SMS messages
- Sentry
  - Runtime error handling 
- Google
  - Address verification / typeahead
- Persona
  - KYC

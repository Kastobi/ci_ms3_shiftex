# MS3 – Shiftex: An Emergency Shift Exchange Platform

![opener](/readmeAssets/amIresponsive.jpg) **TODO: INSERT PICTURE**

[The website](http://ci-ms3-shiftex.herokuapp.com/) is a Full-Stack-Project which enables a collective 
of users to manage their shift exchanges on their given rotation plans. It was developed with a dataset
in mind, which includes ca 50.000 emergency shifts of 2.500 pharmacies organized in 95 rotation plans.

## Table of Contents
1. [UX](#UX)
   1. [Strategy & Scope](#Strategy-&-Scope)
   2. [Structure & Skeleton](#Structure-&-Skeleton)
   3. [Surface](#Surface) 
2. [Features](#Features)
   1. [Existing Features](#Existing-Features)
      1. [Meta](#Meta)
   2. [Features left to Implement](#Features-left-to-Implement)
3. [Technologies](#Technologies)
4. [Testing](#Testing)
   1. [Validators](#Validators)
   2. [Manual testing](#Manual-testing)
      - [Test cases](#Test-cases)
   3. [Automated testing](#Automated-testing)
5. [Deployment](#Deployment)
6. [Credits](#Credits)
 
---

## UX

### Strategy & Scope

A selection of the major objectives and selected ways to achieve them in form of user stories and conclusions.

As a…

#### Non participating User...
1. I want to see, which drugstore is on emergency duty right now.

#### User in need of a swap...

I'm not able to serve all shifts assigned to me. My rotation plan is rather big, and I need a fast and 
reliable method to communicate my request to swap to all other rotation plan members.

1. I want to request a swap on a given shift.
2. I want to revoke a request, if the circumstances changed.
3. I want this request to be communicated to all members in my rotation plan.
4. I want to handle offered shifts on my exchange request (reject / accept).
5. I want the exchange to be executed if both parties agree.

#### User bidding on a swap...

1. I want to see the requests on my rotation plan, and evaluate if I want to offer one of my shifts.
2. I want to offer shifts in exchange for a given swap request.
3. I want to see my offers on a given request and revoke them, if not processed already.
4. I want to see, which of my offers had been rejected, and maybe offer another one.
5. I want to confirm one of my accepted offers, so me as the person helping another one in need, can
select the best accepted offer.
6. I want the exchange to be executed after confirmation.

### Structure & Skeleton

- collections
   - shifts
   - swaps (shift id, biddings - shift ids, status)
   - users

#### Mobile wireframe

#### Desktop wireframe

### Surface


---

[Back to top](#Table-of-Contents)

## Features

### Existing Features

#### Meta

- Login, Logout and Register page allow users to log-in, -out and register.

- Control on the main user page allow users to filter on
    - just the users shifts
    - the available swaps on his rotation plan
    - both of them
    - just on upcoming shifts / swaps
    - all shifts in plan

- Colored, color- and text-changing buttons give users instant feedback on their actions.

- The page doesn't need reloads
    - Exceptions:
        - To include confirms, in this case reload is triggered by the confirmation
        - To include swap requests posted, while the user has been actively logged in.

- If not processed by another instance, every swap-action can be undone
    - Exceptions:
        - A swap request can be revoked, even if there are offers (a user can decide to not swap,
        after all). This cannot be undone
        - A confirmed swap (accepted & confirmed), cannot be undone. 
    
- A user can contact the developer on different ways.

- The Layout is responsive and usable on mobile and desktop devices.

### Features left to Implement
- Filters for duration of shifts, if different types of shift are on the plan.

- Filters for special rotations implemented in the rotation plan, e.g. based on population density in
regions around a drugstore

- A map for users searching a drugstore on duty right now

- Identification of the user requesting a swap
    - Neutral exchange vs concerns helping a competitor, maybe a voting feature per rotation plan?

- A User profile with the possibility
    - to change my contact information
    - to find contact information from my rotation plan
    - a dashboard with number and hours of emergency duty to maintain overview

- Admin functionality for managing the plan itself
    - manage rotation groups
    - mange user accounts (activate/deactivate)
    - add, delete and update bulks of data
        - from my planning software to the exchange platform
        - from the exchange platform to my planning software
    - a dashboard to maintain status overview

- Add logging to undo changes and spot possible problems

- Add more user messaging (e.g. "Your offer xyz was rejected")

---

[Back to top](#Table-of-Contents)
    
## Technologies

#### [HTML](https://en.wikipedia.org/wiki/HTML)
- for the main pages

#### [CSS](https://en.wikipedia.org/wiki/CSS)
- for everything styling related

##### [Bootstrap](https://getbootstrap.com/)
- for the responsive layout and modal

##### [FontAwesome](https://fontawesome.com/)
- for link symbols

##### [Google Font *Lato*](https://fonts.google.com/specimen/Lato)
- for Lato for a clean readable impression

#### [Python](https://www.python.org/)
- for BackEnd logic

##### [Flask](https://flask.palletsprojects.com/en/latest)
- as Backend Microframework

##### [Flask PyMongo](https://flask-pymongo.readthedocs.io/en/latest/)
- for database connection

##### [Flask RESTful](https://flask-restful.readthedocs.io/en/latest/index.html)
- as extension for the restlike api

##### [Flask Login](https://flask-login.readthedocs.io/en/latest/)
- as extension for user login

##### [Flask WTF](https://flask-wtf.readthedocs.io/en/latest/)
- as extension for register and login forms

#### [MongoDB](https://www.mongodb.com/)
- as database

##### [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- as cloud database provide for the deployed version

##### [MongoDB Compass](https://www.mongodb.com/products/compass)
- for database management

#### [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- for FrontEnd logic

##### [jQuery](https://jquery.com/)
- for API communication and User feedback on interaction

#### [Git](https://git-scm.com/) / [GitHub](https://github.com)
- for version control
- as source for deployment

#### [gitpod](https://gitpod.io)
- as IDE

#### [Pycharm](https://www.jetbrains.com/pycharm/)
- as IDE, after gitpod was unavailable to frequently

#### [code institute gitpod template](https://github.com/Code-Institute-Org/gitpod-full-template)
- as a starter for the gitpod environment

#### [code institute readme template](https://github.com/Code-Institute-Solutions/readme-template)
- as a starter for the readme.md

#### [Heroku](https://www.heroku.com/)
- as cloud platform to deploy the platform

---

[Back to top](#Table-of-Contents)

## Testing

### Validators

#### HTML Validator

#### CSS Validator

#### JS Validator

#### Lighthouse

##### Performance

##### Accessibility

##### Best Practices

### Manual testing

#### Chrome exclusive, deployed page

##### Test cases

### Automated testing

### User-Story verification

#### User
 
### Slack review


### Readme

---

[Back to top](#Table-of-Contents)

## Deployment


### Local

- You got a [Python environment](https://www.python.org/downloads/), do you?
    - Installation not covered here, but [here](https://wiki.python.org/moin/BeginnersGuide/Download)
- You got a running [MongoDB](https://www.mongodb.com/try/download/community), do you?
    - Installation not covered here, but [here](https://docs.mongodb.com/guides/server/install/)
- On the [GitHub page](https://github.com/apometricsTK/ci_ms3_shiftex)  click on **Code** (top right)
- Click "Download ZIP"
- Extract to your desired location
- Create "env.py" file in the directory, open it and provide following parameters
    - TZ database name: [Look it up](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
    - Mongo_Uri first line is for local, enter your database name
        if deployed, remove the hash and place it as first in line above

```
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("TZ", " your timezone ")
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/myFirstDatabase")
# os.environ.setdefault("MONGO_URI", " Lookup how to obtain this link for cloud mongoDB in Heroku section ")
os.environ.setdefault("SECRET_KEY", " Your secret key belongs here ")
```

- Save file
- Optional:
    - Create [virtual environment](https://docs.python.org/3/tutorial/venv.html)
    - Activate virtual environment
- Install required packages with

```
pip install -r requirements.txt
```

- Run app with 
```
python run.py
```  


### Deployed / Hosted

The way of deployment varies widely, dependent on the way your hoster / cloud provider works.
I will explain the way to deploy via Heroku and mongoDB Atlas, you can adapt with the support 
of your service provider from this schema.

#### with Heroku and mongoDB Atlas

- [Login](https://account.mongodb.com/account/login) to your mongoDB Atlas Account
    - No Account? [SignUp!](https://account.mongodb.com/account/register)
- Create a Project (Projects -> New Project)
    - Name it and select an owner
    - Click **Create it**
- **Build a Cluster**
    - Select a path (this one uses the free shared Cluster)
    - Choose Cloud provider and region fitting the planned user region
    - Click **Create Cluster**
    - Wait for the cluster to be completed (this takes some minutes)
- Click on **Collections**, **Add my own data**
    - Create a Database name (e.g. "shiftex" without quotation marks)
    - Add Collection "shifts", **Create**
    - Click on the **+** to the right of your database name when hovering it
    - Add Collection "users" and repeat with "swaps"
- On the left side select **Database Access**, **Add new database user**
    - password, username, enter password, **Add User**
- On the left side select **Network Access**, **Add IP Address**
    - **Allow Access from Anywhere**, **Confirm**
- On the left side select **Clusters**, **Connect**
    - **Connect your application**
    - Copy the link, hold it close with password and database name - you need them later
- On the left side select **Clusters**, **Connect**
    - **Connect using mongoDB Compass**, choose your version, copy link,
        - **modify password**, see above
- Use [mongoDB Compass](https://www.mongodb.com/try/download/compass) to upload bulk data
    - Once installed, click **New Connection**
    - enter Link, **Connect**
    - select your database
    - select **shifts** collection
    - **Add Data**, Import File, select file, file type (e.g. JSON), **Import**

- [Login](https://id.heroku.com/login) to your Heroku Account
    - No Account? [Sign Up!](https://signup.heroku.com/)
    - select Python for primary language
    - Activate via the confirmation mail
    - Accept terms
- Click on **Create a new app** (top right)
    - Enter a name (it has to be unique, but is not necessary open to anyone)
    - Select a region (preferably where the app will be used)
    - Click **Create App**
- Select the **Deploy** tab
    - Select **GitHub** (Deployment method)
    - Enter GitHub credentials
    - Select the required repository
    - Click **Connect**
    - Optional: 
        - To activate automatic redeploy on GitHub
            - in Heroku Account, select App, Deploy -> Automatic deploys
            - Select the branch  ("main" / "master" most of the time)
            - Click **Enable Automatic Deploys**
- Select the **Settings** tab
    - Click **Reveal Config Vars**
    - Set the following key - value pairs (left field, right field)
        - IP - 0.0.0.0
        - SECRET_KEY - enter a **SECRET** key here, to protect your app
            - a way to obtain one is [RandomKeygen](https://randomkeygen.com/)
        - MONGO_URI - enter the URI given to you by MongoDB Atlas, pay attention: there are
    **user credentials** included, so be secretive
            - You got the link for mongoDB Atlas? Modify with your password and database name
            - You have to replace "\<password\>" with your password
            - You have to replace "myFirstDatabase" with your database name
- Optional:
    - Configure custom domain (hide that ugly name you had to pick, because all good names are taken)
      and SSL (both not covered here)
- **Domains** let you know where your app is ready for you.

- Visit Domain with your favorite browser

---

[Back to top](#Table-of-Contents)

## Credits

### Content

#### Data

- From a public emergency-shift finder

#### Components

- Browser compatibility verification with [caniuse](https://caniuse.com/)

### Media

* The Font Awesome symbols were made by [Font Awesome](https://fontawesome.com/)

* The first readme screenshot was taken with [ami.responsive](http://ami.responsivedesign.is/)

* The favicon was generated with [favicon.io](https://favicon.io/)

### Acknowledgments

* My mentor Brian Macharia for his support and feedback.

* [Benjamin Kavanagh](https://github.com/BAK2K3) for his support and feedback

* Miguel Grinberg for his incredible [blog](https://blog.miguelgrinberg.com/) and 
  [book](https://www.oreilly.com/library/view/flask-web-development/9781491991725/)
  
* Corey Schafer for his [YouTube Flask tutorial](https://youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)

* Code institute tutor Joke Heyndels for restarting my mind, when I lost myself in details
finding a deployment bug.

* My [team from Code Institute hackathon March 2021](https://hackathon.codeinstitute.net/teams/39/) for feedback and
support.

* The Code Institute slack community for their support.

* The open source community for everything.

### Disclaimer

The project is for educational purposes only.

[Back to top](#Table-of-Contents)

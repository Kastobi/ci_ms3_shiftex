# MS3 – Shiftex: An Emergency Shift Exchange Platform

![opener](/readmeAssets/am_i_responsive.jpg)

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

The value for the user is the quick communication with his rotation group and overview
on shifts and swap requests. The best way to achieve overview over this data is limiting
it (filter irrelevant data = shifts not assigned to user and without a request for swap 
from his rotation group). The shifts date as main information and identifier for the user
is in center of the view.

A filter to just show user shifts or show swap requests as well will support focusing
on the desired intent.

The user journey in a standard process should be
    
1. **User A** posts a swap request
2. **User B** offers shifts of his own to swap
3. **User A** accepts/rejects some of this offers
4. **User B** confirms **one** of the accepted offers
    - here the confirmed swap will be executed

The **given** data is a list of objects, following the schema:

![shift schema](/readmeAssets/shifts.jpg) 

They were bulk-imported into mongoDB, and the set from mongoDB generated "_id" was
used as primary key and main identifier afterwards.

![shift imported schema](/readmeAssets/shifts_import.jpg)

Based on this following user and swap schema has been developed.

![user schema](/readmeAssets/users.jpg) 
![user schema](/readmeAssets/swaps.jpg) 

The document types are stored in three different collections.
    - shifts in shifts
    - swaps in swaps
    - users in users

The relevant connections:
    - users
        - drugstoreId connects to
            - shifts documents
            - swaps documents
    - swaps
        - is based on the **_id** from the shift offered
        - digitsId connects to relevant shifts from the rotation
        - drugstoreId connects to user document and other shifts from user
        - the shiftIds in the arrays connect to offered shifts and their status

#### Desktop wireframe

![Desktop wireframe 1](/readmeAssets/desktop1.png) 
![Desktop wireframe 1](/readmeAssets/desktop2.png) 
![Desktop wireframe 1](/readmeAssets/desktop3.png) 
![Desktop wireframe 1](/readmeAssets/desktop4.png) 
![Desktop wireframe 1](/readmeAssets/desktop5.png) 

#### Mobile wireframe

![Mobile wireframe 1](/readmeAssets/mobile1.png) 

### Surface

As the main purpose is data handling, managing and overview, I deliberately decided against too many graphic 
distractions. 

Signal colors (green to accept something, red to revoke ore reject something) help users to
orientate. Hovering effects and well known control elements support intuitive navigation
and interaction.

---

[Back to top](#Table-of-Contents)

## Features

### Existing Features

#### Drugstores on duty today

A not logged-in user can see drugstores on emergency duty today.

#### Users Dashboard

A user can see his shifts and swap requests from his rotation plan.

##### Handle offers

A user can accept and reject offers on his swap request.

##### Offer shifts

A user can offer one of his shifts on a swap request.

##### Confirm accepted offers

A user can confirm an accepted offer.

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

- Database CRUD functionalities given
    - **Create** Shift, User and Swap documents
    - **Read** Shift, User and Swap documents
    - **Update** Swap documents
    - **Delete** Shift and Swap documents
    
- REST-like endpoints need a login (therefore REST-"like") and only logged-in users are able to use them.

#### 

### Features left to Implement

- Additional security question on revoking request and confirming swap (non-revocable database change)

- Additional security checks on REST-like endpoints
    - e.g. 
        - check if drugstore-id and users-drugstore match
        - expiration timers

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

- Refactoring JavaScript, proper REST-call error reporting

- Add a "help" page, to explain process to users direct on page

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

### Bugs while developing

#### Deploy problem

The app factory pattern with [flask configuration via object](https://flask.palletsprojects.com/en/2.0.x/config/) made
long problems. The IP and PORT must **NOT** be passed in via config object, but must be passed to app.run().

A mongo SSL problem was observed while searching this bug. Therefore SSL stack was added (certifi, dnspython, pyOpenSSL)

[Nearly Full Story (restricted access)](https://code-institute-room.slack.com/archives/CHDVDV2Q4/p1623311812056800).

### Validators

Validators were used by "copy and pasting" the code into validators. HTML was taken from the browser source code, to
validate template schema.
- Strg+A
- Strg+C
- Strg+V

#### HTML Validator

- On script root for the templates the "defer" was removed.
- As the apps views consists of "single purpose use" with only one section and has no SEO intentions, the headers right 
  above the content section were ruled to be sufficient. No further heading was added to the "section" in contrast to 
  HTML validator warning.
- "action" attribute for login and register forms were added.

The validator used is the [HTML validator](https://validator.w3.org/) and the warning mentioned is the only issue.

#### CSS Validator

The styles.css was validated by [jigsaw validator](https://jigsaw.w3.org/css-validator/) and passed without issues.

#### JS Validator

The script.js was validated by [JSHint](https://jshint.com/).

The validator clearly shows much refactor potential. This was evident to the developer but the focus (backend and data)
and the deadline did not allow refactoring the code.

#### Python Validator

#### Lighthouse

After first preloading of the page (to start Heroku dyno and mongoDB) Lighthouse evaluation results:

![Lighthouse](/readmeAssets/lighthouse.jpg)

### Manual testing

The Browsers Chrome(v91.0.4472.101) and Firefox (v89.0) were used for testing.
The deployed version of the page was tested.

All links and buttons were clicked and observed on function.

#### Chrome exclusive, deployed page

##### Test cases

As logged in user (observe database)
- to consider for these tests
  - when upcoming only is checked, just shifts and swap requests starting 24h ago are listed (observe database, 
    identifier from and drugstoreId / digitsId)
- your shifts are listed, when "my shifts" is activated (observe shifts collection, identifier: drugstoreId)
- the rotation plans swaps requests are listed, when "Rotation plan requests" is activated (observe shifts collection, 
  identifier: digitsId)
- when "both" is activated, both are listed - different background, different buttons

As logged in user (compare database)
- for your posted swaps, there is a "Handle offers" and "Revoke request" Button, else "Request swap" (compare swap
  documents shiftId)
- when click "Request Swap"
    - swap document is generated and added to swaps collection (observe swaps collection)
    - the button is replaced by two buttons ("Handle offers" and "Request swap")
- when click "Handle Offers"
    - a modal opens
    - all offered shifts are listed and have "Accept" or "Reject" Buttons (observe swap document)
    - on click on accept/reject and afterwards on the other one
        - the shifts are moved to accept / reject array (observe swap document)
        - the button change from outline to block, disabled and get "-ed" appended to text
- when click "Revoke request"
    - the swap document gets deleted (observe swap document)
    - the buttons disappear and are replaced by "Request swap" button
    
- for "rotation plan swap requests"
    - the swap documents with your digitsId are listed, with offer swap button (compare Database)
        - when clicked, a modal opens:
            - showing your shifts and an "offer shift" button for not offered lists, a "rejected" sign for rejected
              offers and a "revoke offer" button for not handled offers (compare swap document)
            - on click "offer shift" the shift is added to "offer" array (observe swap document)
            - on click "revoke shift" the shift is removed from "offer" array (observe swap document)
    - if there are swap documents with accepted offers from you (identifier same shiftIds with your drugstoreId in swap
    document with your digitsId)
        - there is a "confirm" button, instead of an "offer swap" button
        - on "confirm" click
            - a modal opens, showing the shifts from the accept array of the swap document which got your drugstoreId, 
              with a "confirm swap" button beneath
            - the shifts are paired with the requested swap shift, for easy compare
    
As not logged in user
- You can register with credentials:
    - all fields necessary (First Name, Last Name, Email, Drugstore, Password, Confirm Password, Terms)
    - email has to be a valid email schema
    - password has to have minimum six characters, at least one letter, one number and one special character
        - an error is already highlighted before clicking "sign up"
    - the others are tested on "sign up" clock
    - there is a redirect to login

- You can login with valid credentials
    - there is a redirect to user

### User-Story verification

#### Non participating User...

1. I want to see, which drugstore is on emergency duty right now.

![today on duty screenshot](/readmeAssets/today_on_duty.jpg)

#### User in need of a swap...

1. I want to request a swap on a given shift.
   
![request_swap](/readmeAssets/request_swap.jpg)

2. I want to revoke a request, if the circumstances changed.

![revoke_request](/readmeAssets/revoke_request.jpg)   

3. I want this request to be communicated to all members in my rotation plan.
   
![rotation_requests](/readmeAssets/rotation_requests.jpg)   

4. I want to handle offered shifts on my exchange request (reject / accept).
   
![accept_reject](/readmeAssets/accept_reject.jpg)   

5. I want the exchange to be executed if both parties agree.
    - observed and checked with two users

#### User bidding on a swap...

1. I want to see the requests on my rotation plan, and evaluate if I want to offer one of my shifts.

![rotation_requests](/readmeAssets/rotation_requests.jpg)   
   
2. I want to offer shifts in exchange for a given swap request.
3. I want to see my offers on a given request and revoke them, if not processed already.
4. I want to see, which of my offers had been rejected, and maybe offer another one.
   
![offer_status](/readmeAssets/offer_status.jpg)   

5. I want to confirm one of my accepted offers, so me as the person helping another one in need, can
select the best accepted offer.
   
![confirm1](/readmeAssets/confirm1.jpg)   
![confirm2](/readmeAssets/confirm2.jpg)   

6. I want the exchange to be executed after confirmation.
    - observed and checked with two users
 
### Slack review

The project has been posted to the Code Institute community Slack channel peer-code-review and to the Hackathon 
group-chat for different pairs of eyes.

### Readme

Readme was observed on GitHub. All links were clicked.

---

[Back to top](#Table-of-Contents)

## Deployment

Deployment on local and via Heroku with MongoDB Atlas covered.

### Local

- You got a [Python environment](https://www.python.org/downloads/), do you?
    - Installation not covered here, but [here](https://wiki.python.org/moin/BeginnersGuide/Download)
- You got a running [MongoDB](https://www.mongodb.com/try/download/community), do you?
    - Installation not covered here, but [here](https://docs.mongodb.com/guides/server/install/)
- On the [GitHub page](https://github.com/apometricsTK/ci_ms3_shiftex)  click on **Code** (top right)
- Click "Download ZIP"
- Extract to your desired location
    - You need (other files can)
        - shiftex folder with content
        - requirements.txt (for "virtual environment" step below)
        - run.py
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

- Visit your configured address (default: "http://127.0.0.1:5000") with your favorite browser

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

* The wireframes were drawn with [Balsamiq](https://balsamiq.com/)

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

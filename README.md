# Team 56

# Project Assigned: Tinder for roommates

1. Name of our web-application: **MatchBox**

2. A brief summary of the features we have implemented are as follows:

    a) Design:
    
        i) Typewriter text using JS
        
        ii) Transitions of images on homepage using JS
        
        iii) Implementing Next and Previous buttons to transition to next rowdata of the database.
        
        iv) Created a logo for our website.
        
    b) Other aspects:
    
        i) Created an algorithm to display the matched percentage of two particular entries.
        
        ii) We have also included a login and sign-up page so that if the user is not registered, he/she is redirected to the form else the matching roommate results are displayed directly.
        
    c) Our website displays all the possible roomates of the same gender that a person can have such that with whom he/she has the highest matched percentage is displayed first.
    
    d) A local database is already present in our codebase to which the entries will be appended.

3. Frameworks and packages used:

    a) Google fonts: 
    
         https://fonts.googleapis.com/css2?family=Audiowide&family=Chakra+Petch&family=Poly&family=Rajdhani&family=Sigmar&display=swap
        
    b) Flask:
    ```
        from flask import Flask, render_template, request, redirect, url_for
        import sqlite3
    ```
    
4. Instructions to set up:-
    The application can be accessed by running the flask application app.py. The server link obtained will redirect to the homepage of the website from where other pages can be accessed according to the buttons and links present.
  Running this web application on someone else's computer assumes the following conditions:
    i) The screen resolution assumed is 1920x1080.
    ii) The operating system used is Ubuntu.
    iii) Flask is installed.

5. Contribution of each member to the project:
    ```
    Sumit: 1) Login, Signup, About pages
           2) Flask functionalities in app.py
    Ketaki: 1) Questionnaire page for registration.
            2) Flask functionalities in app.py
    Prabhav: 1) Home and Results pages
             2) Complete designing and integrating it on all pages.
    ```

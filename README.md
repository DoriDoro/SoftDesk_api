# SoftDesk
## Description:
Project 10 OpenClassrooms Path  -  SoftDesk  -- create a secure RESTful API using Django REST

For the SoftDesk project we created an RESTful API from scratch. The User model got additional 
attributes, for GDPR regulations. The user should have the possibility to view, edit and delete 
the information. 

A user can create different types of projects, add other users as contributor(s) and add issues 
to these projects. The issue has different tags, states and priorities. An issue can be assigned 
to a contributor or to the author itself. Out of the issue a user/contributor can create comments.

To guarantee just the author (creating user, no contributor) of a project is able to edit or 
delete a project, issue and comment, we implemented permissions. For the “Green Code” implementation, 
I have created several serializers for different purposes, added pagination and reduced database 
queries with the creation of view properties. 


## Installation:
open terminal:
1. `git clone https://github.com/DoriDoro/SoftDesk_api.git`
2. `cd SoftDesk_api`
3. `pipenv install` this command installs all necessary requirements and installs the virtual environment
4. `pipenv shell` activates the virtual environment
5. `python manage.py runserver` this command starts the server

 ### after the installation and starting the server you can:
1. use: http://127.0.0.1:8000/api/ in browser to check the API 
2. BETTER OPTION: go to [Postman](https://www.postman.com/) and make some tests

 ### useful ULRs:
http://127.0.0.1:8000/api/login/ <br>
username: ThePing <br>
password: HelloThere55

http://127.0.0.1:8000/api/projects/

http://127.0.0.1:8000/api/projects/1/contributors/

http://127.0.0.1:8000/api/projects/1/issues/

http://127.0.0.1:8000/api/projects/1/issues/1/comments/

http://127.0.0.1:8000/api/users/


## Skills:
- Securing an API to comply with OWASP and RGPD standards
- Creating a RESTful API with Django REST


## Visualisation:
all images are Postman visualisations.

**1. GET all projects of the logged-in user:**
![projects](/README_images/GET_projects.png)
<br>

**2. GET detailed version of one project of logged-in user:**
![single_project](/README_images/GET_single_project.png)
<br>

**3. GET all issues of the logged-in user:**
![issues](/README_images/GET_issues.png)
<br>

**4. GET detailed issue of one issue:**
![single_issue](/README_images/GET_single_issue.png)
<br>

**5. GET all comments of logged-in user:**
![comments](/README_images/GET_comments.png)
<br>

**6. GET single comment of logged-in user:**
![single_comment](/README_images/GET_single_comment.png)
<br>

**7. GET all contributors of the project:**
![contributors](/README_images/GET_contributors.png)
<br>

## Articles:
- [How to first migrate custom User model within models directory](https://dev.to/doridoro/how-to-first-migrate-custom-user-model-within-models-directory-1bdl)
- [DRF create @property in view](https://dev.to/doridoro/drf-create-property-decorator-in-view-and-use-property-in-serializer-okm)
- [DRF create validation in serializer](https://dev.to/doridoro/drf-create-validation-in-serializer-421i)
- [Error: \_\_str\_\_ returned non-string (type User)](https://dev.to/doridoro/error-str-returned-non-string-type-user-344n)
- [Problem with serializer](https://dev.to/doridoro/what-problems-can-happen-with-different-serializer-in-drf-5e7m)
- [several ways to create a simple url](https://dev.to/doridoro/several-ways-to-create-a-simple-url-2fhh)
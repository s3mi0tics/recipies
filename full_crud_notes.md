1. open project folder in terminal then type code .

2. start server in terminal to see if it is runs
```
pipenv install flask pymysql flask-bcrypt
pipenv shell
python3 server.py
```

3. create folder structure
    *server.py
    * flask_app
        *config
            *mysqlconnection.py
        *controllers
            *controller_table.py
        *models
            model_table.py
        *templates
            *template.html
        *static
            *style.css
            *img
            *script.js
        *__init__.py
        *pipfile
        pipfile.lock
4. paste to server.py
```
from flask_app import app
from flask_app.controllers import controller_user


if __name__=="__main__":
    app.run(debug=True)
    
```
5. paste to mysqlconnection.py
```
# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'rootroot', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
```
6. controllers files
```
from flask_app import app
from flask import render_template, redirect, session, request

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route(/success)
def success():
    return 'success'

```
7. models files
```
# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database

DATABASE = ''# TODO: fill in data base

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
# use @classmethod to query the database

```
8. template.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Template</title>

<!--   Bootstrap CSS   -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">


</head>
<body>
    <h1>HTML TEMPLATE</h1>

<!--   bootstrap js   -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

</body>
</html>
```
9. __init__.py
```
from flask import Flask

from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = 'rootroot'

bcrypt = Bcrypt(app)
```


# RESTful archeteture
    # two types of routes
    # display routes
    # action routs
        # /tablename/<id>(if possible)/action
        # /user/new -> (display) show form to create a new user
        # /user/create -> (action) create user
        # /user/<id> -> (display) show form
        # /user/<id>/update -> (action) process info that comes from show form
        # /user/<id>/delete -> (action) delete a record
        
# functions
    # create ->
    # get_all ->
    # get_one ->
    # update_one -> returns nothing
    # delete_one ->returns nothing
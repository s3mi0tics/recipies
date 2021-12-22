from flask_app.controllers import controller_user, controller_routes
from flask import flash
import re 


# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = 'recipies_db'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    #C
    @classmethod
    def create(cls, data:dict) ->int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    #R
    @classmethod
    def get_one(cls, data:dict) ->list:
        query = "SELECT * from users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_one_by_email(cls, data:dict) ->list:
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_all(cls) ->list:
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return all_users
        return False


    #U
    @classmethod
    def update_one(cls, data:dict) ->None:
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)



    #D
    @classmethod
    def delete_one(cls, data:dict) ->None:
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #Validate
    @staticmethod
    def validate_registration(data:dict) ->bool:
        is_valid = True

        if len(data['first_name']) < 1:
            flash("First name is required", "err_user_first_name")
            is_valid = False
        
        if len(data['last_name']) < 1:
            flash("Last Name is required", "err_user_last_name")  
            is_valid = False

        if len(data['email']) < 1:
            flash("Email is required", "err_user_email")  
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "err_user_email")
            is_valid = False

        if len(data['password']) < 1:
            flash("Password is required", "err_user_password")  
            is_valid = False

        if len(data['confirm_password']) < 1:
            flash("Confirm Password is required", "err_user_confirm_password")  
            is_valid = False

        elif data['password'] != data['confirm_password']:
            flash("Passwords do not match", "err_user_confirm_password")
            is_valid = False

        all_users = User.get_all()

        for user1 in  all_users: 
            if user1.email == data['email']:
                flash("email in use", "err_user_email")
                is_valid = False
        
        return is_valid


    @staticmethod
    def validate_login(data:dict) ->bool:
        is_valid = True

        if len(data['email']) < 1:
            flash("Email is required", "err_user_email1")  
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "err_user_email1")
            is_valid = False

        if len(data['password']) < 1:
            flash("Password is required", "err_user_password1")  
            is_valid = False
        
        return is_valid

        
        
        
        
        
        
            
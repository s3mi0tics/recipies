# import the function that will return an instance of a connection
from types import MethodDescriptorType
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user

DATABASE = 'recipies_db'
from flask import flash

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.name = data['name']
        self.description = data['description']
        self.under_30_min = data['under_30_min']
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.user_id = data['user_id']


    def creator(self):
        return model_user.User.get_one({'id': self.user_id})

    #C
    @classmethod
    def create(cls, data:dict) ->int:
        query = "INSERT INTO recipies (name, description, under_30_min, instructions, date_made_on, user_id) VALUES (%(name)s, %(description)s, %(under_30_min)s, %(instructions)s, %(date_made_on)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)


    #R
    @classmethod
    def get_one(cls, data:dict) ->list:
        query = "SELECT * from recipies WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls) ->list:
        query = "SELECT * FROM recipies;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_recipies = []
            for recipie in results:
                all_recipies.append(cls(recipie))
            return all_recipies
        return False

    @classmethod
    def get_all_of_user(cls, data) ->list:
        query = "SELECT * FROM recipies WHERE user_id = %(user_id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            all_recipies = []
            for recipie in results:
                all_recipies.append(cls(recipie))
            return all_recipies
        return False
    
    @classmethod
    def get_user(cls, data:dict)-> list:
        query="SELECT * FROM recipies JOIN users ON users.id = recipies.user_id where recipies.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            print(results)
            recipe = cls(results[0])
            data ={
                "id":results[0]["users.id"],
                "created_at":results[0]["users.created_at"],
                "updated_at":results[0]["users.updated_at"],
                "first_name":results[0]["first_name"],
                "last_name":results[0]["last_name"],
                "email":results[0]["email"],
                "password":results[0]["password"],
            }
            user = model_user.User(data)
            recipe.user = user
            return recipe

    #U
    @classmethod
    def update_one(cls, data:dict) ->None:
        query = "UPDATE recipies SET name = %(name)s, description = %(description)s, under_30_min = %(under_30_min)s, instructions = %(instructions)s, date_made_on = %(date_made_on)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #D
    @classmethod
    def delete_one(cls, data:dict) ->None:
        query = "DELETE FROM recipies WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #Validate
    @staticmethod
    def validate_recipe(data:dict) ->bool:
        is_valid = True

        if len(data['name']) < 1:
            flash("First name is required", "err_recipe_name")
            is_valid = False
        
        if len(data['description']) < 1:
            flash("Last Name is required", "err_recipe_description")  
            is_valid = False

        if len(data['instructions']) < 1:
            flash("Email is required", "err_recipe_instructions")  
            is_valid = False

        if not 'under_30_min' in data:
            flash("select one", "err_recipe_under_30_min")  
            is_valid = False

        if not data['date_made_on']:
            flash("enter a date", "err_recipe_date_made_on")  
            is_valid = False

        return is_valid
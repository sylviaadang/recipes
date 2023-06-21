from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users_model


class Recipe:
    DB = 'recipes_schema'

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.minutes = data['minutes']
        self.created_at = data['created_at']
        self.udpated_at = data['updated_at']
        self.user_id = data['user_id']


    @staticmethod
    def validate_recipe(new_recipe):
        is_valid = True
        if len(new_recipe['name']) < 4:
            flash('Name must be at least 3 characters')
            is_valid = False
        if len(new_recipe['description']) < 4:
            flash('Description must be at least 3 characters')
            is_valid = False
        if len(new_recipe['instructions']) < 4:
            flash('Instructions must be at least 3 characters')
            is_valid = False
        if len(new_recipe['date']) < 1:
            flash('Date field is required')
            is_valid = False
        if 'minutes' not in new_recipe:
            flash('Minutes is required')
            is_valid = False

        return is_valid

    @classmethod
    def create_recipe(cls, data):
        query = """
        INSERT INTO recipes (name, description, instructions, date, minutes, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(minutes)s, %(user_id)s);
        """
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT * FROM recipes
        JOIN users ON users.id = recipes.user_id;
        """

        result = connectToMySQL(cls.DB).query_db(query)

        all_recipes = []

        for row in result:

            user_data = {
                'id' : row['user_id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }

            one_recipe = cls(row)
            one_recipe.recipe_poster = users_model.User(user_data)
            all_recipes.append(one_recipe)

        return all_recipes

    @classmethod
    def get_one_recipe(cls,data):
        query = """
        SELECT * FROM recipes
        JOIN users ON users.id = recipes.user_id
        WHERE recipes.id = %(recipe_id)s;
        """

        result = connectToMySQL(cls.DB).query_db(query, data)

        one_recipe = cls(result[0])

        user_data = {
                'id' : result[0]['user_id'],
                'first_name' : result[0]['first_name'],
                'last_name' : result[0]['last_name'],
                'email' : result[0]['email'],
                'password' : result[0]['password'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at']
            }

        one_recipe.recipe_poster = users_model.User(user_data)


        return one_recipe

    @classmethod
    def update_recipe(cls,data):
        query = """
        UPDATE recipes
        SET name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s,
        date = %(date)s,
        minutes = %(minutes)s
        WHERE id = %(recipe_id)s;
        """

        return connectToMySQL(cls.DB).query_db(query, data)


    @classmethod
    def delete_recipe(cls,data):
        query = """
        DELETE FROM recipes
        WHERE id = %(recipe_id)s;
        """

        return connectToMySQL(cls.DB).query_db(query, data)

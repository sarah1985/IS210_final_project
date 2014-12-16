#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Final Project...here we go!"""

import os
import os.path
import pickle


class RecipeManagement(object):
    """This class will create a file to house recipes.
    It will also allow a user to add new recipes via a dictionary
    key, value pair.
    Users can recall recipes using the same dictionary.
    The flush will save any changes the user makes to the disk"""

    __file_object = None
    __data = {}

    def __init__(self, file_path='my_cookbook.pkl'):
        """Constructor. This will create the cookbook pickle file
        to which the user can add, modify or recall recipes."""

        self.__file_path = file_path

    def set(self, key, value):
        """public set method"""

        self.__data[key] = value

    def get(self, key):
        """public get method"""

        try:
            if key in self.__data:
                return self.__data[key]
        except KeyError:
            print "Error: No value found for key: '{}'".format(key)

    def delete(self, key):
        """public delete method"""

        if key in self.__data:
            del self.__data[key]
        else:
            raise "Error: No value found for key: '{}'".format(key)

    def open(self):
        """public open method"""

        if os.path.exists(self.__file_path):
            if os.path.getsize(self.__file_path) > 0:
                self.__file_object = open(self.__file_path, 'rb')
                self.__data = pickle.load(self.__file_object)
                self.__file_object.close()
        self.__file_object = open(self.__file_path, 'wb')

    def flush(self, reopen=True):
        """pickle dump"""

        try:

            self.__file_object = open(self.__file_path, 'wb')

        except IOError:
            print 'The cookbook is not open! Please open before continuing.'

        pickle.dump(self.__data, self.__file_object)
        self.__file_object.close()

        if reopen:
            self.open()

    def close(self):
        """close method"""

        self.flush(reopen=False)

    def read_recipes(self):
        """read saved recipes"""

        self.open()
        recall_list = self.get('key')
        self.close()

        return recall_list

    def save_recipes(self, existing):
        """save recipes"""

        self.open()
        self.set('key', existing)
        self.flush()
        self.close()


class RecipeCollection(object):
    """manages the user input recipes"""

    def __init__(self):
        """constructor"""

        self.recipe_list = []

    def recipe_actions(self):
        """combines ingredient collection and direction collection to create
            new recipe and add to file"""

        user_action = raw_input(
            'Enter a recipe action (add, search, quit): ').lower().strip()

        if len(user_action) > 0 and user_action[0] == 'a':
            add_rec = True
            while add_rec:
                new_rec = Recipe()
                new_rec.create_new_recipe()
                self.recipe_list.append(new_rec)

                cont = raw_input(
                    'Do you want to enter another recipe? ').strip().lower()

                if len(cont) > 0 and cont[0] != 'y':
                    add_rec = False

        elif len(user_action) > 0 and user_action[0] == 's':

            keyword = raw_input(
                'Enter the keyword you\'d like to search: ').lower().strip()

            search_results = self.search_recipes(keyword)

            if len(search_results) == 0:
                print 'No results found! Please try another search.'

            else:
                for item in search_results:
                    print item.input_to_string()

        elif len(user_action) > 0 and user_action[0] == 'q':

            quit_conf = raw_input(
                'Are you sure you want to save and quit? ').lower().strip()

            if len(quit_conf) > 0 and quit_conf[0] == 'y':
                save_quit = RecipeManagement()
                save_quit.save_recipes(self)
                return False

        return True

    def input_to_string(self):
        """return entered values to user"""

        rec_list = ''
        for item in self.recipe_list:
            rec_list = rec_list + item.input_to_string() + '\n\n'

        return rec_list

    def search_recipes(self, keyword):
        """search recipes by keyword"""

        search_results = []

        for item in self.recipe_list:
            if item.search_recipe(keyword):
                search_results.append(item)

        return search_results


class Recipe(object):
    """defines the recipe and its components"""

    def __init__(self):
        """constructor"""

        self.title = ''
        self.ingredients = IngredientCollection()
        self.directions = DirectionCollection()

    def create_new_recipe(self):
        """creates new recipe at the request of the user"""

        self.title = raw_input(
            'What is the recipe name? ').lower().strip()

        self.ingredients.get_ingredient_list()

        self.directions.get_direction_list()

    def input_to_string(self):
        """input to string"""

        recipe = '--{0}-- \n\n {1} \n\n {2}'.format(
            self.title, self.ingredients.input_to_string(),
            self.directions.input_to_string())

        return recipe

    def search_recipe(self, keyword):
        """search recipe for keyword"""

        if keyword in self.title:
            return True

        if self.ingredients.search_ingredient_collection(keyword):
            return True

        if self.directions.search_dir_collection(keyword):
            return True

        return False


class IngredientCollection(object):
    """ingredient class"""

    def __init__(self):
        """constructor"""

        self.ingredient_list = []

    def get_ingredient_list(self):
        """capture user input ingredients"""

        add_ingredient = True
        while add_ingredient:
            user_prompt = raw_input(
                'Are there ingredients to add? ').strip().lower()

            if len(user_prompt) > 0 and user_prompt[0] == 'y':
                print 'Please add your ingredient. '
                new_ingredient = Ingredient()
                self.ingredient_list.append(new_ingredient)
                new_ingredient.get_user_input()

            else:
                add_ingredient = False
                print 'You\'re finished entering ingredients! Thank you!'

    def input_to_string(self):
        """return entered values to user"""

        ing_list = ''
        for item in self.ingredient_list:
            ing_list = ing_list + item.input_to_string() + '\n'

        return ing_list

    def search_ingredient_collection(self, keyword):
        """ingredient collection search method"""

        for item in self.ingredient_list:
            if item.search_ingredient(keyword):
                return True

        return False


class Ingredient(object):
    """defines individual ingredients"""

    def __init__(self):
        """constructor"""

        self.quantity = 0
        self.unit = ''
        self.name = ''
        self.notes = ''

    def get_user_input(self):
        """Gathers quantity, unit ingredient name and notes.

        Quantity is captured as string and remains so to allow for flexibility
        in entering (i.e.: 1/3 or compound fractions are allowed and will
        display in '\human friendly'\ form. This value is not required.

        Unit remains as string and allows abbreviations or full words. This
        value is not required.

        Ingredient name is required.

        Additional notes allows the users to capture any information required
        for the recipe but not captured elsewhere. (e.g.: softened, sifted,
        separated, minced, chopped, etc.)"""

        self.quantity = raw_input('Quantity? (if none, press Enter) ').strip()

        self.unit = raw_input(
            'Unit of Measure? (if none, press Enter) ').strip()

        self.name = raw_input('Ingredient Name? ').strip()
        while self.name.strip() == '':
            self.name = raw_input('Cannot be blank. Ingredient Name? ').strip()

        self.notes = raw_input(
            'Additional Notes/Information? (if none, press Enter) ').strip()

    def input_to_string(self):
        """convert raw input into string"""

        ingredient = '{0} {1} {2} {3}'.format(
            self.quantity, self.unit, self.name, self.notes)

        return ingredient

    def search_ingredient(self, keyword):
        """ingredient search method"""

        return keyword in self.input_to_string()


class DirectionCollection(object):
    """collects user input directions"""

    def __init__(self):
        """constructor"""

        self.direction_list = []

    def get_direction_list(self):
        """captures user input recipe directions"""

        add_direction = True
        while add_direction:
            user_prompt = raw_input(
                'Are there directions to add? ').strip().lower()

            if len(user_prompt) > 0 and user_prompt[0] == 'y':
                print 'Please add your direction. '
                new_direction = Direction()
                self.direction_list.append(new_direction)
                new_direction.get_user_input()

            else:
                add_direction = False
                print 'You\'re finished entering directions! Thank you!'

    def input_to_string(self):
        """return entered values to user"""

        dir_string = ''
        counter = 0
        for item in self.direction_list:
            counter += 1
            dir_string = dir_string + '{}. {}\n'.format(counter, item.direction)

        return dir_string

    def search_dir_collection(self, keyword):
        """ingredient collection search method"""

        for item in self.direction_list:
            if item.search_direction(keyword):
                return True

        return False


class Direction(object):
    """defines individual directions"""

    def __init__(self):
        """constructor"""

        self.direction = ''

    def get_user_input(self):
        """method to gather user input recipe directions"""

        self.direction = raw_input('Direction: ')
        while self.direction.strip() == '':
            self.direction = raw_input(
                'Cannot be blank. Please enter direction: ')

        return self.direction

    def search_direction(self, keyword):
        """method to search for keyword in direction"""

        return keyword in self.direction


if __name__ == "__main__":

    rec_mgmt = RecipeManagement()
    rec_col = rec_mgmt.read_recipes()
    #rec_col = RecipeCollection()
    while True:
        if not rec_col.recipe_actions():
            break
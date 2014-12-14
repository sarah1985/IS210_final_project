#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Final Project...here we go!"""

import os
import os.path
import pickle
import fractions


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


# def change_yield(current, new):
#     """takes current yield and new yield value as arguments.
#         returns recipe with new yields"""
#
#     new_yield = raw_input(
#         'Please enter the yield change. ('
#         'e.g.: to double a recipe, enter 2. To halve it, enter 0.5)')
#         #fractions.Fraction(current * new)
#
#     return new_yield


class RecipeCollection(object):
    """creates custom '\cookbook'\!"""

    def __init__(self):
        """constructor"""

        #self.cookbook =

    def seach_recipes(self):
        """method to search all recipes for entered keyword and return
        results to the user for review"""

        search_results = []

        #for


        if len(search_results) > 0:
            for item in search_results:
                print item

        else:
            print 'No results found! Please try another search.'


class Recipe(object):
    """defines the recipe and its components"""

    def __init__(self):
        """constructor"""

        self.new_recipe = []

    def create_new_recipe(self):
        """combines ingredient collection and direction collection to create
        new recipe and add to file"""

        ingredient_collection = IngredientCollection()
        direction_collection = DirectionCollection()




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

    def user_review(self):
        """return entered values to user"""

        for item in self.ingredient_list:
            print item.input_to_string()

    def search_ingredient_collection(self, keyword):
        """ingredient collection search method"""

        for item in self.ingredient_list:
            return True if item.search_ingredient(keyword) else False


class Ingredient(object):
    """defines individual ingredients"""

    def __init__(self):
        """constructor"""

        self.quantity = 0
        self.unit = ''
        self.name = ''
        self.notes = ''

    def get_user_input(self):
        """input method"""

        self.quantity = raw_input("Quantity? ").strip()
        while not self.quantity.isdigit():
            self.quantity = raw_input("Not a valid number. Quantity? ")
        self.quantity = fractions.Fraction(int(self.quantity), 1)

        self.unit = raw_input('Unit of Measure? ').strip()

        self.name = raw_input('Ingredient Name? ').strip()
        while self.name.strip() == '':
            self.name = raw_input('Cannot be blank. Ingredient Name? ')

        self.notes = raw_input('Additional Notes/Information? ')

    def input_to_string(self):
        """convert raw input into string"""

        ingredient = '{0} {1} {2} {3}'.format(
            self.quantity, self.unit, self.name, self.notes)

        return ingredient

    def search_ingredient(self, keyword):
        """ingredient search method"""

        # search_result = []
        #
        # keyword = raw_input(
        #     "What keyword would you like to search? ").strip().lower()
        #
        # if keyword in ingredient:
        #     search_result.append(ingredient)
        #
        # else:
        #     print "No matches found!"
        #
        # return search_result

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

    def user_review(self):
        """return entered values to user"""

        for item in self.direction_list:
            print item.direction_list()

    def search_ingredient_collection(self, keyword):
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

        self.direction = raw_input('Please enter direction: ')
        while self.direction.strip() == '':
            self.direction = raw_input(
                'Cannot be blank. Please enter direction: ')

        return self.direction

    def search_direction(self, keyword):
        """method to search for keyword in direction"""

        return keyword in self.direction

if __name__ == "__main__":
    # test = Ingredient()
    # test.get_user_input()
    # print test.input_to_string()

    test_list = IngredientCollection()
    test_list.get_ingredient_list()
    print test_list.user_review()

    create_recipe = RecipeManagement()
    create_recipe.set('key', test_list)
    create_recipe.open()
    create_recipe.flush()
    create_recipe.close()

    recall_recipe = RecipeManagement()
    recall_recipe.open()
    recall_list = recall_recipe.get('key')
    recall_recipe.close()
    recall_list.IngredientCollection.user_review()
    print recall_list.search_ingredient_collection(
        raw_input('Enter search keyword: '))
import db_connect


class RecipeClass(object):
    """Class for recipe item with attributes - id, name, ingredients, steps """

    def __init__(self, id, name, ingredients, steps):
        """Constructor definition - Initialize variables"""
        self.__id = id
        self.name = name
        self.ingredients = ingredients
        self.steps = steps

    def add_recipe(self):
        """For adding new recipe"""
        if self.__check_exists() is None:
            db_connect.add_recipe(self.name, self.ingredients, self.steps)
            return "Recipe successfully added to database!"
        else:
            return "Recipe already exits! Please upload a different recipe or enter a different name"

    def __check_exists(self):
        """Check if item exists on db"""
        return db_connect.get_recipe_name(self.name)

    def __str__(self):
        """Return recipe attributes in str format"""
        return "Recipe is {}".format(self.name)

    def __repr__(self):
        """Used in interpreter - return __str__"""
        return self.__str__()
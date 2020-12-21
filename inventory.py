import db_connect


class InventoryClass(object):
    """Class used for inventory item with
    attributes id, name, unit, quantity"""
    def __init__(self, id, name, unit, quantity):
        """Constructor definition - initialize attribute"""
        self.__id = id
        self.name = name
        self.unit = unit
        self.quantity = quantity

    def __str__(self):
        """Return attributes in str format"""
        return "{}\n{}\n{}".format(self.name, self.unit, self.quantity)

    def __repr__(self):
        """Used in interpreter - return __str__"""
        return self.__str__()

    def __check_exists(self):
        """Check if item exists on db"""
        return db_connect.get_item_name(self.name)

    def insert(self):
        """For calling function to insert into db"""
        if len(self.__check_exists()) == 0:
            db_connect.add_inventory(self.name, self.unit, self.quantity)
            message = "Item successfully added to database!"
        else:
            message = "Item already exists. " \
                      "Please go to inventory list and update quantity!"
        return message

    def update(self):
        """For calling function to update inventory item in db"""
        db_connect.update_inventory(self.quantity, self.name)

    def __add__(self, other):
        pass








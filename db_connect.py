from flask import Flask, render_template, request
from wtforms import Form, validators, FloatField, IntegerField, StringField, FileField
import mysql.connector
import string
import math
import os
import recipe
from inventory import InventoryClass

app = Flask(__name__)

my_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restaurant_db"
)

my_cursor = my_db.cursor()


def get_inventory():
    """Return all recipes from database"""
    my_cursor.execute("SELECT * FROM inventory")
    return my_cursor.fetchall()


def get_item(id):
    """Return specific item from inventory"""
    my_cursor.execute("SELECT * FROM inventory where id = %s ", (id,))
    return my_cursor.fetchall()


def get_item_name(name):
    """Return specific item from inventory"""
    my_cursor.execute("SELECT * FROM inventory where name = %s ", (name,))
    return my_cursor.fetchall()


def add_recipe(name, ingredients, steps):
    """Insert recipe to database"""
    sql = "INSERT INTO recipe(name, ingredients, steps) values (%s, %s, %s)"
    my_cursor.execute(sql, (name, ingredients, steps))
    my_db.commit()


def get_all_recipe():
    """Get all recipes from database"""
    my_cursor.execute("SELECT id, name FROM recipe")
    return my_cursor.fetchall()


def get_recipe(id):
    """Return specific recipe from inventory"""
    my_cursor.execute("SELECT name, ingredients, steps FROM recipe where id = %s ", (id,))
    return my_cursor.fetchall()


def get_ingredients(id):
    """Return ingredients of a recipe"""
    my_cursor.execute("SELECT ingredients from recipe where id = %s", (id,))
    return my_cursor.fetchone()


def get_item_cnt(name):
    """Return count of inventory"""
    my_cursor.execute("SELECT quantity, unit FROM inventory WHERE name = %s", (name,))
    return my_cursor.fetchone()


def add_inventory(name, unit, quantity):
    """Insert into database"""
    param_tuple = (name, unit, quantity)
    sql_formula = "INSERT into inventory(name, unit, quantity) values(%s, %s, %s)"
    my_cursor.execute(sql_formula, param_tuple)
    my_db.commit()


def update_inventory(quantity, name):
    """Update inventory item"""
    param_tuple = (quantity, name)
    sql_formula = "Update inventory set quantity = %s where name = %s"
    my_cursor.execute(sql_formula, param_tuple)
    my_db.commit()


def get_recipe_name(name):
    """Return recipe if it exists"""
    my_cursor.execute("SELECT * FROM recipe WHERE name = %s", (name,))
    return my_cursor.fetchone()
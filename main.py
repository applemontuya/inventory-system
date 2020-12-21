import db_connect
import os
from flask import Flask, render_template, redirect, url_for, request
from inventory import InventoryClass
from forms import InventoryForm, NewRecipeForm, EstimateForm
from recipe import RecipeClass


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Route and function for landing page"""
    return render_template("index.html")


@app.route("/add-recipe", methods=["Get", "Post"])
def add_recipe():
    """Route and function for adding recipe"""
    message = None
    form = NewRecipeForm(request.form)
    input_list = []
    ingredient_set = set()
    step_list = []
    if request.method == "POST":
        input_name = form.name_field.data
        try:
            # store the file contents as a string
            input_val = open(form.file_field.data, "r")
            for line in input_val:
                input_list.append(line)
            cnt_1 = 0
            cnt_2 = 0
            for cnt in input_list:
                if cnt.strip("\n").lower() == "ingredients:":
                    cnt_1 += 1
                elif cnt.strip("\n").lower() == "steps:":
                    cnt_2 += 1
                elif cnt_1 > 0 and cnt_2 == 0:
                    ingredient_set.add(cnt.strip("\n"))
                elif cnt_2 > 0:
                    step_list.append(cnt.strip("\n"))
            # Convert sets to strings separated by ',' for saving to DB
            ingredient_string = ','.join(ingredient_set)
            step_string = ','.join(step_list)
            # Create recipe object
            recipe = RecipeClass(1, input_name.lower(),
                                 ingredient_string, step_string)
            # Call method that saves recipe to DB
            message = recipe.add_recipe()
        except Exception as e:
            message = "Python error: {}".format(e)
    return render_template("add-recipe.html",
                           template_form=form, message=message)


@app.route("/recipes", methods=["GET"])
def view_recipes():
    """Route and function for viewing all recipes"""
    # Get all recipes from database
    recipe = db_connect.get_all_recipe()
    return render_template("recipe_list.html", recipe_list=recipe)


@app.route("/view-recipe/<id>", methods=["GET", "POST"])
def view_recipe(id):
    """Route and function for viewing specific recipe"""
    # Get recipe from database
    output_list = db_connect.get_recipe(id)
    recipe_list = []
    form = EstimateForm(request.form)
    for item in output_list:
        for i in item:
            recipe_list.append(i.replace(",","<br/>"))
    if request.method == 'POST' and form.validate():
        return redirect(url_for("get_summary",
                                recipe_id=id, servings=form.servings_field.data))
    else:
        return render_template("view-recipe.html",
                               recipe=recipe_list, template_form=form)


@app.route("/inventory", methods=["GET"])
def view_inventory():
    """Route and function for viewing inventory list"""
    # Get inventory items from database
    items = db_connect.get_inventory()
    return render_template("inventory.html", item_list=items)


@app.route("/view-item/<id>", methods=["GET", "POST"])
def view_item(id):
    """Route and function for viewing and updating inventory item"""
    form = InventoryForm(request.form)
    message = None
    # Get item from database
    items = db_connect.get_item(id)
    # Set formfield values with db value
    form.name_field.data = items[0][1]
    form.unit_field.data = items[0][2]
    if request.method == 'POST':
        try:
            # Get formfield values and create inventory object
            name = form.name_field.data
            quantity = form.quantity_field.data
            unit = form.unit_field.data
            inventory = InventoryClass(1, name.lower(), unit, quantity)
            # Update inventory object value
            inventory.update()
            message = "Item successfully updated!"
        except Exception as e:
            message = "Python error: {}".format(e)
    return render_template("view-item.html", template_form=form, message=message)


@app.route("/add-item", methods=["GET", "POST"])
def add_item():
    """Route and function for adding inventory item"""
    form = InventoryForm(request.form)
    message = None
    if request.method == 'POST':
        try:
            name = form.name_field.data
            quantity = form.quantity_field.data
            unit = form.unit_field.data
            inventory = InventoryClass(1,
                            name.lower(), unit.lower(), quantity.lower())
            message = inventory.insert()
        except Exception as e:
            message = "Python error: {}".format(e)
    return render_template("add-item.html",
                           template_form=form, message=message)


@app.route("/summary/<recipe_id>/<servings>", methods=["GET", "POST"])
def get_summary(recipe_id, servings):
    """Route and function for getting the summary/estimate
    of needed inventory with chosen recipe and entered servings"""
    # Get ingredients from database
    ingredients_var = db_connect.get_ingredients(recipe_id)
    ingredients_dict = {}
    inventory_dict = {}
    need_dict = {}
    # Go through the ingredients
    for item in ingredients_var:
        for i in item.split(','):
            quant, unit, name = i.split()
            if name not in ingredients_dict.keys():
                # Save to dictionary the needed ingredients
                # With quantity multiplied by # of servings
                ingredients_dict[name] = str(float(quant)
                                             * float(servings)) + ' ' + unit
            # Get the inventory count of the ingredient
            inventory_var = db_connect.get_item_cnt(name)
            # If item exists, add to inventory dict; if not, update the needed items.
            if inventory_var:
                item_cnt = inventory_var[0]
                item_unit = inventory_var[1]
                inventory_dict[name] = str(item_cnt) \
                                 + " " + str(item_unit)
                order_quantity = float(quant) \
                                 * float(servings) - float(item_cnt)
                if order_quantity < 0: order_quantity = 0
                need_dict[name] = str(order_quantity) + " " + str(item_unit)
            else:
                need_dict[name] = str(float(quant) * float(servings)) + " " + str(unit)
    return render_template("summary.html", ingredients=ingredients_dict,
                           inventory=inventory_dict, to_order=need_dict)


if __name__ == '__main__':
    app.run(debug=True)
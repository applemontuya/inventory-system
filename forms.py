from wtforms import Form, validators, FloatField, IntegerField, StringField, FileField


class NewRecipeForm(Form):
    """Form for adding a new recipe"""
    name_field = StringField(validators=[validators.required()])
    file_field = FileField(validators=[validators.required()])


class InventoryForm(Form):
    """Form for adding new inventory item """
    name_field = StringField(validators=[validators.required()])
    unit_field = StringField(validators=[validators.required()])
    quantity_field = StringField(validators=[validators.InputRequired()])


class EstimateForm(Form):
    """Form for requesting ingredients estimate"""
    servings_field = IntegerField(validators=[validators.required()])
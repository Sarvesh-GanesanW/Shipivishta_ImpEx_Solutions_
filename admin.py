from flask_admin import Admin
from flask_admin.contrib.pymongo import ModelView
from flask_admin.form import rules
from wtforms import Form, StringField, TextAreaField, validators
from db import get_db_connection
import logging

# Define WTForms form classes for MongoDB collections
class ServiceForm(Form):
    category = StringField('Category', validators=[validators.DataRequired()])
    name = StringField('Name', validators=[validators.DataRequired()])
    description = TextAreaField('Description', validators=[validators.DataRequired()])
    benefits = TextAreaField('Benefits', validators=[validators.DataRequired()])
    how_to_apply = TextAreaField('How to Apply', validators=[validators.DataRequired()])

class ResourceForm(Form):
    title = StringField('Title', validators=[validators.DataRequired()])
    description = TextAreaField('Description', validators=[validators.DataRequired()])
    file_url = StringField('File URL', validators=[validators.DataRequired()])

# Initialize the Flask-Admin extension
def setup_admin(app):
    try:
        admin = Admin(app, name='Shipivishta CMS', template_mode='bootstrap3')

        # Database connection
        db = get_db_connection()

        # Customized admin views
        class ServicesView(ModelView):
            can_create = True
            can_edit = True
            can_delete = True
            column_list = ('category', 'name', 'description', 'benefits', 'how_to_apply')
            form = ServiceForm
            
            form_create_rules = [
                rules.FieldSet(('category', 'name', 'description', 'benefits', 'how_to_apply'), 'Service Info')
            ]
            
            form_edit_rules = form_create_rules

        class ResourcesView(ModelView):
            can_create = True
            can_edit = True
            can_delete = True
            column_list = ('title', 'description', 'file_url')
            form = ResourceForm
            
            form_create_rules = [
                rules.FieldSet(('title', 'description', 'file_url'), 'Resource Info')
            ]
            
            form_edit_rules = form_create_rules

        # Add views to the admin interface
        admin.add_view(ServicesView(db['Services'], 'Services'))
        admin.add_view(ResourcesView(db['Resources'], 'Resources'))
        logging.info("Admin interface setup successfully.")
    except Exception as e:
        logging.error("Failed to set up the admin interface: %s", e, exc_info=True)
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length

import logging

class ServiceForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    benefits = TextAreaField('Benefits', validators=[DataRequired(), Length(min=10)])
    how_to_apply = TextAreaField('How to Apply', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        logging.info("ServiceForm initialized")

class ResourceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    file_url = FileField('File URL', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        logging.info("ResourceForm initialized")

try:
    logging.basicConfig(level=logging.INFO)
    logging.info("Forms for admin panel loaded successfully.")
except Exception as e:
    logging.error("Error loading forms for admin panel: %s", e, exc_info=True)
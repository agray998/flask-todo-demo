from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from datetime import date
from application.models import Todo, Project

class NameCheck():
    def __init__(self, message = "Project name already exists"):
        self.message = message
    
    def __call__(self, form, field):
        if field.data in [project.project_name for project in Project.query.all()]:
            raise(ValidationError(self.message))

class DateCheck():
    def __init__(self, message="Due date must be in the future"):
        self.message = message
    
    def __call__(self, form, field):
        if field.data < date.today():
            raise ValidationError(self.message)

class AddToDo(FlaskForm):
    title = StringField("Task Name", validators=[DataRequired()])
    desc = StringField("Task Description")
    status = SelectField("Status", choices=[('todo', 'todo'), ('done', 'done')])
    proj_id = SelectField("Project to Link", choices=[])
    submit = SubmitField("Add Item")

class AddProject(FlaskForm):
    name = StringField("Project Name", validators=[NameCheck()])
    due = DateField("Due Date", validators = [DateCheck()])
    submit = SubmitField("Add Project")

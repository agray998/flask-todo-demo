from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, SubmitField

class AddToDo(FlaskForm):
    title = StringField("Task Name")
    desc = StringField("Task Description")
    status = SelectField("Status", choices=[('todo', 'todo'), ('done', 'done')])
    proj_id = IntegerField("Project to Link")
    submit = SubmitField("Add Item")

class AddProject(FlaskForm):
    name = StringField("Project Name")
    due = DateField("Due Date")
    submit = SubmitField("Add Project")
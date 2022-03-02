from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import Todo, Project
from datetime import date, timedelta

class TestBase(TestCase):
    def create_app(self): # Sets test configuration
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db',
            SECRET_KEY = "test secret key",
            DEBUG = True,
            WTF_CSRF_ENABLED = False
        )

        return app
    
    def setUp(self): # Run before each test
        db.create_all()
        sample_proj = Project(project_name = "Sample Project", due_date = date.today() + timedelta(30))
        sample_todo = Todo(title = "Sample Item", desc = "A sample task for testing", status = "todo", proj_id = 1)

        db.session.add(sample_proj)
        db.session.add(sample_todo)
        db.session.commit()
    
    def tearDown(self): # Run after each test
        db.session.remove()
        db.drop_all()

class TestHome(TestBase):
    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assert200(response)
        self.assertIn(b'Sample Item', response.data)

class TestAddTodo(TestBase):
    def test_create_get(self):
        response = self.client.get(url_for('create'))
        self.assert200(response)
        self.assertIn(b'Task Name', response.data)
    
    def test_create_post(self):
        response = self.client.post(
            url_for('create'),
            data = dict(title="Sample task 2", desc="Test adding todo", status='todo', proj_id = 1),
            follow_redirects = True
        )
        self.assert200(response)
        self.assertIn(b'Sample task 2', response.data)
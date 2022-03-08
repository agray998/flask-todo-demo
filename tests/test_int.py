from flask_testing import LiveServerTestCase
from selenium import webdriver
from urllib.request import urlopen
from flask import url_for
from datetime import date, timedelta

from application import app, db
from application.models import Todo, Project
from application.forms import AddProject

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db',
            LIVESERVER_PORT = 5050,
            DEBUG = True,
            TESTING = True
        )
        return app
    
    def setUp(self):
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options = chrome_options)
        db.create_all()
        self.driver.get(f'http://localhost:{self.TEST_PORT}/create-proj')

    def tearDown(self):
        self.driver.quit()
        db.drop_all()
    
    def test_server_running(self):
        response = urlopen('http://localhost:5050/create-proj')
        self.assertEqual(response.code, 200)
    
class TestAddProject(TestBase):
    TEST_CASES = ('Project 1', date.today() + timedelta(30)), ('Project 2', date.today() + timedelta(14))

    def submit_input(self, case):
        self.driver.find_element_by_xpath('/html/body/div/form/input[2]').send_keys(case[0])
        self.driver.find_element_by_xpath('/html/body/div/form/input[3]').click()
        self.driver.find_element_by_xpath('/html/body/div/form/input[3]').send_keys(str(case[1]).replace('-',''))
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()

    def test_add_proj(self):
        for case in self.TEST_CASES:
            self.submit_input(case)
            projs = Project.query.filter_by(project_name=case[0]).all()
            self.assertNotEqual(projs, None)

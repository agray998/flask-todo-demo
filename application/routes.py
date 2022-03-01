from flask import redirect, url_for, render_template
from application import app, db
from application.models import Todo, Project
from datetime import date, timedelta

@app.route('/')
def home():
    num_todos = Todo.query.count()
    todos = [str(todo) + " " + str(todo.project) for todo in Todo.query.all()]
    return render_template('index.html', num = num_todos, todos = todos)

@app.route('/search=<keyword>')
def search(keyword):
    data = db.session.execute(f"SELECT * FROM todo WHERE desc LIKE '%{keyword}%'")
    data = list(data)
    num_results = len(data)
    return render_template('search.html', res = [str(res) for res in data], n = num_results)

@app.route('/done')
def done():
    res = [str(t) for t in Todo.query.filter_by(status='done').order_by(Todo.title.desc()).all()]
    return render_template('done.html', res = res)

@app.route('/create/<int:pnum>/<title>/<desc>')
def create(pnum, title, desc):
    todo = Todo(title=title, desc=desc, status='todo', proj_id = pnum)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/create-proj/<name>')
def create_project(name):
    new_proj = Project(project_name = name, due_date = date.today() + timedelta(30))
    db.session.add(new_proj)
    db.session.commit(),
    return redirect(url_for('home'))

@app.route('/update/<int:pk>/<newstatus>')
@app.route('/update/<int:pk>/<newtitle>/<newstatus>')
def update(pk, newstatus, newtitle = None): # defining multiple routes and setting default val in function def allows the user to either update just the status, or update the task description and status
    todo = Todo.query.get(pk)
    if newtitle:
        todo.title = newtitle
    todo.status = newstatus
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete/<int:i>')
def delete(i):
    todo = Todo.query.get(i)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))
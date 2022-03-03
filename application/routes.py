from flask import redirect, url_for, render_template, request
from application import app, db
from application.models import Todo, Project
from application.forms import AddToDo, AddProject
# from datetime import date, timedelta

@app.route('/')
def home():
    num_todos = Todo.query.count()
    todos = Todo.query.all()
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

@app.route('/create-todo', methods=['GET', 'POST'])
def create():
    message = None
    projects = Project.query.all()
    form = AddToDo()
    form.proj_id.choices.extend([(project.pk, str(project)) for project in projects])
    if request.method == 'POST':
        if not form.validate_on_submit():
            message = "Task name cannot be blank"
            return render_template('add_todo.html', form = form, ptitle = "Add Item", message = message)
        title = form.title.data
        desc = form.desc.data
        status = form.status.data
        proj = int(form.proj_id.data)
        new_todo = Todo(title = title, status = status, desc = desc, proj_id = proj)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_todo.html', form = form, ptitle = "Add Item", message = message)

@app.route('/create-proj', methods=['GET', 'POST'])
def create_project():
    message = None
    form = AddProject()
    if request.method == 'POST':
        if not form.validate_on_submit():
            message = ""
            for field in ['name', 'due']:
                try:
                    err = eval(f"form.{field}.errors[-1]")
                except IndexError:
                    err = ""
                message += err + ", "
            return render_template('add_proj.html', form = form, message = message)
        name = form.name.data
        date = form.due.data
        new_proj= Project(project_name = name, due_date = date)
        db.session.add(new_proj)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_proj.html', form = form, message = message)

@app.route('/update/<int:pk>', methods=['GET', 'POST'])
def update(pk):
    todo = Todo.query.get(pk)
    projects = Project.query.all()
    form = AddToDo()
    form.proj_id.choices.extend([(project.pk, str(project)) for project in projects])
    if request.method == 'POST':
        todo.title = form.title.data
        todo.desc = form.desc.data
        todo.status = form.status.data
        todo.proj_id = int(form.proj_id.data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_todo.html', form = form, ptitle = "Update Item")

@app.route('/delete/<int:i>')
def delete(i):
    todo = Todo.query.get(i)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('home'))
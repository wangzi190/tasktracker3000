from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
tasks = Blueprint('tasks', __name__, url_prefix='/tasks', template_folder='templates/tasks')

@tasks.route("/")
def menu():
    return render_template("/menu.html")

@tasks.route("/view")
@login_required
def view():
    from main import Task
    tasks = Task.query
    return render_template("/view.html", tasks=tasks)

@tasks.route("/create")
def create():
    return render_template("/create.html")

@tasks.route("/create", methods=['POST'])
def task_create():
    from main import Task, db
    taskName=request.form['taskName']
    monthDayYear=request.form['monthDayYear']
    value=request.form['value']
    sections=request.form['sections']
    if taskName and monthDayYear:
        if value != 0:
            if sections != 0:
                monthDayYear = str(monthDayYear)
                splitDate = monthDayYear.split("-")
                newTask = Task(
                    user_id=current_user.id,
                    month=splitDate[1],
                    day=splitDate[2],
                    year=splitDate[0],
                    taskName=str(taskName),
                    category='category',
                    sections=sections,
                    value=value,
                    completed=False,
                    stickers=0
                )
                db.session.add(newTask)
                db.session.commit()
                flash('Task created successfully.')
                return redirect(url_for('tasks.view'))
            else:
                flash('Task cannot have zero sections. Please try again.')
        else:
            flash('Task cannot have value of zero. Please try again.')
    else:
        flash('Missing required field. Please try again.')
    return render_template("/create.html")

@tasks.route("/edit")
def edit():
    return render_template("/edit.html")

@tasks.route("/delete")
def delete():
    return render_template("/delete.html")

@tasks.route("/categories")
@login_required
def categories():
    return render_template("/categories.html")

@tasks.route("/categories", methods=['POST'])
@login_required
def categories_action():
    from main import Category, db
    categoryName=request.form['categoryName']
    newCategory = Category(
        user_id=current_user.id,
        categoryName=categoryName
    )
    db.session.add(newCategory)
    db.session.commit()

    return render_template("/categories.html")

@tasks.route("/stickers")
@login_required
def stickers():
    return render_template("/stickers.html")
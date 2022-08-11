from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
tasks = Blueprint('tasks', __name__, url_prefix='/tasks', template_folder='templates/tasks')

@tasks.route("/view")
def view():
    return render_template("/view.html")

@tasks.route("/create")
def create():
    return render_template("/create.html")

@tasks.route("/create", methods=['POST'])
def create_action():
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
                    user_id=00000000,
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

@tasks.route("/categories")
@login_required
def categories():
    return render_template("/categories.html")

@tasks.route("/stickers")
@login_required
def stickers():
    return render_template("/stickers.html")
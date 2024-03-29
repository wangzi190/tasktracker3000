from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
tasks = Blueprint('tasks', __name__, url_prefix='/tasks', template_folder='templates/tasks')

@tasks.route("/")
@login_required
def menu():
    return render_template("/menu.html")

@tasks.route("/view")
@login_required
def view():
    from main import Task
    tasks = Task.query
    return render_template("/view.html", tasks=tasks)

@tasks.route("/create")
@login_required
def create():
    from main import Category
    categories = Category.query
    return render_template("/create.html", categories=categories)

@tasks.route("/points")
@login_required
def points():
    return render_template("/points.html")

@tasks.route("/create", methods=['POST'])
def task_create():
    from main import Task, db
    taskName=request.form['taskName']
    monthDayYear=request.form['monthDayYear']
    category=request.form['category']
    value=request.form['value']
    sections=request.form['sections']
    if taskName and monthDayYear:
        if value != 0:
            if sections != 0:
                monthDayYear = str(monthDayYear)
                splitDate = monthDayYear.split("-")
                if category:
                    category=category
                else:
                    category="N/A"
                newTask = Task(
                    user_id=current_user.id,
                    month=splitDate[1],
                    day=splitDate[2],
                    year=splitDate[0],
                    taskName=str(taskName),
                    category=category,
                    progress=0,
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
@login_required
def edit():
    return render_template("/edit.html")

@tasks.route("/delete")
@login_required
def delete():
    from main import Task
    tasks = Task.query
    return render_template("/delete.html", tasks=tasks)

@tasks.route("/delete", methods=['POST'])
@login_required
def tasks_delete():
    from main import Task, db
    toDelete=request.form['taskToDelete']
    if toDelete:
        Task.query.filter_by(id=toDelete).delete()
        db.session.commit()
        flash('Task successfully deleted.')
        return redirect(url_for('tasks.view'))
    else:
        flash('Missing required field. Please try again.')
    return render_template("/delete.html", tasks=tasks)

"""taskName=request.form['taskName']"""

@tasks.route("/categories")
@login_required
def categories():
    from main import Category
    categories = Category.query
    return render_template("/categories.html", categories=categories)

@tasks.route("/categories_edit", methods=['POST'])
def categories_edit():
    from main import Category, db
    return render_template("/categories.html")

@tasks.route("/categories_delete", methods=['POST'])
def categories_delete():
    from main import Category, db
    toDelete=request.form['categoryToDelete']
    if toDelete != "null":
        Category.query.filter_by(id=toDelete).delete()
        db.session.commit()
        flash('Category successfully deleted.')
        return redirect(url_for('tasks.categories'))
    else:
        flash('Missing required field. Please try again.')
    return render_template("/categories.html")

@tasks.route("/categories_action", methods=['POST'])
def categories_action():
    from main import Category, db
    categoryName=request.form['categoryName']
    if categoryName:
        newCategory = Category(
            current_user.id,
            str(categoryName)
        )
        db.session.add(newCategory)
        db.session.commit()
        flash('Category created successfully.')
        return redirect(url_for('tasks.categories'))
    else:
        flash('Missing required field. Please try again.')
    return render_template("/categories.html")

@tasks.route("/stickers")
@login_required
def stickers():
    return render_template("/stickers.html")

@tasks.route("/stickers_action", methods=['POST'])
def stickers_action():
    return render_template("/stickers.html")

@tasks.route("/stickerbook")
@login_required
def stickerbook():
    return render_template("/stickerbook.html")
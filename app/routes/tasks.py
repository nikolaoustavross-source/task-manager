from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, date
from ..models import Task
from .. import db
from ..weather import get_weather

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    status_filter = request.args.get('status', 'ALL')
    priority_filter = request.args.get('priority', 'ALL')

    query = Task.query.filter_by(user_id=current_user.id)

    if status_filter in ('PENDING', 'COMPLETED'):
        query = query.filter_by(status=status_filter)

    if priority_filter in ('LOW', 'MEDIUM', 'HIGH'):
        query = query.filter_by(priority=priority_filter)

    tasks = query.order_by(Task.created_at.desc()).all()

    weather = get_weather(current_user.city)

    total = Task.query.filter_by(user_id=current_user.id).count()
    pending = Task.query.filter_by(user_id=current_user.id, status='PENDING').count()
    completed = Task.query.filter_by(user_id=current_user.id, status='COMPLETED').count()

    return render_template(
        'dashboard.html',
        tasks=tasks,
        weather=weather,
        status_filter=status_filter,
        priority_filter=priority_filter,
        total=total,
        pending=pending,
        completed=completed,
        today=date.today(),
    )


@tasks_bp.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'MEDIUM')
        due_date_str = request.form.get('due_date', '')

        if not title:
            flash('Title is required.', 'danger')
            return render_template('task_form.html', action='Create', task=None)

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'danger')
                return render_template('task_form.html', action='Create', task=None)

        task = Task(
            title=title,
            description=description or None,
            priority=priority if priority in ('LOW', 'MEDIUM', 'HIGH') else 'MEDIUM',
            due_date=due_date,
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created!', 'success')
        return redirect(url_for('tasks.dashboard'))

    return render_template('task_form.html', action='Create', task=None)


@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'MEDIUM')
        status = request.form.get('status', 'PENDING')
        due_date_str = request.form.get('due_date', '')

        if not title:
            flash('Title is required.', 'danger')
            return render_template('task_form.html', action='Edit', task=task)

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'danger')
                return render_template('task_form.html', action='Edit', task=task)

        task.title = title
        task.description = description or None
        task.priority = priority if priority in ('LOW', 'MEDIUM', 'HIGH') else 'MEDIUM'
        task.status = status if status in ('PENDING', 'COMPLETED') else 'PENDING'
        task.due_date = due_date
        db.session.commit()
        flash('Task updated.', 'success')
        return redirect(url_for('tasks.dashboard'))

    return render_template('task_form.html', action='Edit', task=task)


@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.', 'info')
    return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.status = 'COMPLETED' if task.status == 'PENDING' else 'PENDING'
    db.session.commit()
    return redirect(url_for('tasks.dashboard'))

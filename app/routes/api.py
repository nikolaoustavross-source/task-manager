from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..models import Task
from .. import db

api_bp = Blueprint('api', __name__)


@api_bp.route('/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    """Return all tasks for the current user as JSON."""
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
@login_required
def api_get_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    return jsonify(task.to_dict())


@api_bp.route('/tasks', methods=['POST'])
@login_required
def api_create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    task = Task(
        title=data['title'],
        description=data.get('description'),
        priority=data.get('priority', 'MEDIUM'),
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api_bp.route('/tasks/<int:task_id>', methods=['PATCH'])
@login_required
def api_update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    if 'title' in data:
        task.title = data['title']
    if 'status' in data and data['status'] in ('PENDING', 'COMPLETED'):
        task.status = data['status']
    if 'priority' in data and data['priority'] in ('LOW', 'MEDIUM', 'HIGH'):
        task.priority = data['priority']
    db.session.commit()
    return jsonify(task.to_dict())


@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def api_delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({'deleted': True})


@api_bp.route('/stats', methods=['GET'])
@login_required
def api_stats():
    total = Task.query.filter_by(user_id=current_user.id).count()
    pending = Task.query.filter_by(user_id=current_user.id, status='PENDING').count()
    completed = Task.query.filter_by(user_id=current_user.id, status='COMPLETED').count()
    return jsonify({'total': total, 'pending': pending, 'completed': completed})

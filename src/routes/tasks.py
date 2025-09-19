from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.task import Task, TaskApplication
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def get_tasks():
    try:
        # Get query parameters
        category = request.args.get('category')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Build query
        query = Task.query.filter_by(status='pending')
        
        if category and category != 'Todos':
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(
                db.or_(
                    Task.title.contains(search),
                    Task.description.contains(search),
                    Task.location_address.contains(search)
                )
            )
        
        # Order by creation date (newest first)
        query = query.order_by(Task.created_at.desc())
        
        # Paginate
        tasks = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks.items],
            'total': tasks.total,
            'pages': tasks.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro interno do servidor'}), 500

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'message': 'Tarefa não encontrada'}), 404
        
        return jsonify({'task': task.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro interno do servidor'}), 500

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'location_address', 'price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} é obrigatório'}), 400
        
        # Parse scheduled_date if provided
        scheduled_date = None
        if data.get('scheduled_date'):
            try:
                scheduled_date = datetime.fromisoformat(data['scheduled_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'message': 'Formato de data inválido'}), 400
        
        # Create new task
        task = Task(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            location_address=data['location_address'],
            price=float(data['price']),
            client_id=current_user_id,
            scheduled_date=scheduled_date,
            estimated_duration=data.get('estimated_duration', '')
        )
        
        db.session.add(task)
        db.session.commit()
        
        # Update user's task count
        user = User.query.get(current_user_id)
        user.total_tasks_created += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Tarefa criada com sucesso',
            'task': task.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno do servidor'}), 500

@tasks_bp.route('/<int:task_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_task(task_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Check if task exists
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Tarefa não encontrada'}), 404
        
        # Check if user is the task owner
        if task.client_id == current_user_id:
            return jsonify({'message': 'Você não pode se candidatar à sua própria tarefa'}), 400
        
        # Check if user is a tasker
        user = User.query.get(current_user_id)
        if not user.is_tasker:
            return jsonify({'message': 'Apenas taskers podem se candidatar a tarefas'}), 400
        
        # Check if user already applied
        existing_application = TaskApplication.query.filter_by(
            task_id=task_id,
            tasker_id=current_user_id
        ).first()
        
        if existing_application:
            return jsonify({'message': 'Você já se candidatou a esta tarefa'}), 400
        
        # Create application
        application = TaskApplication(
            task_id=task_id,
            tasker_id=current_user_id,
            message=data.get('message', ''),
            proposed_price=float(data.get('proposed_price', task.price))
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Candidatura enviada com sucesso',
            'application': application.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno do servidor'}), 500

@tasks_bp.route('/<int:task_id>/applications', methods=['GET'])
@jwt_required()
def get_task_applications(task_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if task exists and user is the owner
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'message': 'Tarefa não encontrada'}), 404
        
        if task.client_id != current_user_id:
            return jsonify({'message': 'Acesso negado'}), 403
        
        applications = TaskApplication.query.filter_by(task_id=task_id).all()
        
        return jsonify({
            'applications': [app.to_dict() for app in applications]
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro interno do servidor'}), 500

@tasks_bp.route('/my-tasks', methods=['GET'])
@jwt_required()
def get_my_tasks():
    try:
        current_user_id = get_jwt_identity()
        task_type = request.args.get('type', 'created')  # created or assigned
        
        if task_type == 'created':
            tasks = Task.query.filter_by(client_id=current_user_id).order_by(Task.created_at.desc()).all()
        else:
            tasks = Task.query.filter_by(tasker_id=current_user_id).order_by(Task.created_at.desc()).all()
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks]
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro interno do servidor'}), 500


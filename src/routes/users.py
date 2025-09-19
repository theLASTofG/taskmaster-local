from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db, User
from src.models.review import Review

users_bp = Blueprint('users', __name__)

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro interno do servidor'}), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['first_name', 'last_name', 'phone', 'bio', 'is_tasker']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro interno do servidor'}), 500

@users_bp.route('/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404
        
        reviews = Review.query.filter_by(reviewed_id=user_id).order_by(Review.created_at.desc()).all()
        
        return jsonify({
            'reviews': [review.to_dict() for review in reviews]
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro interno do servidor'}), 500

@users_bp.route('/search', methods=['GET'])
def search_users():
    try:
        query = request.args.get('q', '')
        user_type = request.args.get('type', 'all')  # all, taskers, clients
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Build query
        users_query = User.query
        
        if user_type == 'taskers':
            users_query = users_query.filter_by(is_tasker=True)
        elif user_type == 'clients':
            users_query = users_query.filter_by(is_tasker=False)
        
        if query:
            users_query = users_query.filter(
                db.or_(
                    User.first_name.contains(query),
                    User.last_name.contains(query),
                    User.bio.contains(query)
                )
            )
        
        # Order by rating (for taskers) or creation date
        if user_type == 'taskers':
            users_query = users_query.order_by(User.rating.desc())
        else:
            users_query = users_query.order_by(User.created_at.desc())
        
        # Paginate
        users = users_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro interno do servidor'}), 500


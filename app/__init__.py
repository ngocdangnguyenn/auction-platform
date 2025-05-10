from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Configure login
    login_manager.login_view = 'auth.connexion'
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "info"

    with app.app_context():
        # Register blueprints
        from app.main.routes import main
        from app.auth.routes import auth
        from app.admin.routes import admin
        from app.client.routes import client
        
        app.register_blueprint(main)
        app.register_blueprint(auth, url_prefix='/auth')
        app.register_blueprint(admin, url_prefix='/admin')
        app.register_blueprint(client, url_prefix='/client')

        # User loader
        @login_manager.user_loader
        def load_user(user_id):
            from app.models import Utilisateur
            return Utilisateur.query.get(int(user_id))

        # Context processors
        @app.context_processor
        def inject_now():
            return {'now': datetime.utcnow()}

        @app.context_processor
        def inject_categories():
            from app.models import Produit
            categories = db.session.query(Produit.categorie).distinct().all()
            return {'categories': [cat[0] for cat in categories if cat[0]]}
        
        @app.context_processor
        def inject_notifications():
            if current_user.is_authenticated:
                try:
                    from app.models import Notification
                    count = db.session.query(Notification).filter_by(
                        utilisateur_id=current_user.id_utilisateur,
                        lue=False
                    ).count()
                    return {'notifications_counts': count}
                except Exception as e:
                    print(f"Erreur notifications: {str(e)}")
                    return {'notifications_counts': 0}
            return {'notifications_counts': 0}

    return app
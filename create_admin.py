from app import create_app, db
from app.models import Utilisateur
from werkzeug.security import generate_password_hash

# Créez l'application Flask
app = create_app()

# Ajoutez un administrateur dans le contexte de l'application
with app.app_context():
    # Vérifiez si un administrateur existe déjà
    admin_exist = Utilisateur.query.filter_by(email="admin@example.com").first()
    if admin_exist:
        print("Un administrateur avec cet email existe déjà.")
    else:
        # Créez un nouvel administrateur
        admin = Utilisateur(
            nom="Admin",
            prenom="Super",
            email="admin@example.com",
            mot_de_passe=generate_password_hash("admin123"),
            adresse="123 Rue Admin",
            code_postal="75000",
            ville="Paris",
            pays="France",
            telephone="0123456789",
            role="admin"  # Rôle administrateur
        )
        db.session.add(admin)
        db.session.commit()
        print("Administrateur créé avec succès !")
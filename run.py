import os
from app import create_app, db
from app.models import Utilisateur, Produit, Enchere, Mise, PackJetons, Transaction, Remboursement

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Configure les objets disponibles dans le shell Flask"""
    return {
        'db': db, 
        'Utilisateur': Utilisateur, 
        'Produit': Produit,
        'Enchere': Enchere,
        'Mise': Mise,
        'PackJetons': PackJetons,
        'Transaction': Transaction,
        'Remboursement': Remboursement
    }

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


from datetime import datetime
import traceback
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from app import db
from app.client.forms import PlacerEnchereForm
from app.models import Enchere, Notification, Produit, Mise

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Page d'accueil avec les enchères actives"""
    encheres_actives = Enchere.query.options(
        db.joinedload(Enchere.produit)
    ).filter(
        Enchere.date_fin > datetime.utcnow(),
        Enchere.statut == 'ouverte'
    ).order_by(Enchere.date_fin).all()
    
    return render_template('index.html', 
                         encheres=encheres_actives, 
                         title='Accueil')

@main.route('/enchere/<int:enchere_id>')
def detail_enchere(enchere_id):
    """Affiche le détail d'une enchère"""
    enchere = Enchere.query.options(
        db.joinedload(Enchere.produit),
        db.joinedload(Enchere.utilisateur_gagnant)
    ).get_or_404(enchere_id)

    # Vérifier et finaliser l'enchère si nécessaire
    if enchere.date_fin <= datetime.utcnow() and enchere.statut != 'terminee':
        from app.services.enchere_service import verifier_et_finaliser_enchere
        verifier_et_finaliser_enchere(enchere)
        db.session.refresh(enchere)

    form = PlacerEnchereForm(enchere_id=enchere.id_enchere)
    return render_template(
        'detail_enchere.html',
        enchere=enchere,
        form=form,
        current_time=datetime.utcnow()
    )
    
@main.route('/rechercher', methods=['GET'])
def rechercher_produits():
    """Recherche de produits par nom"""
    query = request.args.get('q', '').strip()
    produits = []
    if query:
        produits = Produit.query.filter(
            Produit.nom_produit.ilike(f"%{query}%")
        ).all()
    return render_template('main/recherche.html', 
                         query=query, 
                         produits=produits)

@main.route('/produit/<int:produit_id>')
def detail_produit(produit_id):
    """Détail d'un produit spécifique"""
    produit = Produit.query.get_or_404(produit_id)
    return render_template('main/detail_produit.html', produit=produit)

@main.route('/categories')
def categories():
    """Affiche les produits et enchères par catégorie"""
    categories = db.session.query(Produit.categorie).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    categorie_selectionnee = request.args.get('categorie')

    produits = []
    encheres = []
    if categorie_selectionnee:
        produits = Produit.query.filter_by(
            categorie=categorie_selectionnee
        ).all()
        # Use joinedload to eagerly load the produit relationship
        encheres = Enchere.query.options(
            db.joinedload(Enchere.produit)
        ).join(Produit).filter(
            Produit.categorie == categorie_selectionnee
        ).all()

    return render_template(
        'main/categories.html',
        categories=categories,
        categorie_selectionnee=categorie_selectionnee,
        produits=produits,
        encheres=encheres,
        title='Catégories'
    )

@main.route('/toutes_encheres', methods=['GET'])
def toutes_encheres():
    """Affiche toutes les enchères avec possibilité de filtrage"""
    filter_choice = request.args.get('filter', 'all')
    now = datetime.utcnow()

    # Base query with eager loading of produit relationship
    query = Enchere.query.options(db.joinedload(Enchere.produit))

    if filter_choice == "actuelles":
        encheres = query.filter(
            Enchere.date_fin >= now,
            Enchere.statut == 'ouverte'
        ).order_by(Enchere.date_fin.asc()).all()
    elif filter_choice == "terminees":
        encheres = query.filter(
            Enchere.date_fin < now,
            Enchere.statut == 'terminee'
        ).order_by(Enchere.date_fin.desc()).all()
    else:
        encheres = query.order_by(Enchere.date_fin.desc()).all()

    return render_template(
        'toutes_encheres.html',
        encheres=encheres,
        filter_choice=filter_choice,
        title='Toutes les enchères'
    )

@main.route('/a-propos')
def a_propos():
    """Page À propos"""
    return render_template('a_propos.html')

@main.route('/faq')
def faq():
    """Page FAQ"""
    return render_template('faq.html')
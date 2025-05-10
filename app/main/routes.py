from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from app import db
from app.client.forms import PlacerEnchereForm
from app.models import Enchere, Produit, Mise

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

@main.route('/enchere/<int:enchere_id>', methods=['GET', 'POST'])
def detail_enchere(enchere_id):
    """Détail d'une enchère spécifique"""
    enchere = Enchere.query.get_or_404(enchere_id)
    form = PlacerEnchereForm(enchere_id=enchere.id_enchere)

    from app.services.enchere_service import verifier_statut_enchere
    if verifier_statut_enchere(enchere):
        if enchere.statut == 'terminee' and not enchere.prix_gagnant:
            success = enchere.determine_gagnant()
            if success:
                db.session.refresh(enchere)
    
    mises_utilisateur = []
    if current_user.is_authenticated:
        mises_utilisateur = Mise.query.filter_by(
            enchere_id=enchere_id,
            utilisateur_id=current_user.id_utilisateur
        ).order_by(Mise.date_mise.desc()).all()

    return render_template(
        'detail_enchere.html',
        enchere=enchere,
        produit=enchere.produit,
        mises_utilisateur=mises_utilisateur,
        form=form,
        title=f'Enchère - {enchere.produit.nom_produit}',
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

@main.route('/comment-ca-marche')
def comment_ca_marche():
    """Page explicative du fonctionnement des enchères"""
    return render_template('comment_ca_marche.html',
                         title='Comment ça marche')

@main.route('/a-propos')
def a_propos():
    """Page À propos"""
    return render_template('a_propos.html')

@main.route('/faq')
def faq():
    """Page FAQ"""
    return render_template('faq.html')
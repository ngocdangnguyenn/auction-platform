from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user
from datetime import datetime
from app import db
from app.client.forms import PlacerEnchereForm
from app.models import Enchere, Produit, Mise

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Page d'accueil avec les enchères actives"""
    encheres_actives = Enchere.query.filter(
        Enchere.date_fin > datetime.utcnow(),
        Enchere.statut == 'ouverte'
    ).order_by(Enchere.date_fin).all()
    
    return render_template('index.html', encheres=encheres_actives, title='Accueil')

@main.route('/enchere/<int:enchere_id>', methods=['GET', 'POST'])
def detail_enchere(enchere_id):
    """Détail d'une enchère spécifique"""
    enchere = Enchere.query.get_or_404(enchere_id)
    produit = enchere.produit

    # Initialiser le formulaire
    form = PlacerEnchereForm(enchere_id=enchere.id_enchere)

    # Récupérer les mises de l'utilisateur courant pour cette enchère
    mises_utilisateur = []
    if current_user.is_authenticated:
        mises_utilisateur = Mise.query.filter_by(
            enchere_id=enchere_id,
            utilisateur_id=current_user.id_utilisateur
        ).order_by(Mise.date_mise.desc()).all()

    return render_template(
        'detail_enchere.html',
        enchere=enchere,
        produit=produit,
        mises_utilisateur=mises_utilisateur,
        form=form,  # Passer le formulaire au template
        title=f'Enchère - {produit.nom_produit}'
    )

@main.route('/comment-ca-marche')
def comment_ca_marche():
    """Page explicative du fonctionnement des enchères"""
    return render_template('comment_ca_marche.html', title='Comment ça marche')

from flask import request, render_template
from app.models import Produit

@main.route('/rechercher', methods=['GET'])
def rechercher_produits():
    query = request.args.get('q', '').strip()
    produits = []
    if query:
        produits = Produit.query.filter(Produit.nom_produit.ilike(f"%{query}%")).all()
    return render_template('main/recherche.html', query=query, produits=produits)

from flask import render_template
from app.models import Produit

@main.route('/produit/<int:produit_id>')
def detail_produit(produit_id):
    produit = Produit.query.get_or_404(produit_id)
    return render_template('main/detail_produit.html', produit=produit)

@main.route('/categories')
def categories():
    """Affiche les produits et enchères par catégorie"""
    # Récupérer toutes les catégories existantes
    categories = db.session.query(Produit.categorie).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]  # Extraire les noms des catégories

    # Récupérer la catégorie sélectionnée
    categorie_selectionnee = request.args.get('categorie')

    produits = []
    encheres = []
    if categorie_selectionnee:
        produits = Produit.query.filter_by(categorie=categorie_selectionnee).all()
        encheres = Enchere.query.join(Produit).filter(Produit.categorie == categorie_selectionnee).all()

    return render_template(
        'main/categories.html',
        categories=categories,
        categorie_selectionnee=categorie_selectionnee,
        produits=produits,
        encheres=encheres,
        title='Catégories'
    )

@main.route('/a-propos')
def a_propos():
    return render_template('a_propos.html')

@main.route('/faq')
def faq():
    return render_template('faq.html')

from flask import request, render_template
from datetime import datetime
from app.models import Enchere

@main.route('/toutes_encheres', methods=['GET'])
def toutes_encheres():
    # Récupère le paramètre 'filter' dans l'URL (par défaut, on affiche toutes les enchères)
    filter_choice = request.args.get('filter', 'all')
    now = datetime.utcnow()

    if filter_choice == "actuelles":
        # Enchères en cours : on considère celles qui ne sont pas terminées (date_fin >= now ou statut ouvert)
        encheres = Enchere.query.filter(Enchere.date_fin >= now, Enchere.statut == 'ouverte').order_by(Enchere.date_fin.asc()).all()
    elif filter_choice == "terminees":
        # Enchères terminées : date_fin < now et statut terminé
        encheres = Enchere.query.filter(Enchere.date_fin < now, Enchere.statut == 'terminee').order_by(Enchere.date_fin.desc()).all()
    else:
        # Toutes les enchères, triées par date de fin (du plus récent au plus ancien par exemple)
        encheres = Enchere.query.order_by(Enchere.date_fin.desc()).all()

    return render_template('toutes_encheres.html', encheres=encheres, filter_choice=filter_choice)


# Importation des modules

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from db_init import get_db,init_db

# Déclaration des variables

months = {
    0: "Tous",
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décenbre"
}

sexes = {
    "B": "Male et Femelle",
    "M": "Mâle",
    "F": "Femelle"
}

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Déclarations des fonctions de l'application

def renderForms():
    """
    Fonction permettant de récupérer à l'aide d'une requpête SQL toutes 
    les familles ainsi que toutes les années des velages.
    """
    year = []
    fam = []
    db = get_db()
    # Requête SQL : On récupère tous les velages
    cur =  db.execute('SELECT * FROM velages')
    for velage in cur.fetchall():
        ans = int(velage[3][6:])
        if ans not in year:
            year.append(ans)
    year.sort()
    # Requête SQL : On récupère toutes les familles
    cur =  db.execute('SELECT * FROM familles')
    for famille in cur.fetchall():
        fam.append(famille[1])
    fam.sort()
    return year, fam

@bp.route('/gender', methods=('GET', 'POST'))
def gender():
    """
    Fonction permettant de récupérer les données et de faire la requête SQL nous
    permettant d'afficher un graphique sur la diversité des genres. Ceci est notre 
    première fonctionnalité supplémentaire.
    """
    db = get_db()
    # Requête SQL : On récupère tous les animaux de sexe M
    cur =  db.execute('SELECT * FROM animaux WHERE sexe = "M"')
    data = cur.fetchall()
    Male = len(data)
    print(Male)
    # Requête SQL : On récupère tous les animaux de sexe F 
    cur =  db.execute('SELECT * FROM animaux WHERE sexe = "F"')
    data = cur.fetchall()
    Female = len(data)
    print(Female)    

    return render_template('auth/gender.html', data = data, Male = Male, Female = Female)


@bp.route('/complication', methods=('GET', 'POST'))
def complication():
    """
    Fonction permettant de récupérer les données et de faire la requête SQL nous
    permettant d'afficher un graphique des complications. Ceci est notre deuxième
    fonctionnalité supplémentaire.
    """
    list_complication = []
    list_complication_id = []
    nb_complication = []
    db = get_db()
    # Requête SQL : On récupère toutes les données de la table des complications enregistrés
    cur =  db.execute('SELECT * FROM complications')
    data = cur.fetchall()
    for dat in data:
        list_complication.append('"'+dat[1]+'"')
        list_complication_id.append(dat[0])
    print(list_complication)
    print(list_complication_id)
    for element in list_complication_id:
        curr = db.execute('SELECT * FROM velages_complications WHERE complication_id = "{}"'.format(element))
        nb_db = curr.fetchall()
        nb_complication.append(len(nb_db))
    return render_template('auth/complication.html',data = data,nb_complication = nb_complication,list_complication = list_complication)


@bp.route('/velage', methods=('GET', 'POST'))
def velage():
    """
    Fonction permettant de gérer l'accès à la page où est situé l'interface
    qui permet à l'utilisateur de former des graphiques.
    """
    if request.method == 'POST':
        return redirect(url_for("auth.affich_graph",Famille = request.form.get("Famille"), Sexe = request.form.get("Sexe"),Mois = request.form.get("Mois"),Ans = request.form.get("Année")))
    else:
        annee, fam = renderForms()
        return render_template('auth/velage.html', form=render_template('auth/form_velage.html', annee = annee, fam = fam, months=months, sexs=sexes))


@bp.route("/<Famille>/<Sexe>/<Mois>/<Ans>", methods=('GET', 'POST'))
def affich_graph(Famille,Sexe,Mois,Ans):
    """
    Fonction permettant à l'utilisateur d'afficher les graphiques au moyen de
    l'interface disponible sur la page 'Graphiques'.
    """
    if request.method == 'POST':
        return redirect(url_for("auth.affich_graph",Famille = request.form.get("Famille"), Sexe = request.form.get("Sexe"),Mois = request.form.get("Mois"),Ans = request.form.get("Année")))
    else:
        annee, fam = renderForms()
        vel = []
        list_complication = ['"Aide vétérinaire au vêlage"', '"Vêlage difficile"', '"Mère avec post complication"', '"Veau trop petit à la naissance"', '"Veau mal placé"', '"Vêlage plus tôt que prévu"', '"Veau trop gros à la naissance"', '"Veau avec post complication"', '"Veau mal formé"']
        
        if Famille == "Toutes les familles" and Sexe == "Male et femelle" and Ans == "Toutes les années" and Mois == "Tous les mois":
            # Requête SQL :
            cur = db.execute("SELECT velages.id, velages.date, velages_complications.complication_id FROM velages INNER JOIN velages_complications ON velages.id = velages_complications.velage_id")
            for velage in cur.fetchall():
                vel.append(velage[2])
            nb_complication = [vel.count(1),vel.count(2),vel.count(3),vel.count(4),vel.count(5),vel.count(6),vel.count(7),vel.count(8),vel.count(9)]
            print(nb_complication)
            
        elif Famille != "Toutes les familles" and Sexe == "Male et femelle" and Ans == "Toutes les années" and Mois == "Tous les mois":
            # Requête SQL :
            cur = db.execute("SELECT velages.id, velages.date, velages_complications.complication_id FROM velages INNER JOIN velages_complications ON velages.id = velages_complications.velage_id ")
            for velage in cur.fetchall():
                vel.append(velage[2])
            nb_complication = [vel.count(1),vel.count(2),vel.count(3),vel.count(4),vel.count(5),vel.count(6),vel.count(7),vel.count(8),vel.count(9)]
            print(nb_complication)

    return render_template('auth/afiche.html', form=render_template('auth/form_velage.html', annee = annee, fam = fam, months=months, sexs=sexes))
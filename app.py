from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route("/")
def start():
    """ Page d'accueil redirigée vers les actualités """
    return redirect(url_for('actualite'))

@app.route("/actualites")
def actualite():
    """ Afficher les actualités """
    data=read_json("actualites")
    dataCommentaire=read_json("commentaire")
    return render_template("actualites.html", data=data, commentaire=dataCommentaire, name="all")

@app.route("/actualites/<name>")
def specific_actualite(name):
    """ Afficher les actualités par type """
    data=read_json("actualites")
    dataCommentaire=read_json("commentaire")
    return render_template("actualites.html", data=data, commentaire=dataCommentaire, name=name)

@app.route("/concert")
def concert():
    """ Afficher les concerts """
    data=read_json("concert")
    return render_template("concert.html", data=data)

@app.route("/commentaire", methods=["POST"])
def commentaire():
    """ Valider et écrire un commentaire """
    write_json("commentaire", {'actu': request.form['actu'], 'name': request.form['name'], 'commentaire': request.form['commentaire']})
    return redirect(url_for('actualite'))

def read_json(name):
    """ Lire dans un fichier Json """
    f = open(name + '.json')
    data = json.load(f)

    f.close()
    return data

def write_json(name, data):
    """ Ecrire dans un fichier Json existant """
    dataFromFile = read_json(name)
    f = open(name + '.json', "w")

    dataFromFile.append(data)

    f.write(json.dumps(dataFromFile))

    f.close()
    return data

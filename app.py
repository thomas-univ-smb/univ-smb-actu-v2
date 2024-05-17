from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"FMOTDEPASSEz\n\xec]/'

@app.route("/")
def start():
    """ Page d'acceuil du site web """
    return redirect(url_for('actualite'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Permet de se connecter """
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('actualite'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    """ Permet de se déconnecter""" 
    session.pop('username', None)
    return redirect(url_for('actualite'))

@app.route("/actualites")
def actualite():
    """ Afficher les actualités """
    dataActualites=read_json("actualites")
    dataCommentaire=read_json("commentaire")
    return render_template("actualites.html", data=dataActualites, commentaire=dataCommentaire, name="all")

@app.route("/actualites/<name>")
def specific_actualite(name):
    """ Afficher les actualités par type """
    dataActualites=read_json("actualites")
    dataCommentaire=read_json("commentaire")
    return render_template("actualites.html", data=dataActualites, commentaire=dataCommentaire, name=name)

@app.route("/concert")
def concert():
    """ Afficher les concerts """
    dataActualites=read_json("concert")
    return render_template("concert.html", data=dataActualites)

@app.route("/commentaire", methods=["POST"])
def commentaire():
    """ Valider et écrire un commentaire """
    write_json("commentaire", {'actu': request.form['actu'], 'name': request.form['name'], 'commentaire': request.form['commentaire']})
    return redirect(url_for('actualite'))

@app.route("/ajoutactu", methods=['GET', 'POST'])
def ajouteractu():
    """ Permet d'ajouter une actualité """
    if request.method == 'POST':
        print(request.form)
        write_json("actualites", {'id': int(request.form['id']), 'title': request.form['title'], 'dateActu': request.form['dateActu'], 'type' : request.form['type']})
        return redirect(url_for('actualite'))
    data=read_json("actualites")
    max=0
    index=0
    for i in range(0,len(data)):
        if data[i]['id'] > max:
            max=data[i]['id']
            index=data[i]['id']+1
    return '''
    <form method="post">
    <input type="hidden" name="id" value='''+str(index)+'''>
    <p><input disabled value='''+str(index)+''' type=text name=id>
    <p><input requiered placeholder="Titre de l'actualité" type=text name=title>
    <p><input requiered placeholder='Type de musique' type=text name=type>
    <p><label for=dateActu>Date de l'actualité :</label>
    <input requiered placeholder=dateActu type=date name=dateActu>
    <p><input type=submit value=Envoyer>
    </form>
    '''

@app.route("/ajoutconcert", methods=['GET', 'POST'])
def ajouterconcert():
    """ Permet d'ajouter un concert """
 #{"id": 1, "title": "Musilac 2024", "dateConcert" : "03/05/2024"}
    if request.method == 'POST':
        write_json("concert", {'id': int(request.form['id']), 'title': request.form['title'], 'dateConcert': request.form['dateConcert']})
        return redirect(url_for('concert'))
    data=read_json("concert")
    max=0
    index=0
    for i in range(0,len(data)):
        if data[i]['id'] > max:
            max=data[i]['id']
            index=data[i]['id']+1
    return '''
    <form method="post">
    <input type="hidden" name="id" value='''+str(index)+'''>
    <p><input disabled value='''+str(index)+''' type=text name=id>
    <p><input requiered placeholder="Titre du concert" type=text name=title>
    <p><label for=dateConcert>Date du concert :</label>
    <input requiered placeholder=dateConcert type=date name=dateConcert>
    <p><input type=submit value=Envoyer>
    </form>
    '''

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

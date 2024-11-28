from flask import Flask, render_template, request, redirect, url_for, flash
from connect_db import get_session
import random, string
import smtplib
#from email.mime.text import MIMEText
from flask_mail import Mail, Message
import re

app = Flask(__name__)

session = get_session()
session.set_keyspace('ts2_keyspace')

user = {} # [idPersonne, courriel, idChoix, intitule]

# rubrique Accueil
@app.route('/')
def home():
    return render_template('home.html')

# rubrique Activités
@app.route('/rechercheActivites', methods=['GET', 'POST'])
def rechercheActivites():
    msg = None
    if request.method == 'POST':
        if 'search_by_activity_week' in request.form:
            intitule = request.form.get('intitule')
            semaine = request.form.get('semaine')
            if not intitule or not semaine:
                msg = 'Veuillez sélectionner une activité et une semaine.'
                return redirect(url_for('rechercheActivites', message=msg))
            return redirect(url_for('affichage_act_sem', intitule=intitule, semaine=semaine))
        
        elif 'search_by_email' in request.form:
            courriel = request.form.get('courriel')
            if not courriel:
                msg = 'Veuillez entrer un email.', 'error'
                return redirect(url_for('rechercheActivites', message=msg))
            return redirect(url_for('affichage_act_utilisateur', courriel=courriel))
    choix_list = session.execute('SELECT * FROM Choix')
    semaines = [1, 2, 3, 4, 5]
    return render_template('activites.html', choix_list=choix_list, semaines=semaines, message=msg)

@app.route('/affichageActSem')
def affichage_act_sem():
    intitule = request.args.get('intitule')
    semaine = request.args.get('semaine')
    semaine = int(semaine)

    # get idChoix from intitule
    prepared_query_choix = session.prepare('SELECT * FROM Choix WHERE intitule=? ALLOW FILTERING')
    choix = session.execute(prepared_query_choix, [intitule]).one()
    print(f"Choix : {choix}")

    # get reservations for this choix
    prepared_query_reserv = session.prepare('SELECT * FROM Reservations WHERE ref_Choix_uuid=? AND noSemaine=? ALLOW FILTERING')
    reservations = session.execute(prepared_query_reserv, [choix[0], semaine]).all()
    print(f"Reservations : {reservations}")

    # to avoid syntax error below, join both tables here
    # get all utilisateurs
    utilisateurs = session.execute('SELECT * FROM Personnes').all()

    # for reservation in reservations:
    #     print(f"Reservation ref_personne_uuid: {reservation[10]}")
    # for utilisateur in utilisateurs:
    #     print(f"Personne idPersonne: {utilisateur[0]}")


    dict_users = {utilisateur[0]: utilisateur for utilisateur in utilisateurs}
    print(f"Utilisateurs : {dict_users}")
    # dict_users = {}
    # for reservation in reservations:
        # for utilisateur in utilisateurs:
            # if utilisateur[0] == reservation[10]:
                # dict_users[utilisateur[0]] = utilisateur

    # Regroupement des réservations par jour
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']
    grouped_reservations = {jour: [] for jour in jours}

    for reservation in reservations:
        #utilisateurs = session.execute('SELECT * FROM Reservations, Personnes WHERE Reservations.ref_personne_uuid=Personnes.idPersonne').all()    # syntax error
        #for id, user in dict_users:
        user = dict_users.get(reservation[10])
        #id = reservation[10]
        grouped_reservations[reservation[4]].append({
            'courriel': user[1],
            'heure': reservation[5]
        })
    print(f"grouped_reservations :\n {grouped_reservations}")
    return render_template('affichageActSem.html', intitule=intitule, semaine=semaine, grouped_reservations=grouped_reservations)

# Route pour afficher les réservations par utilisateur (email)
@app.route('/affichageActUtilisateur')
def affichage_act_utilisateur():
    courriel = request.args.get('courriel')

    # get id utilisateur pour chercher ses reservations
    prepared_query_utilisateur = session.prepare('SELECT * FROM Personnes WHERE courriel=? ALLOW FILTERING')
    utilisateur = session.execute(prepared_query_utilisateur, [courriel]).one()
    print(f"utilisateur :\n {utilisateur}")

    # get les reservations de l'utilisateur
    idUtilisateur = utilisateur[0]
    print(f"idUtilisateur :\n {idUtilisateur}")
    prepared_query_reserv = session.prepare('SELECT * FROM Reservations WHERE ref_personne_uuid=? ALLOW FILTERING')
    reservations = session.execute(prepared_query_reserv, [idUtilisateur]).all()
    print(f"reservations :\n {reservations}")

    # get all choix
    choices = session.execute('SELECT * FROM Choix').all()

    dict_choices = {choix[0]: choix for choix in choices}
    print(f"choices : {dict_choices}")

    # Regrouper les réservations par activité
    grouped_reservations = []
    for reservation in reservations:
        choix = dict_choices.get(reservation[9])
        #choix = session.execute('SELECT * FROM Reservations, Choix WHERE Reservations.ref_Choix_uuid=Choix.idChoix').one() # syntax error
        grouped_reservations.append({
            'activite': choix[4],
            'semaine': reservation[6],
            'jour': reservation[4],
            'heure': reservation[5]
        })
    print(f"grouped_reservations :\n {grouped_reservations}")
    return render_template('affichageActUtilisateur.html', courriel=courriel, grouped_reservations=grouped_reservations)


# rubrique Réservation
@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    msg = None
    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']
        if not email or not mdp:
            msg = "Un champs ou plusieurs ne sont pas remplis."
            return render_template('connexion.html', message = msg)
        prepared_query = session.prepare("SELECT * FROM Personnes WHERE courriel=?")
        userInfo = session.execute(prepared_query, [email]).one()
        #print(f"userInfo:\n- idPersonne : {userInfo[0]}\n- 1 : {userInfo[1]}\n- 2 : {userInfo[2]}\n- 3 : {userInfo[3]}\n- 4 : {userInfo[4]}\n- 5 : {userInfo[5]}")
        if userInfo is None:
            msg = "Aucun utilisateur n'est associé à cette adresse courriel."
            return render_template('connexion.html', message = msg)
        
        if mdp == userInfo[2]:
            user['idPersonne'] = userInfo[0]
            user['courriel'] = userInfo[1]
            return redirect(url_for('choix_activite'))
        else:
            msg = "Mauvais mot de passe."
            return render_template('connexion.html', message = msg)
    return render_template('connexion.html', message=msg)

@app.route('/choix_activite', methods=['GET', 'POST'])
def choix_activite():
    msg = None
    #prepared_query = session.prepare("SELECT * FROM Choix WHERE ref_Tsxxx=105")
    activities = session.execute("SELECT * FROM Choix WHERE ref_Tsxxx=105")
    # if request.method == 'POST':
    #     idChoix = request.form['idChoix']
    #     user['idChoix'] = idChoix
    #     return redirect(url_for('reserver'))
    return render_template('choixActivite.html', activities=activities, message=msg)

@app.route("/choisir", methods=['GET', 'POST'])
def choisir():
    msg = None
    if request.method == 'POST':
        intitule = request.form.get('intitule')
        if not intitule:
            msg = "Aucune activité n'a été sélectionnée."
            activities = session.execute("SELECT * FROM Choix WHERE ref_Tsxxx=105")
            return render_template('choixActivite.html', activities=activities, message=msg)
        if intitule:
            prepared_query = session.prepare("SELECT * FROM Choix WHERE intitule=? ALLOW FILTERING")
            rslt = session.execute(prepared_query, [intitule]).one()
            if rslt:
                user['idChoix'] = rslt[0]
                user['intitule'] = rslt[4]
                return render_template('reservation.html')
        
@app.route("/reserver", methods=['GET', 'POST'])
def reservation():
    #print(f"user:\n- 0 : {user[0]}\n- 1 : {user[1]}\n- 2 : {user[2]}\n- 3 : {user[3]}")
    if request.method == 'POST':
        semaine = request.form['semaine']
        jour = request.form['jour']
        heure = request.form['heure']
        semaine = int(semaine)
        heure = int(heure)
        prepared_query = session.prepare("INSERT INTO Reservations (idReservation, ref_personne_uuid, ref_Choix_uuid, Quantite, noSemaine, extraReservation2, noperiode) VALUES (uuid(), ?, ?, 1, ?, ?, ?)")
        session.execute(prepared_query, [user['idPersonne'], user['idChoix'], semaine, jour, heure])
        return render_template('confirmationReservation.html', courriel=user['courriel'], activite=user['intitule'], semaine=semaine, jour=jour, heure=heure)# courriel=user['courriel'], activite=semaine=semaine, jour=jour, heure=heure
    return render_template("reservation.html")


# rubrique Devenir membre
@app.route('/nouvel_usager', methods=['GET', 'POST'])
def nouvel_usager():
    message = None
    email = "nouveau@email.ca"
    mdp = None

    if request.method == 'POST':
        email = request.form.get('email', email)
        mdp = request.form.get('mdp', None)
        if not mdp:
            mdp = random_password(8)
        if mdp and len(mdp) >= 8:
            message = "Le mot de passe ne doit pas contenir plus que 8 caractères."

        prenom = request.form.get('prenom')
        nom = request.form.get('nom')
        #print("/nouvel_usager\nemail: ", email, " / mdp: ", mdp, " / prenom: ", prenom, " / nom:", nom)

        if not email or not prenom or not nom:
            message = "Tous les champs marqués par un * sont obligatoires."
        else:
            # Nous procéderons ensuite à l'enregistrement (voir ci-dessous)
            return redirect(url_for('valide_usager', email=email, mdp=mdp, prenom=prenom, nom=nom))

    return render_template('nouvelUsager.html', email=email, mdp=mdp, message=message)

@app.route('/valide_usager', methods=['GET', 'POST'])
def valide_usager():
    email = request.args.get('email')
    mdp = request.args.get('mdp')
    prenom = request.args.get('prenom')
    nom = request.args.get('nom')
    #print("/valide_usager\nemail: ", email, " / mdp: ", mdp, " / prenom: ", prenom, " / nom:", nom)
    if not email or not mdp or not prenom or not nom:
        return render_template('nouvelUsager.html', email=email, prenom=prenom, nom=nom, mdp=mdp, message="Un champ ou plusieurs sont vides.")

    if not valide_email(email):
        return render_template('nouvelUsager.html', email=email, prenom=prenom, nom=nom, mdp=mdp, message="Adresse courriel invalide!")

    if exist_usager(email, session):
        return render_template('nouvelUsager.html', email=email, prenom=prenom, nom=nom, mdp=mdp, message="Il existe déjà un compte associé à cette adresse courriel!")

    # Enregistrer l'usager dans la base de données (ici, vous pouvez ajouter une requête Cassandra)
    enregistrer_usager(prenom, nom, email, mdp, session)

    # Envoi de l'email de confirmation
    # envoi_email(email, mdp)
    
    return render_template('confirmationCompte.html', prenom=prenom, nom=nom, email=email, mdp=mdp)

def valide_email(email):
    email_regex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def exist_usager(email, session):
    prepared_query = session.prepare("SELECT * FROM Personnes WHERE courriel = ?")
    #print(f"def exist_usager\nEmail: {email}, Type: {type(email)}")
    result = session.execute(prepared_query, [email])
    return len(result.current_rows) > 0

def enregistrer_usager(prenom, nom, email, mdp, session):
    prepared_query = session.prepare("INSERT INTO Personnes (IdPersonne, prenom, nom, courriel, tsxxx, mdp) VALUES (uuid(), ?, ?, ?, 105, ?)")
    session.execute(prepared_query, [prenom, nom, email, mdp])

# def envoi_email(email, mdp):
#     try:
#         print("def envoi_email...")
#         fromaddr = 'admin.no-reply@serre-toi.ca'
#         toaddr = email
#         msg = '''
#             From: {fromaddr}
#             To: {toaddr}
#             Subject: Serre-toi - Création de compte
#             Votre compte sur Serre-toi a été créé avec succès. Votre mot de passe est : {mdp}"
#         '''
#         host = "server.smtp.com"
#         server = smtplib.SMTP(host)
#         FROM = fromaddr
#         TO = email
#         MSG = msg
#         server.sendmail(FROM, TO, MSG)
#         server.quit()
#         return "Email sent successfully"
#     except Exception as e:
#         return f"Failed to send email: {e}"
        
def random_password(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# rubrique Modalités d'adhésion
@app.route("/modalites")
def modalites():
    return render_template("modalites.html")

# rubrique Blogue
@app.route("/blogue")
def blogue():
    return render_template("blogue.html")

if __name__ == '__main__':
    app.run(debug=True)

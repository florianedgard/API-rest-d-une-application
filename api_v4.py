from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)

#db = Database("192.168.1.xxx", "extern_user", "Bt5@c13l972", "ciel2027")
db = Database("127.0.0.1", "root", "", "ciel2027")
    
@app.route('/v4/etudiants/', methods=['GET'])
def getEtudiants():
    code = db.login(request)
    if code == 500:
        return jsonify({'message': 'Echec de connexion à la base de données'}), 500
    if code == 401:
        return jsonify({'message': 'Accès non autorisé'}), 401
        
    etudiants = []
    data = db.readAll()
    if data == 401:
        return jsonify("Requête invalide"), 400
    if data == 400:
        return jsonify("Requête invalide"), 400
    for row in data:
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
            }
        etudiants.append(etudiant)
    return jsonify(etudiants), 200

@app.route('/v4/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    code = db.login(request)
    if code == 500:
        return jsonify({'message': 'Echec de connexion à la base de données'}), 500
    if code == 401:
        return jsonify({'message': 'Accès non autorisé'}), 401
    
    data = db.readOne(id)
    if data == 400:
        return jsonify("Requête invalide"), 400
    if data != 404:
        etudiant = {
            "idetudiant": data[0],
            "nom": data[1],
            "prenom": data[2],
            "email": data[3],
            "telephone": data[4]
        }
        return jsonify(etudiant), 200
    else: 
        return jsonify("id invalide"), 404

@app.route('/v3/etudiants/', methods=['POST'])
def addEtudiant():
    code = db.login(request)
    if code == 500:
        return jsonify({'message': 'Echec de connexion à la base de données'}), 500
    if code == 401:
        return jsonify({'message': 'Accès non autorisé'}), 401
    
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    telephone = data.get('telephone')
    
    result = db.create(nom, prenom, email, telephone)
    
    if result == 201:
        return jsonify("Etudiant ajouté avec succès"), 201
    else:
        return jsonify("Erreur lors de l'ajout de l'étudiant"), 400

@app.route('/v3/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    code = db.login(request)
    if code == 500:
        return jsonify({'message': 'Echec de connexion à la base de données'}), 500
    if code == 401:
        return jsonify({'message': 'Accès non autorisé'}), 401
    
    result = db.delete(id)
    
    if result == 200:
        return jsonify("Etudiant supprimé avec succès"), 200
    else:
        return jsonify("Erreur lors de la suppression de l'étudiant"), 400

@app.route('/v3/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    code = db.login(request)
    if code == 500:
        return jsonify({'message': 'Echec de connexion à la base de données'}), 500
    if code == 401:
        return jsonify({'message': 'Accès non autorisé'}), 401
    
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    telephone = data.get('telephone')
    
    result = db.update(id, nom, prenom, email, telephone)
    
    if result == 200:
        return jsonify("Etudiant mis à jour avec succès"), 200
    else:
        return jsonify("Erreur lors de la mise à jour de l'étudiant"), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug=True)

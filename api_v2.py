from flask import Flask, jsonify, request
from db import Database
import mysql.connector             
app = Flask(__name__)

mydb= mysql.connector.connect(
    host= "127.0.0.1",
    user= "extern_user1",
    password= " bt5@c13l972",
    database= "ciel2027",
    port = 3306
)
cursor = mydb.cursor()

# Récupérer tous les étudiants
@app.route('/api/etudiants/', methods=['GET'])
def getEtudiants():
    try :

        etudiants = []

        request = "SELECT * FROM etudiant"
        cursor.execute(request)
        result = cursor.fetchall()

        for row in result:
            etudiant = {
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4]
            }

            etudiants.append(etudiant)
        return jsonify(etudiants), 201
    
    except:
        return jsonify({"error": "Aucun étudiant trouvé"}), 404


# Récupérer un étudiant grâce à son ID
@app.route('/api/etudiants/<id>', methods=['GET'])
def getEtudiant(id):
    req = "SELECT * FROM etudiant WHERE idetudiant = " + id
    print(req)
    try :

        cursor.execute(req)
        row = cursor.fetchone()
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        return jsonify(etudiant), 200
    except:
        return jsonify({"error": "Étudiant non trouvé"}), 404

# Ajouter un étudiant
@app.route('/api/etudiants/', methods=['POST'])
def addEtudiant():
    try:

        nom = request.json['nom']
        prenom = request.json['prenom']
        email = request.json['email']
        telephone = request.json['telephone']
        req = f"INSERT INTO etudiant (nom, prenom, email, telephone) \
            VALUES ('{nom}', '{prenom}', '{email}', '{telephone}')"
        cursor.execute(req)
        mydb.commit()
        return jsonify({"message": "Ajout OK"}), 201
    except:
        return jsonify({"error": "Erreur lors de l'ajout"}), 400

# Mettre à jour un étudiant
@app.route('/api/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    try:

        nom = request.json['nom']
        prenom = request.json['prenom']
        email = request.json['email']
        telephone = request.json['telephone']
        req = f"UPDATE etudiant \
            SET nom='{nom}', prenom='{prenom}', email='{email}', telephone='{telephone}' \
               WHERE idetudiant={id}"
        cursor.execute(req)
        mydb.commit()
        return jsonify({"message": "Mise à jour OK"}), 200
    except:
        return jsonify({"error": "Erreur lors de la mise à jour"}), 400

# Supprimer un étudiant
@app.route('/api/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id): 
    try:
        req = f"DELETE FROM etudiant WHERE idetudiant={id}"
        cursor.execute(req)
        mydb.commit()
        return jsonify({"message": "Suppression OK"}), 200
    except:
        return jsonify({"error": "Erreur lors de la suppression"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


import os

# Configuration de la base de données
DB_HOST = "production-db.sofiatech.internal"
DB_USER = "admin"
# Mauvaise pratique : un mot de passe en clair dans le code
DB_PASSWORD = "SuperSecretPassword123!" 

# Mauvaise pratique CRITIQUE : Clés d'accès AWS codées en dur
# (Ce sont de fausses clés, mais elles ont le format exact qu'AWS utilise, Gitleaks va les repérer tout de suite !)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def get_db_connection():
    print(f"Connecting to {DB_HOST} with user {DB_USER}...")
    # Logique de connexion...

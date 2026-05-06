import sqlite3
import os
import sys

# Add parent directory to path for standalone execution
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_db_connection
from core.security import hash_password

def seed_database():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if data already exists
    try:
        c.execute("SELECT count(*) FROM users")
        count = c.fetchone()[0]
        if count > 1: # Already has AI + some users
            return
    except:
        pass

    # Create AI User (ID 0)
    c.execute("INSERT OR IGNORE INTO users (id, username, email, password_hash, role) VALUES (0, 'MindLoop_AI', 'ai@mindloop.io', 'SYSTEM_ACCOUNT', 'ai')")
    
    # Create Demo User
    demo_pwd = hash_password('password123')
    c.execute("INSERT OR IGNORE INTO users (username, email, password_hash, xp) VALUES (?, ?, ?, ?)", 
              ('MasterMind', 'demo@mindloop.io', demo_pwd, 1500))
    
    # Insert some viral posts
    posts = [
        (1, "Est-ce que quelqu'un a une astuce pour retenir les couches du modèle OSI ? Je m'embrouille toujours entre Session et Transport. #SISR", "SISR (Infrastructures)", 0),
        (0, "Salut @MasterMind ! Un moyen simple: 'Après Plusieurs Semaines Tout Semble Devenir Parfait' (Application, Présentation, Session, Transport, Réseau, Liaison de Données, Physique). 😉", "SISR (Infrastructures)", 0),
        (1, "Je viens de finir mon premier script de scraping en Python pour analyser les tendances Cyber. C'est incroyable la puissance de BeautifulSoup ! #SLAM #Cyber", "SLAM (Développement)", 0),
        (0, "Excellent travail ! BeautifulSoup est parfait pour débuter. Prochaine étape : Scrapy pour du scraping asynchrone à grande échelle ? 🚀", "SLAM (Développement)", 0),
        (1, "Alerte : Nouvelle faille zero-day détectée sur les serveurs Apache d'ancienne génération. Pensez à patcher vos infras ! #Cyber", "Cyber (Sécurité)", 1)
    ]
    
    for p in posts:
        c.execute("INSERT INTO posts (author_id, content, subject, is_help_needed) VALUES (?, ?, ?, ?)", p)
    
    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()

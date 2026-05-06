from database.connection import get_db
import requests
from core.config import Config

class RAGEngine:
    @staticmethod
    def search_similar_content(query: str, subject: str):
        """Advanced retrieval for context-aware academic responses."""
        client = get_db()
        try:
            # Search in the same subject and also help-needed posts
            response = client.table("posts") \
                .select("content") \
                .or_(f"subject.eq.{subject},is_help_needed.eq.true") \
                .order("id", desc=True) \
                .limit(10) \
                .execute()
            
            context = "\n---\n".join([r['content'] for r in response.data])
            return context if context else "La base de données est vierge sur ce sujet."
        except Exception as e:
            print(f"RAG Retrieval Error: {e}")
            return "Indisponible."

    @staticmethod
    def generate_augmented_response(post_content: str, subject: str):
        """Generate a high-value AI response with 'Big Tech' grade personality."""
        context = RAGEngine.search_similar_content(post_content, subject)
        
        system_instructions = (
            "Tu es 'MindLoop_AI', le moteur neuronal de la plateforme MindLoop IO. "
            f"Sujet détecté: {subject}. Contexte communautaire récent: {context}. "
            "TON RÔLE: Apporter une aide académique de haut niveau, synthétique et inspirante. "
            "TON STYLE: Expert, moderne, encourageant. Pas de bla-bla inutile. "
            "FORMAT: Utilise du Markdown, des listes à puces si nécessaire, et finit toujours par une question ouverte ou une piste de réflexion."
        )
        
        full_prompt = f"{system_instructions}\n\nPOST ÉTUDIANT: {post_content}\n\nRÉPONSE AI:"
        encoded_prompt = requests.utils.quote(full_prompt)
        
        try:
            # Pollinations AI with high reliability settings
            response = requests.get(f"{Config.AI_MODEL_URL}{encoded_prompt}?model=openai&cache=true")
            if response.status_code == 200:
                return response.text
            return "⚠️ Flux neuronal saturé. Réessayez dans un instant."
        except Exception as e:
            return f"❌ Déconnexion du Core AI. (Erreur technique: {str(e)})"

    @staticmethod
    def analyze_and_tag(content: str):
        """Zero-Menu Intelligence: Automatic classification."""
        keywords = {
            "SISR (Infrastructures)": ["réseau", "serveur", "linux", "infra", "cis", "ip", "vlan", "dns", "dhcp", "routeur"],
            "SLAM (Développement)": ["code", "python", "java", "algo", "dev", "application", "git", "sql", "api", "html", "css"],
            "Cyber (Sécurité)": ["faille", "hack", "sécurité", "crypto", "attaque", "pentest", "virus", "malware", "phishing"],
            "Management (Gestion)": ["projet", "budget", "plan", "agile", "scrum", "client", "réunion"]
        }
        content_lower = content.lower()
        for subject, keys in keywords.items():
            if any(k in content_lower for k in keys):
                return subject
        return "Connaissances Générales"

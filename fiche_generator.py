import pdfplumber
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY") or st.secrets.get("CEREBRAS_API_KEY", "")


def extraire_texte_pdf(pdf_file) -> str:
    texte = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            contenu = page.extract_text()
            if contenu:
                texte += contenu + "\n"
    return texte.strip()


def appeler_ia(messages: list, max_tokens: int = 3000) -> str:
    # Essai avec Groq en priorité
    if GROQ_API_KEY:
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": 0.3
                }
            )
            data = response.json()
            if "choices" in data:
                return data["choices"][0]["message"]["content"]
        except Exception:
            pass

    # Fallback Cerebras
    response = requests.post(
        "https://api.cerebras.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {CEREBRAS_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-oss-120b",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.3
        }
    )
    data = response.json()
    return data["choices"][0]["message"]["content"]


def generer_fiche(texte: str, niveau: str = "Prépa ingénieur 1ère année") -> str:
    if "1ère" in niveau:
        instructions_niveau = "Niveau 1ère année : notions fondamentales, méthodes de base, définitions précises. Pas de concepts avancés."
    else:
        instructions_niveau = "Niveau 2ème année : approfondissement, liens entre concepts, démonstrations clés, subtilités de concours."

    messages = [
        {
            "role": "system",
            "content": """Tu es un professeur agrégé de classes préparatoires scientifiques.
Tu crées des fiches de révision denses, précises et opérationnelles.
RÈGLES : zéro remplissage, formules exactes, jamais de LaTeX ($), utilise Unicode : α β γ π ∑ ∫ ≤ ≥ ≠ √ ∞"""
        },
        {
            "role": "user",
            "content": f"""Niveau : {niveau}
{instructions_niveau}

Génère une fiche de révision complète avec cette structure :

# [TITRE DU COURS]
> Résumé en 20 mots max.

## L'essentiel à retenir
- **Notion 1** : explication
- **Notion 2** : explication
- **Notion 3** : explication
- **Notion 4** : explication
- **Notion 5** : explication

## Définitions clés
| Terme | Définition |
|-------|------------|
| Terme 1 | définition |

## Formules & Théorèmes
| Nom | Formule | Conditions |
|-----|---------|------------|
| Nom | formule | quand l'appliquer |

## Méthode de raisonnement
1. **Étape 1** → description
2. **Étape 2** → description
3. **Vérification** → ce qu'il faut contrôler

## Pièges & Erreurs fréquentes
- Erreur : description -> Correct : ce qu'il faut faire
- Confusion : deux notions -> Distinction : la différence

## Questions de révision
### Faciles
1. [Question]
2. [Question]
3. [Question]

### Intermédiaires
4. [Question]
5. [Question]
6. [Question]

### Difficiles
7. [Question]
8. [Question]
9. [Question]
10. [Question]

**Réponses :**
1. [Réponse complète]
2. [Réponse complète]
3. [Réponse complète]
4. [Réponse complète]
5. [Réponse complète]
6. [Réponse complète]
7. [Réponse complète]
8. [Réponse complète]
9. [Réponse complète]
10. [Réponse complète]

## Liens avec d'autres notions
- **Prérequis** : liste
- **Suite logique** : liste

Cours :
\"\"\"{texte[:8000]}\"\"\"
"""
        }
    ]
    return appeler_ia(messages, max_tokens=3000)


def generer_quizz(texte: str, niveau: str = "Prépa ingénieur 1ère année") -> str:
    if "1ère" in niveau:
        instructions_niveau = "Niveau 1ère année : questions sur les fondamentaux."
    else:
        instructions_niveau = "Niveau 2ème année : questions approfondies, niveau concours."

    messages = [
        {
            "role": "system",
            "content": """Tu es un professeur de prépa qui crée des quizz rigoureux.
RÈGLES : une seule bonne réponse par QCM, mauvaises réponses plausibles, jamais de LaTeX."""
        },
        {
            "role": "user",
            "content": f"""Niveau : {niveau}
{instructions_niveau}

Génère un quizz de 15 questions QCM. Structure :

**Question 1** : [énoncé]
- A) [proposition]
- B) [proposition]
- C) [proposition]
- D) [proposition]

[...15 questions...]

## Réponses & Explications
**Q1** : Bonne réponse : [lettre] — [explication 2 lignes max]
[...15 réponses...]

Cours :
\"\"\"{texte[:8000]}\"\"\"
"""
        }
    ]
    return appeler_ia(messages, max_tokens=3000)


def generer_correction(texte: str, niveau: str = "Prépa ingénieur 1ère année") -> str:
    if "1ère" in niveau:
        instructions_niveau = "Niveau 1ère année : explique chaque étape, justifie les méthodes."
    else:
        instructions_niveau = "Niveau 2ème année : correction niveau concours, arguments attendus par le jury."

    messages = [
        {
            "role": "system",
            "content": """Tu es un professeur agrégé de prépa qui corrige des devoirs surveillés.
RÈGLES ABSOLUES :
- Corrige chaque question dans l'ordre, sans en sauter aucune
- Pour chaque question : raisonnement détaillé, résultat final, erreur classique
- NE PAS générer de tableau de points, de barème, ou de grille de notation
- NE PAS résumer ou sauter des questions sous prétexte qu'elles sont similaires
- Jamais de LaTeX ($), utilise Unicode pour les symboles mathématiques"""
        },
        {
            "role": "user",
            "content": f"""Niveau : {niveau}
{instructions_niveau}

Corrige ce sujet intégralement, question par question, sans en omettre aucune.
N'inclus PAS de tableau de points ou de barème.

# Correction du DS

## Exercice 1 — [titre de l'exercice]

### Question 1.1
**Raisonnement :** [étapes détaillées du raisonnement]
**Résultat :** [réponse finale claire]
**Erreur classique :** [erreur que font souvent les élèves]

### Question 1.2
**Raisonnement :** [étapes détaillées]
**Résultat :** [réponse finale]
**Erreur classique :** [erreur fréquente]

[Continue TOUTES les questions jusqu'à la fin du sujet]

## Bilan
- **Notions évaluées** : liste des notions
- **Méthodes à retenir** : liste des méthodes

Sujet complet :
\"\"\"{texte[:10000]}\"\"\"
"""
        }
    ]
    return appeler_ia(messages, max_tokens=6000)
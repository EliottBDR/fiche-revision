import streamlit as st
from fiche_generator import extraire_texte_pdf, generer_fiche, generer_quizz, generer_correction

st.set_page_config(
    page_title="Fiche IA",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Assistant révision IA")
st.markdown("Upload ton cours ou sujet PDF → résultat structuré en quelques secondes. **100% gratuit.**")
st.divider()

col1, col2 = st.columns(2)

with col1:
    mode = st.selectbox(
        "Type de document",
        ["Fiche de révision", "Quizz", "Correction DS"]
    )

with col2:
    niveau = st.selectbox(
        "Niveau",
        ["Prépa ingénieur 1ère année", "Prépa ingénieur 2ème année"]
    )

descriptions = {
    "Fiche de révision": "📖 Génère une fiche dense avec définitions, formules, méthodes et questions.",
    "Quizz": "❓ Génère 15 questions QCM avec réponses et explications.",
    "Correction DS": "✏️ Corrige ton sujet question par question avec le détail du raisonnement."
}
st.info(descriptions[mode])

labels = {
    "Fiche de révision": "📄 Upload ton cours (PDF uniquement)",
    "Quizz": "📄 Upload ton cours (PDF uniquement)",
    "Correction DS": "📄 Upload ton sujet de DS (PDF uniquement)"
}

uploaded_file = st.file_uploader(labels[mode], type=["pdf"])

if uploaded_file is not None:
    st.success(f"✅ Fichier reçu : **{uploaded_file.name}**")

    boutons = {
        "Fiche de révision": "🚀 Générer la fiche",
        "Quizz": "🚀 Générer le quizz",
        "Correction DS": "🚀 Générer la correction"
    }

    if st.button(boutons[mode], type="primary"):

        with st.spinner("⏳ Génération en cours... (20-40 secondes)"):
            texte = extraire_texte_pdf(uploaded_file)

            if not texte or len(texte) < 50:
                st.error("❌ Impossible d'extraire le texte. "
                         "Essaie un PDF avec du texte sélectionnable (pas scanné).")
            else:
                if mode == "Fiche de révision":
                    resultat = generer_fiche(texte, niveau)
                elif mode == "Quizz":
                    resultat = generer_quizz(texte, niveau)
                else:
                    resultat = generer_correction(texte, niveau)

                st.divider()

                # --- Affichage avec réponses cachées ---
                if mode in ["Fiche de révision", "Quizz"]:
                    if "**Réponses" in resultat or "## ✅ Réponses" in resultat:
                        separateur = "**Réponses" if "**Réponses" in resultat else "## ✅ Réponses"
                        parties = resultat.split(separateur, 1)
                        contenu_principal = parties[0]
                        reponses = separateur + parties[1] if len(parties) > 1 else ""
                        st.markdown(contenu_principal)
                        with st.expander("👁️ Voir les réponses (clique pour révéler)"):
                            st.markdown(reponses)
                    else:
                        st.markdown(resultat)
                else:
                    st.markdown(resultat)

                # --- Téléchargement HTML ---
                st.divider()
                import markdown as md

                html_contenu = md.markdown(
                    resultat,
                    extensions=["tables", "fenced_code", "nl2br"]
                )

                html_complet = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Arial, sans-serif; font-size: 13px; line-height: 1.7; max-width: 800px; margin: 40px auto; color: #1a1a1a; }}
  h1 {{ font-size: 22px; color: #0f3460; border-bottom: 2px solid #0f3460; padding-bottom: 5px; }}
  h2 {{ font-size: 17px; color: #16213e; border-left: 4px solid #0f3460; padding: 6px 10px; background-color: #f0f4ff; margin-top: 20px; }}
  h3 {{ font-size: 14px; color: #0f3460; margin-top: 14px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 12px; }}
  th {{ background-color: #0f3460; color: white; padding: 6px 10px; text-align: left; }}
  td {{ border: 1px solid #ccc; padding: 5px 10px; }}
  tr:nth-child(even) td {{ background-color: #f5f5f5; }}
  code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: monospace; }}
  pre {{ background-color: #f4f4f4; padding: 12px; border-radius: 5px; border-left: 4px solid #0f3460; white-space: pre-wrap; }}
  blockquote {{ border-left: 4px solid #0f3460; margin: 10px 0; padding: 5px 15px; background-color: #f0f4ff; }}
  ul, ol {{ padding-left: 20px; }}
  li {{ margin: 4px 0; }}
  strong {{ color: #0f3460; }}
</style>
</head>
<body>
{html_contenu}
</body>
</html>"""

                st.download_button(
                    label="⬇️ Télécharger (.html)",
                    data=html_complet.encode("utf-8"),
                    file_name=f"fiche_{uploaded_file.name.replace('.pdf', '')}.html",
                    mime="text/html"
                )
                st.caption("💡 Pour convertir en PDF : ouvre le fichier dans ton navigateur → Ctrl+P → Enregistrer en PDF")

st.divider()
st.caption("v0.7 · Fait avec Groq + Cerebras · Développé par [EliottBDR](https://github.com/EliottBDR)")
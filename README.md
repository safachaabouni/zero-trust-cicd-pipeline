# 🔒 Zero-Trust Secret Scanning Pipeline

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Gitleaks](https://img.shields.io/badge/Gitleaks-Secret_Scanner-8A2BE2?style=for-the-badge)
![DevSecOps](https://img.shields.io/badge/DevSecOps-Zero_Trust-red?style=for-the-badge)

## 📌 Présentation du Projet
Ce projet implémente une architecture de sécurité **Zero-Trust** au sein d'une chaîne d'intégration continue (CI). L'objectif est d'empêcher toute fuite de données sensibles (clés d'API, mots de passe, tokens) dans le code source, en bloquant systématiquement les déploiements compromis.

Contrairement aux solutions basiques qui ne scannent que le dernier commit, cette implémentation effectue un **audit cryptographique complet** de l'historique Git et utilise des règles personnalisées pour s'adapter au contexte de l'entreprise.

## 🏗️ Architecture et Décisions Techniques

### 1. Moteur d'Analyse : Gitleaks via Docker Natif
Pour contourner les limitations des plugins d'intégration continue (souvent restreints au mode *Protect*), Gitleaks est exécuté directement via son conteneur **Docker officiel**. Cela permet d'invoquer le mode `detect` et d'avoir un contrôle total sur les arguments d'audit.

### 2. Audit d'Historique Profond (Deep Fetch)
Le pipeline est configuré avec `fetch-depth: 0`. Le scanner ne regarde pas uniquement le *diff* du jour, il remonte l'intégralité de l'arbre des commits pour traquer les secrets oubliés dans le passé (Hard-fail automatique en cas de détection).

### 3. Règles de Détection Hybrides (Custom Regex)
Le scanner n'est pas limité à son dictionnaire par défaut. Un fichier `gitleaks.toml` sur-mesure a été développé pour :
* **Maintenir la base de connaissances mondiale** (`useDefault = true`) pour détecter les formats connus (AWS, Stripe, Slack, GitHub...).
* **Traquer les fuites internes** via des expressions régulières (Regex) spécifiques, capables de repérer des mots de passe génériques (ex: `DB_PASSWORD = "..."`) malgré une faible entropie.

## ⚙️ Workflow du Pipeline (CI)
Le processus se déclenche à chaque `push` ou `pull_request` sur la branche `main` :

1. **Checkout du Code :** Téléchargement du dépôt avec rapatriement complet de l'historique Git.
2. **Mounting Docker :** Le répertoire de travail de GitHub Actions est monté en tant que volume à l'intérieur du conteneur Gitleaks.
3. **Analyse Hybride :** Gitleaks charge le fichier `gitleaks.toml`, compile les Regex par défaut et personnalisées, puis scanne chaque ligne de chaque commit.
4. **Sanction (Gatekeeper) :** Si un secret est trouvé, le processus se termine en `Exit Code 1`, cassant immédiatement le build et générant un rapport détaillé (Fichier, Ligne, Commit Hash, Règle enfreinte).

## 🚀 Pistes d'Améliorations
* Implémentation de Gitleaks en *Pre-commit hook* côté développeur pour bloquer le secret avant même qu'il ne quitte le poste de travail.
* Intégration d'un agent IA pour masquer ou "tourner" (rotate) automatiquement les clés compromises détectées dans les logs.

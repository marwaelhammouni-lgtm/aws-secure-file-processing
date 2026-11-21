# AWS Secure File Processing

Projet de traitement sécurisé de fichiers avec **Amazon S3, AWS Lambda, Python et GitHub Actions**.

## 1. Présentation du projet

Ce projet permet de traiter automatiquement les fichiers déposés dans un bucket Amazon S3 grâce à une fonction AWS Lambda.

La fonction vérifie le fichier avant de le lire :
- Le bucket doit être celui autorisé.
- Le nom du fichier doit être valide.
- Seuls les fichiers `.txt` sont acceptés.
- La taille doit être supérieure à 0 et inférieure ou égale à 1 Mio.
- Le contenu est lu en UTF-8, dans une limite de 4 096 octets.

## 2. Architecture AWS

Les principaux services utilisés sont :

- **Amazon S3** : stockage privé des fichiers.
- **AWS Lambda** : traitement des fichiers à leur création.
- **AWS IAM** : gestion des permissions de la fonction.
- **Amazon CloudWatch** : consultation des journaux d'exécution.

Région AWS : `eu-north-1` (Europe – Stockholm).

## 3. Structure du dépôt

```text
aws-secure-file-processing/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── src/
│   ├── __init__.py
│   └── lambda_function.py
├── tests/
│   └── test_lambda.py
├── requirements-dev.txt
├── .gitignore
├── LICENSE
└── README.md

```

## 4. Installation et tests locaux

Prérequis :
- Python 3.12
- Git
- pip

Installer les dépendances de développement :

```bash
python -m pip install -r requirements-dev.txt
```

Exécuter les tests :

```bash
python -m pytest -v
```

Les tests couvrent notamment :
- L'acceptation d'un fichier `.txt`.
- Le rejet d'un fichier PDF.
- Le rejet d'un fichier dépassant 1 Mio.

## 5. Intégration continue avec GitHub Actions

Le workflow est défini dans :

`.github/workflows/ci-cd.yml`

Il se déclenche automatiquement :
- Lors d'un `push` sur la branche `main`.
- Lors d'une Pull Request vers `main`.

Les étapes automatisées sont :
1. Récupération du code source.
2. Configuration de Python 3.12.
3. Installation des dépendances.
4. Exécution des tests avec `pytest`.

Le résultat des exécutions est consultable dans l'onglet **Actions** du dépôt GitHub.

**État actuel :** l'intégration continue (CI) est configurée. Le déploiement automatique (CD) n'est pas activé.

## 6. Préparer le paquet de déploiement Lambda

Le code source de la fonction se trouve dans :

`src/lambda_function.py`

Pour préparer un paquet ZIP :

1. Copier `lambda_function.py` dans un dossier de préparation.
2. Compresser ce fichier en ZIP.
3. Vérifier que `lambda_function.py` se trouve directement à la racine de l'archive.

Structure attendue :

```text
lambda-deployment.zip
└── lambda_function.py
```

Le fichier ZIP préparé localement n'est pas automatiquement envoyé vers AWS.

## 7. Procédure de déploiement manuel futur

Cette procédure est destinée à une personne disposant des autorisations AWS nécessaires. Elle n'a pas encore été exécutée dans le cadre de ce projet.

Pour mettre à jour le code de la fonction :

1. Se connecter à la console AWS avec une identité autorisée.
2. Sélectionner la région `eu-north-1`.
3. Ouvrir AWS Lambda.
4. Sélectionner la fonction `ProjetAWS-S3-FileProcessor`.
5. Dans la section du code source, choisir l'option de téléversement d'un fichier `.zip`.
6. Sélectionner `lambda-deployment.zip`.
7. Enregistrer les modifications.
8. Vérifier la configuration du gestionnaire :

```text
lambda_function.lambda_handler
```

Le runtime utilisé par le projet est Python 3.12.

Après un déploiement autorisé, il faudra vérifier le fonctionnement de la fonction et consulter ses journaux CloudWatch.

**Attention :** le téléversement modifie le code de la fonction AWS. Il doit être réalisé uniquement après autorisation et validation.

## 8. Sécurité et permissions

Le projet utilise un bucket S3 privé et une fonction Lambda disposant d'un rôle IAM dédié.

La politique de lecture S3 de la fonction autorise `s3:GetObject` sur les objets du bucket du projet. Elle ne lui accorde pas de droits d'écriture ou de suppression.

Aucune clé d'accès AWS permanente ne doit être stockée dans le dépôt GitHub.

## 9. État actuel et améliorations futures

| Élément | État |
|---|---|
| Code Python Lambda | Préparé |
| Tests unitaires | Présents |
| GitHub Actions CI | Configurée |
| Paquet ZIP | Préparé localement |
| Déploiement manuel AWS | Non effectué |
| Déploiement automatique CD | Non configuré |
| Accès AWS par OIDC | Amélioration future |

Une évolution possible consiste à mettre en place un déploiement automatisé avec GitHub Actions et AWS OIDC, au moyen d'un rôle IAM dédié et de permissions limitées.

Cette évolution nécessitera une configuration IAM autorisée.

## 10. Objectifs pédagogiques

Ce projet permet de pratiquer :
- Le stockage sécurisé avec Amazon S3.
- Le traitement événementiel avec AWS Lambda.
- La gestion des permissions avec IAM.
- Les tests automatisés avec Python et pytest.
- L'intégration continue avec GitHub Actions.
- La préparation d'un paquet de déploiement Lambda.
- Les principes de sécurité et de moindre privilège.

---

**Projet personnel de formation AWS et DevOps.**

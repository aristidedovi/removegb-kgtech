# Flask Image Background Removal

This Flask application provides an API endpoint to remove the background from images using the `rembg` library. The application also includes functionality to resize images to a square format.

## Prérequis

Avant de commencer, assurez-vous d'avoir Python et `pip` installés sur votre machine. Vous aurez également besoin des packages suivants :

- Flask
- rembg
- Pillow

## Installation

1. **Clonez le dépôt :**

   ```bash
   git clone https://github.com/votre-utilisateur/votre-repository.git
   cd votre-repository
   ```

2. **Créez un environnement virtuel :**

   ```bash
   python -m venv venv
   ```

3. **Activez l'environnement virtuel :**

   - Sur **Windows** :

     ```bash
     venv\Scripts\activate
     ```

   - Sur **macOS/Linux** :

     ```bash
     source venv/bin/activate
     ```

4. **Créez un fichier `requirements.txt` avec les dépendances suivantes :**

   ```text
   Flask
   rembg
   Pillow
   ```

5. **Installez les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

L'application utilise les dossiers suivants pour stocker les fichiers :

- `flaskr/static/uploads/` : Pour les images téléchargées.
- `flaskr/static/outputs/` : Pour les images traitées.

Assurez-vous que ces dossiers existent dans votre répertoire de projet. Vous pouvez créer ces dossiers en exécutant :

```bash
mkdir -p flaskr/static/uploads
mkdir -p flaskr/static/outputs
```

## Utilisation

1. **Démarrez le serveur Flask :**

   Assurez-vous que votre fichier principal Flask est nommé `app.py`. Vous pouvez démarrer le serveur avec :

   ```bash
   python wsgi.py
   ```

   Par défaut, le serveur sera disponible à l'adresse `http://localhost:5000`.

2. **API Endpoint pour supprimer l'arrière-plan :**

   - **URL** : `/api/v1/remove-background`
   - **Méthode** : `POST`
   - **Paramètres** : `images` (un ou plusieurs fichiers image à traiter)

   **Exemple de requête avec `curl` :**

   ```bash
   curl -X POST http://localhost:5000/api/v1/remove-background -F "images=@path/to/your/image.jpg"
   ```

   **Réponse** : JSON contenant les URLs des images traitées.

   ```json
   {
     "message": "Images processed",
     "files": [
       "/static/outputs/modified_filename.jpg"
     ]
   }
   ```

## Fonctionnalités

- **Suppression de l'arrière-plan** : Envoie une image à l'endpoint pour retirer son arrière-plan.
- **Redimensionnement en format carré** : Les images traitées sont redimensionnées pour être au format carré (500x500 pixels par défaut).

## Développement

Pour développer ou modifier l'application, voici quelques points clés :

- Les routes et la logique de traitement des images sont définies dans le fichier `app.py`.
- Les images sont traitées en utilisant les bibliothèques `rembg` et `Pillow`.

## License

Ce projet est sous la licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contact

Pour toute question, veuillez contacter [dovi.aristide@gmail.com]mailto:dovi.aristide@gmail.com).

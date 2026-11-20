
import urllib.parse
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")

BUCKET_AUTORISE = "projet-aws-stockage-securise-2026"
TAILLE_MAX = 1024 * 1024  # 1 Mio


def lambda_handler(event, context):
    print("Début du traitement S3")

    for record in event.get("Records", []):
        try:
            bucket = record["s3"]["bucket"]["name"]
            objet = record["s3"]["object"]

            key = urllib.parse.unquote_plus(objet["key"])
            taille = objet["size"]

            if bucket != BUCKET_AUTORISE:
                raise ValueError("Bucket non autorisé")

            if not key or key.endswith("/"):
                raise ValueError("Nom de fichier invalide")

            if not key.lower().endswith(".txt"):
                raise ValueError(
                    "Format refusé : seuls les fichiers .txt sont acceptés"
                )

            if (
                not isinstance(taille, int)
                or taille <= 0
                or taille > TAILLE_MAX
            ):
                raise ValueError(
                    "Taille de fichier invalide ou supérieure à 1 Mio"
                )

            print(f"Fichier validé : {key}")
            print(f"Taille : {taille} octets")

            response = s3.get_object(Bucket=bucket, Key=key)

            contenu = response["Body"].read(4096).decode(
                "utf-8",
                errors="replace"
            )

            print("Lecture du fichier réussie")

        except (ClientError, KeyError, ValueError) as error:
            print(f"Erreur pendant le traitement : {error}")
            raise

    return {
        "statusCode": 200,
        "body": "Traitement terminé avec succès"
    }

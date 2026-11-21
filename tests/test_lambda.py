
import io
import pytest
from src import lambda_function


def creer_evenement(nom, taille):
    return {
        "Records": [{
            "s3": {
                "bucket": {
                    "name": "projet-aws-stockage-securise-2026"
                },
                "object": {
                    "key": nom,
                    "size": taille
                }
            }
        }]
    }


def test_fichier_txt_accepte(monkeypatch):
    monkeypatch.setattr(
        lambda_function.s3,
        "get_object",
        lambda **kwargs: {"Body": io.BytesIO(b"Bonjour AWS")}
    )

    event = creer_evenement("test.txt", 100)
    resultat = lambda_function.lambda_handler(event, None)

    assert resultat["statusCode"] == 200


def test_fichier_pdf_refuse():
    event = creer_evenement("document.pdf", 100)

    with pytest.raises(ValueError, match="Format refusé"):
        lambda_function.lambda_handler(event, None)


def test_fichier_trop_volumineux_refuse():
    event = creer_evenement("grand.txt", 2 * 1024 * 1024)

    with pytest.raises(ValueError, match="Taille de fichier"):
        lambda_function.lambda_handler(event, None)

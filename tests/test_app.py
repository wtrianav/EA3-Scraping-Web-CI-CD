"""Pruebas unitarias automatizadas para validar el scraper y el generador web."""
import os
from scraper import get_books
from build_web import generate_html


def test_get_books_returns_valid_data():
    libros = get_books(limit=5)
    assert len(libros) == 5, "Debe extraer exactamente 5 libros"
    for libro in libros:
        assert "Titulo" in libro and libro["Titulo"]
        assert "Precio_GBP" in libro and libro["Precio_GBP"] > 0
        assert "Disponibilidad" in libro
        assert 1 <= libro["Rating"] <= 5


def test_generate_html_creates_index(tmp_path):
    muestra = [{
        "Titulo": "Libro de Prueba",
        "Precio_Texto": "£25.00",
        "Precio_GBP": 25.0,
        "Disponibilidad": "In stock",
        "Rating": 5
    }]
    output_file = generate_html(muestra, output_dir=str(tmp_path))
    assert os.path.exists(output_file), "El archivo index.html debe generarse"
    with open(output_file, "r", encoding="utf-8") as f:
        contenido = f.read()
    assert "Libro de Prueba" in contenido
    assert "£25.00" in contenido

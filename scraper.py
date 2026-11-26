"""
Módulo de extracción de datos (Web Scraping) para Books to Scrape.
Extrae título, precio numérico, disponibilidad y calificación de los libros.
"""
import os
import json
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

TARGET_URL = os.getenv("TARGET_URL", "https://books.toscrape.com/")
MAX_ITEMS = int(os.getenv("MAX_ITEMS", "20"))

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_books(url: str = TARGET_URL, limit: int = MAX_ITEMS) -> list[dict]:
    """Realiza una petición HTTP GET y extrae los datos de los libros."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    productos = soup.find_all("article", class_="product_pod")

    items = []
    for item in productos[:limit]:
        titulo = item.find("h3").find("a")["title"]
        precio_texto = item.find("p", class_="price_color").text.strip()
        precio_num = float(re.sub(r"[^0-9.]", "", precio_texto))
        disponibilidad = item.find("p", class_="instock availability").text.strip()

        rating_tag = item.find("p", class_="star-rating")
        rating_word = next((c for c in rating_tag["class"] if c in RATING_MAP), "One")
        rating_num = RATING_MAP[rating_word]

        items.append({
            "Titulo": titulo,
            "Precio_Texto": precio_texto,
            "Precio_GBP": precio_num,
            "Disponibilidad": disponibilidad,
            "Rating": rating_num
        })
    return items


def save_outputs(data: list[dict], csv_path: str = "libros.csv", json_path: str = "libros.json") -> None:
    """Guarda los datos extraídos en formatos CSV y JSON."""
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False, encoding="utf-8")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    libros = get_books()
    save_outputs(libros)
    print(f"Extracción completada: {len(libros)} libros guardados en libros.csv y libros.json.")

"""
Generador de la aplicación web estática (dist/index.html) a partir de los datos extraídos.
"""
import os
import json
from datetime import datetime, timezone
from scraper import get_books, save_outputs


def generate_html(libros: list[dict], output_dir: str = "dist") -> str:
    """Construye una aplicación web responsiva con búsqueda y métricas."""
    os.makedirs(output_dir, exist_ok=True)
    precios = [b["Precio_GBP"] for b in libros]
    total = len(libros)
    promedio = sum(precios) / total if total else 0.0
    minimo = min(precios) if total else 0.0
    maximo = max(precios) if total else 0.0
    fecha_actualizacion = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    data_json = json.dumps(libros, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Monitor de Precios - Books to Scrape (CI/CD)</title>
  <style>
    :root {{
      --bg: #f4f6f9;
      --card: #ffffff;
      --primary: #1e3a8a;
      --accent: #2563eb;
      --text: #1f2937;
      --muted: #6b7280;
      --border: #e5e7eb;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.5; }}
    header {{ background: var(--primary); color: #fff; padding: 2rem 1.5rem; text-align: center; }}
    header h1 {{ font-size: 1.8rem; margin-bottom: 0.4rem; }}
    header p {{ opacity: 0.9; font-size: 0.95rem; }}
    main {{ max-width: 1050px; margin: 2rem auto; padding: 0 1rem; }}
    .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }}
    .kpi {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 1.2rem; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .kpi span {{ display: block; font-size: 0.85rem; color: var(--muted); }}
    .kpi strong {{ font-size: 1.5rem; color: var(--primary); }}
    .controls {{ display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }}
    .controls input, .controls select {{ padding: 0.65rem 0.9rem; border: 1px solid var(--border); border-radius: 8px; font-size: 0.95rem; background: #fff; }}
    .controls input {{ flex: 1; min-width: 240px; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 10px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    th, td {{ padding: 0.85rem 1rem; text-align: left; border-bottom: 1px solid var(--border); }}
    th {{ background: #eff6ff; color: var(--primary); font-weight: 600; }}
    tr:hover {{ background: #f9fafb; }}
    .badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 999px; font-size: 0.8rem; background: #dcfce7; color: #166534; }}
    footer {{ text-align: center; padding: 2rem 1rem; color: var(--muted); font-size: 0.85rem; }}
  </style>
</head>
<body>
  <header>
    <h1>Monitor de Catálogo: Books to Scrape</h1>
    <p>Aplicación web desplegada automáticamente mediante GitHub Actions (CI/CD) en GitHub Pages</p>
  </header>
  <main>
    <section class="kpis">
      <div class="kpi"><span>Libros Analizados</span><strong>{total}</strong></div>
      <div class="kpi"><span>Precio Promedio</span><strong>£{promedio:.2f}</strong></div>
      <div class="kpi"><span>Precio Mínimo</span><strong>£{minimo:.2f}</strong></div>
      <div class="kpi"><span>Precio Máximo</span><strong>£{maximo:.2f}</strong></div>
    </section>
    <section class="controls">
      <input type="text" id="searchInput" placeholder="Buscar libro por título..." />
      <select id="ratingFilter">
        <option value="0">Todas las calificaciones</option>
        <option value="5">5 estrellas</option>
        <option value="4">4 estrellas o más</option>
        <option value="3">3 estrellas o más</option>
      </select>
    </section>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Título del Libro</th>
          <th>Precio</th>
          <th>Calificación</th>
          <th>Disponibilidad</th>
        </tr>
      </thead>
      <tbody id="booksBody"></tbody>
    </table>
  </main>
  <footer>
    Última actualización automatizada: {fecha_actualizacion} | Proyecto EA3 - Ingeniería de Software y Datos (IU Digital de Antioquia)
  </footer>
  <script>
    const libros = {data_json};
    const tbody = document.getElementById("booksBody");
    const searchInput = document.getElementById("searchInput");
    const ratingFilter = document.getElementById("ratingFilter");

    function render() {{
      const q = searchInput.value.toLowerCase();
      const minRating = parseInt(ratingFilter.value, 10);
      const filtered = libros.filter(b => b.Titulo.toLowerCase().includes(q) && b.Rating >= minRating);
      tbody.innerHTML = filtered.map((b, i) => `
        <tr>
          <td>${{i + 1}}</td>
          <td>${{b.Titulo}}</td>
          <td><strong>${{b.Precio_Texto}}</strong></td>
          <td>${{"★".repeat(b.Rating)}}${{ "☆".repeat(5 - b.Rating) }}</td>
          <td><span class="badge">${{b.Disponibilidad}}</span></td>
        </tr>
      `).join("");
    }}

    searchInput.addEventListener("input", render);
    ratingFilter.addEventListener("change", render);
    render();
  </script>
</body>
</html>
"""
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path


if __name__ == "__main__":
    libros = get_books()
    save_outputs(libros)
    path = generate_html(libros)
    print(f"Aplicación web generada exitosamente en {path}")

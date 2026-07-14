#!/usr/bin/env python3
"""
Script para generar la lista de fotos
XV Años Karla Lizbeth Bustamante Hernandez
"""

import os
import glob
import json

def generate_photo_list(photos_dir="imagenes", output_file="photos_list.js"):
    photos_list = []
    seen = set()

    # Subcarpetas con categoría
    subcarpetas = [
        "1. Misa",
        "2. fiesta vals",
        "3. fiesta torito",
        "4. extras",
    ]

    for subdir in subcarpetas:
        subdir_path = os.path.join(photos_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue
        webp_files = sorted(glob.glob(os.path.join(subdir_path, "*.webp")))
        print(f"  {subdir}: {len(webp_files)} fotos")
        for webp_path in webp_files:
            filename = os.path.basename(webp_path)
            name_without_ext = os.path.splitext(filename)[0]
            rel_path = f"{photos_dir}/{subdir}/{filename}"
            thumb_path = f"{photos_dir}/thumb/{subdir}/{filename}"
            if name_without_ext not in seen:
                seen.add(name_without_ext)
                entry = {
                    "name": name_without_ext,
                    "path": rel_path,
                    "filename": filename,
                    "category": subdir,
                }
                if os.path.exists(thumb_path):
                    entry["thumb"] = thumb_path
                photos_list.append(entry)

    # Fotos sueltas en raíz (sin duplicar)
    root_files = sorted(glob.glob(os.path.join(photos_dir, "*.webp")))
    root_count = 0
    for webp_path in root_files:
        filename = os.path.basename(webp_path)
        name_without_ext = os.path.splitext(filename)[0]
        if name_without_ext not in seen:
            seen.add(name_without_ext)
            photos_list.append({
                "name": name_without_ext,
                "path": f"{photos_dir}/{filename}",
                "filename": filename,
                "category": "general",
            })
            root_count += 1
    if root_count:
        print(f"  general (raíz): {root_count} fotos")

    if not photos_list:
        print(f"No se encontraron archivos WebP en {photos_dir}")
        return

    js_code = f"""// Lista de fotos generada automaticamente
// XV Anos Karla Lizbeth Bustamante Hernandez
// Total de fotos: {len(photos_list)}
// Generado: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

const photos = {json.dumps(photos_list, indent=4, ensure_ascii=False)};

window.addEventListener('DOMContentLoaded', function() {{
    console.log(`Cargadas ${{photos.length}} fotos`);
    renderGallery();
    updateStats();
}});
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_code)

    print(f"\nArchivo generado: {output_file}")
    print(f"Total de fotos: {len(photos_list)}")
    print(f"\nAhora puedes abrir selector.html en el navegador")

if __name__ == "__main__":
    generate_photo_list()

# exporter.py
from docx import Document

def export_project_to_word(file_path, projekt_data):
    doc = Document()
    doc.add_heading("Projekt Árajánlat", level=0)
    doc.add_paragraph(f"Projekt neve: {projekt_data['projektnev']}")
    doc.add_paragraph(f"Megrendelő neve: {projekt_data['megrendelo']}")
    doc.add_paragraph(f"Lakcím: {projekt_data['cim']}")
    doc.add_paragraph("")

    for helyseg in projekt_data['helyisegek']:
        doc.add_heading(helyseg['nev'], level=1)
        doc.add_paragraph("Anyag tételek:")
        for t in helyseg['tetel_lista']:
            doc.add_paragraph(
                f"- {t['nev']} | {t['egyseg']} | {t['egysegar']} Ft | {t['mennyiseg']} db | {t.get('megjegyzes','')}",
                style='List Bullet'
            )
        doc.add_paragraph("Kivitelezési tételek:")
        for t in helyseg.get('kivitelezesi_tetelek', []):
            doc.add_paragraph(
                f"- {t['nev']} | {t['egyseg']} | {t['egysegar']} Ft | {t['mennyiseg']} db | {t.get('megjegyzes','')}",
                style='List Bullet'
            )
        doc.add_paragraph("")

    doc.save(file_path)

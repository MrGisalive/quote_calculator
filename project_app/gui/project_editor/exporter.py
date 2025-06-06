from docx import Document

def export_project_to_word(file_path, projekt_data):
    """
    Egy projekt teljes adatstruktúráját szépen formázott Word dokumentumba menti.
    :param file_path: Hová mentse a .docx fájlt.
    :param projekt_data: Dict a projekt minden adatával.
    """
    doc = Document()
    doc.add_heading("Projekt Árajánlat", level=0)
    doc.add_paragraph(f"Projekt neve: {projekt_data['projektnev']}")
    doc.add_paragraph(f"Megrendelő neve: {projekt_data['megrendelo']}")
    doc.add_paragraph(f"Lakcím: {projekt_data['cim']}")
    doc.add_paragraph("")

    # Végigmegyünk a helyiségeken, külön alcímmel, listákkal
    for helyseg in projekt_data['helyisegek']:
        doc.add_heading(helyseg['nev'], level=1)

        # Anyag tételek felsorolása
        doc.add_paragraph("Anyag tételek:")
        for t in helyseg.get('tetel_lista', []):
            doc.add_paragraph(
                f"- {t['nev']} | {t['egyseg']} | {t['egysegar']} Ft | {t['mennyiseg']} db | {t.get('megjegyzes', '')}",
                style='List Bullet'
            )

        # Kivitelezési tételek felsorolása
        doc.add_paragraph("Kivitelezési tételek:")
        for t in helyseg.get('kivitelezesi_tetelek', []):
            doc.add_paragraph(
                f"- {t['nev']} | {t['egyseg']} | {t['egysegar']} Ft | {t['mennyiseg']} db | {t.get('megjegyzes', '')}",
                style='List Bullet'
            )
        doc.add_paragraph("")  # Két helyiség között üres sor

    doc.save(file_path)

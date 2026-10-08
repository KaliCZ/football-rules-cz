"""Rebuild the page-indexed Soutěžní řád transcript, images, and OCR metadata.

Maintenance only: requires pdftotext, PyMuPDF, Tesseract, and Czech traineddata.
The packaged skill and build_skill.py do not require these tools.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import fitz

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / 'skills/football-rules-cz/references'
PDF_NAME = 'soutezni-rad-facr-2026-06-26.pdf'
PDF_SHA256 = '2aa7ce271ab02c79e7f0c591f8f8531fdc97fbaa9b0b198ae4b830f8d018b883'
CES_SHA256 = '934bcaf97ef3348413263331131c9fa7f55f30db333c711929c124fb635f7e1b'
IMAGE_PAGES = (13, 31, 32, 53, 60, 61, 62, 63, 83, 84, 85, 86, 87)
OCR_PAGES = (83, 84, 85, 86, 87)
TABLE_PAGES = (13, 31, 32, 53, 60, 61, 62, 63, 83)
ANNEXES = {53: 1, 54: 2, 60: 3, 64: 4, 65: 5, 72: 6, 75: 7}
HEADER = 'Soutěžní řád FAČR (s účinností od 26. 6. 2026)'


def clean_page(text, number):
    lines = text.splitlines()
    # Remove only the exact running header and the final printed page number.
    lines = [line.rstrip() for line in lines if line.strip() != HEADER]
    while lines and not lines[-1].strip():
        lines.pop()
    if lines and lines[-1].strip() == str(number):
        lines.pop()
    return '\n'.join(lines).strip()


def prose(text):
    """Join line wrapping within paragraphs, preserving legal list markers."""
    out, paragraph = [], []

    def flush():
        if paragraph:
            out.append(' '.join(paragraph))
            paragraph.clear()

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            flush()
        elif re.fullmatch(r'§\s*\d+[a-z]?', line):
            flush()
            out.append('### ' + re.sub(r'§\s*', '§ ', line))
        elif re.match(r'^(ČÁST |HLAVA |Díl |PŘÍLOHA Č\.)', line):
            flush()
            out.append(line)
        else:
            if re.match(r'^(\d+\.|[a-z]{1,2}\))\s', line):
                flush()
            paragraph.append(line)
        i += 1
    flush()
    return '\n\n'.join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, default=REFERENCES / 'sources' / PDF_NAME)
    parser.add_argument('--tessdata-dir', type=Path, required=True)
    args = parser.parse_args()
    source = args.pdf.read_bytes()
    if hashlib.sha256(source).hexdigest() != PDF_SHA256:
        raise ValueError('Unexpected source PDF; review a new edition before changing this converter.')
    model = args.tessdata_dir / 'ces.traineddata'
    if hashlib.sha256(model.read_bytes()).hexdigest() != CES_SHA256:
        raise ValueError('Unexpected Czech OCR model checksum.')
    doc = fitz.open(args.pdf)
    if len(doc) != 87:
        raise ValueError('Expected all 87 pages.')
    result = subprocess.run(['pdftotext', '-layout', str(args.pdf), '-'], check=True,
                            capture_output=True, text=True)
    pages = result.stdout.split('\f')
    if len(pages) != 88 or pages[-1].strip():
        raise ValueError('Unexpected pdftotext page boundaries.')
    pages = [clean_page(text, n) for n, text in enumerate(pages[:-1], 1)]
    index = []
    annex = None
    for number, text in enumerate(pages, 1):
        if number in ANNEXES:
            annex = ANNEXES[number]
            index.append(f'- [Příloha č. {annex}](#pdf-{number:03})')
        if annex is None:
            lines = text.splitlines()
            for i, line in enumerate(lines):
                match = re.fullmatch(r'\s*§\s*(\d+[a-z]?)\s*', line)
                if match:
                    title = next((line.strip() for line in lines[i+1:] if line.strip()), '')
                    index.append(f'- [§ {match[1]} – {title}](#pdf-{number:03})')
    output = [
        '# Soutěžní řád FAČR – znění označené účinností od 26. 6. 2026',
        '> Pracovní převod uživatelem dodaného PDF. Pozdější změny nejsou zahrnuty; '
        'účinnost jednotlivých novel je nutné posoudit podle § 73 odst. 3 a data situace.',
        f'Zdroj: [původní PDF](sources/{PDF_NAME}). PDF obsahuje 87 stran; tištěné '
        'číslování odpovídá pořadí stran PDF (bez posunu). '
        'Nativní text je zachován, tabulky mají pevné rozložení. Obrazové strany 83–87 '
        'mají zvlášť označený automatický OCR přepis; rozměry, tabulky a vztahy '
        'v diagramech ověřuj v přiloženém obrázku nebo PDF, nikoli jen z OCR.',
        f'SHA-256 PDF: `{PDF_SHA256}`.',
        '## Obsah – hlavní řád a přílohy', '\n'.join(index),
    ]
    metadata = []
    with tempfile.TemporaryDirectory() as temp:
        for number, text in enumerate(pages, 1):
            output.extend([f'<a id="pdf-{number:03}"></a>',
                           f'## PDF strana {number} / tištěná strana {number}',
                           f'[PDF, strana {number}](sources/{PDF_NAME}#page={number})'])
            if text:
                output.append('```text\n' + text + '\n```' if number in TABLE_PAGES else prose(text))
            ocr = None
            if number in IMAGE_PAGES:
                image_name = f'soutezni-rad-pdf-{number:03}.png'
                image_path = REFERENCES / 'assets' / image_name
                image_path.parent.mkdir(parents=True, exist_ok=True)
                doc[number-1].get_pixmap(dpi=150).save(image_path)
                output.append(f'![Původní stránka Soutěžního řádu – PDF {number}](assets/{image_name})')
            if number in OCR_PAGES:
                high_resolution = Path(temp) / f'{number}.png'
                doc[number-1].get_pixmap(dpi=300).save(high_resolution)
                result = subprocess.run(['tesseract', str(high_resolution), 'stdout',
                                         '--tessdata-dir', str(args.tessdata_dir), '-l', 'ces',
                                         '--psm', '3'], check=True, capture_output=True, text=True)
                ocr = clean_page(result.stdout, number)
                if not ocr.strip():
                    raise ValueError(f'Empty OCR for page {number}')
                output.extend(['### Automatický OCR přepis obrazové stránky',
                               '> Pomůcka pro vyhledávání; může obsahovat chyby a nezachovává '
                               'prostorové vztahy. Čísla a popisky ověř v obrázku nebo PDF.',
                               '```text\n' + ocr + '\n```'])
            metadata.append({'page': number, 'printed_page': number,
                             'native_text_characters': len(text),
                             'native_text_sha256_without_whitespace': hashlib.sha256(re.sub(r'\s+', '', text).encode()).hexdigest(),
                             'ocr_characters': len(ocr) if ocr is not None else 0,
                             'image': f'assets/soutezni-rad-pdf-{number:03}.png'
                             if number in IMAGE_PAGES else None})
    REFERENCES.mkdir(parents=True, exist_ok=True)
    target = REFERENCES / 'sources' / PDF_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    if args.pdf.resolve() != target.resolve():
        shutil.copyfile(args.pdf, target)
    (REFERENCES / 'competition-regulations-text.md').write_text('\n\n'.join(output) + '\n', encoding='utf-8')
    provenance = {
        'source': 'User-uploaded PDF; official listing URL is a provenance reference, not a verified download.',
        'official_listing': 'https://www.fotbal.cz/urednideska/uredni-deska-predpisy/426?category=1',
        'pdf': f'sources/{PDF_NAME}', 'sha256': PDF_SHA256,
        'edition_label': 's účinností od 26. 6. 2026', 'page_count': 87,
        'pdftotext': subprocess.run(['pdftotext','-v'],capture_output=True,text=True,check=True).stderr.splitlines()[0],
        'pymupdf': fitz.VersionBind,
        'tesseract': subprocess.run(['tesseract','--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],
        'ocr_language': 'ces', 'ocr_dpi': 300, 'ocr_psm': 3,
        'ocr_model_sha256': CES_SHA256,
        'ocr_model_source': 'https://raw.githubusercontent.com/tesseract-ocr/tessdata_fast/main/ces.traineddata',
        'pages': metadata,
    }
    (REFERENCES / 'competition-regulations-provenance.json').write_text(
        json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Converted 87 pages, OCR on 5 image pages, preserved 13 page images.')


if __name__ == '__main__':
    main()

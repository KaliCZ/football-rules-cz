"""Offline coverage, transcription integrity, citations, and packaging checks."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import io

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('build_skill', ROOT / 'scripts/build_skill.py')
BUILD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILD)
REF = BUILD.REFERENCES


def normalized_hash(text):
    return hashlib.sha256(re.sub(r'\s+', '', text).encode()).hexdigest()


class SkillResourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (REF / 'competition-regulations-text.md').read_text(encoding='utf-8')
        cls.metadata = json.loads((REF / 'competition-regulations-provenance.json').read_text())
        cls.pages = dict(re.findall(r'<a id="pdf-(\d{3})"></a>\n(.*?)(?=<a id="pdf-|\Z)', cls.text, re.S))

    def test_pdf_identity_and_complete_page_mapping(self):
        source = REF / self.metadata['pdf']
        checksum = hashlib.sha256(source.read_bytes()).hexdigest()
        self.assertEqual(checksum, '2aa7ce271ab02c79e7f0c591f8f8531fdc97fbaa9b0b198ae4b830f8d018b883')
        self.assertEqual(checksum, self.metadata['sha256'])
        self.assertEqual(self.metadata['page_count'], 87)
        self.assertEqual(set(self.pages), {f'{n:03}' for n in range(1, 88)})
        self.assertEqual([p['page'] for p in self.metadata['pages']], list(range(1, 88)))
        for p in self.metadata['pages']:
            n = p['page']
            self.assertEqual(p['printed_page'], n)
            self.assertIn(f'PDF strana {n} / tištěná strana {n}', self.pages[f'{n:03}'])
            self.assertIn(f'sources/soutezni-rad-facr-2026-06-26.pdf#page={n}', self.pages[f'{n:03}'])

    def test_native_text_preserved_on_every_page(self):
        # Compare every page against hashes recorded directly from the PDF text
        # before prose formatting; this detects dropped/reordered legal text.
        for p in self.metadata['pages']:
            with self.subTest(page=p['page']):
                section = self.pages[f'{p["page"]:03}']
                native = section.split(f'#page={p["page"]})', 1)[1]
                native = native.split('![Původní stránka', 1)[0]
                native = re.sub(r'^### ', '', native, flags=re.M)
                native = native.replace('```text', '').replace('```', '')
                self.assertEqual(normalized_hash(native), p['native_text_sha256_without_whitespace'])

    def test_main_sections_and_seven_annexes_are_indexed(self):
        index = self.text.split('<a id="pdf-001">', 1)[0]
        found = re.findall(r'^- \[§ (\d+[a-z]?) –', index, re.M)
        expected = [str(n) for n in range(1, 74) if n != 41] + ['41a', '41b', '42a', '42b']
        self.assertCountEqual(found, expected)
        for n, page in [(1, 53), (2, 54), (3, 60), (4, 64), (5, 65), (6, 72), (7, 75)]:
            self.assertIn(f'[Příloha č. {n}](#pdf-{page:03})', index)

    def test_ocr_is_searchable_and_images_are_preserved(self):
        self.assertEqual([p['page'] for p in self.metadata['pages'] if p['ocr_characters']], list(range(83, 88)))
        self.assertEqual([p['page'] for p in self.metadata['pages'] if p['image']],
                         [13, 31, 32, 53, 60, 61, 62, 63, 83, 84, 85, 86, 87])
        for p in self.metadata['pages']:
            if p['image']:
                self.assertTrue((REF / p['image']).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
                self.assertIn(p['image'], self.pages[f'{p["page"]:03}'])
            if p['ocr_characters']:
                section = self.pages[f'{p["page"]:03}']
                self.assertIn('Automatický OCR přepis', section)
                self.assertGreater(len(section.split('```text\n', 1)[1].split('```', 1)[0].strip()), 100)
        self.assertIn('BETONOVÝ ZÁHONOVÝ', self.pages['087'])
        self.assertIn('UMĚLÝ TRÁVNÍK', self.pages['087'])

    def test_representative_citations_and_effective_date(self):
        self.assertIn('§ 71', self.pages['050'])
        self.assertIn('Protest', self.pages['050'])
        self.assertIn('Procesním řádem', self.pages['050'])
        self.assertIn('§ 73', self.pages['052'])
        self.assertIn('1. července 2026', self.pages['052'])
        self.assertIn('26. června 2026', self.pages['052'])
        self.assertIn('Pravidlo 11', (REF / 'rules.md').read_text())

    def test_all_links_and_reproducible_archive(self):
        BUILD.verify_links()
        content = BUILD.archive_bytes()
        self.assertEqual(content, BUILD.archive_bytes())
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            self.assertIsNone(z.testzip())
            expected = {'football-rules-cz/' + p.relative_to(BUILD.SKILL).as_posix(): p
                        for p in BUILD.SKILL.rglob('*') if p.is_file()}
            self.assertEqual(set(z.namelist()), set(expected))
            for name, p in expected.items():
                self.assertEqual(z.read(name), p.read_bytes())

    def test_link_validation_rejects_missing_and_unsafe_targets(self):
        with tempfile.TemporaryDirectory() as temp:
            skill = Path(temp)
            doc = skill / 'test.md'
            (skill / 'target.md').write_text('<a id="present"></a>')
            with patch.object(BUILD, 'SKILL', skill):
                for link in ['[missing](absent.pdf)', '[unsafe](../outside.md)',
                             '[anchor](#absent)', '[cross](target.md#absent)']:
                    doc.write_text(link)
                    with self.subTest(link=link), self.assertRaises(ValueError):
                        BUILD.verify_document_links(doc)
                doc.write_text('[valid](target.md#present)')
                BUILD.verify_document_links(doc)


class MisconductReportingResourcesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metadata = json.loads((REF / 'misconduct-reporting-provenance.json').read_text(encoding='utf-8'))
        cls.text = (REF / 'misconduct-reporting-text.md').read_text(encoding='utf-8')
        cls.pages = dict(re.findall(r'<a id="pdf-(\d{3})"></a>\n(.*?)(?=<a id="pdf-|\Z)', cls.text, re.S))

    def test_source_identity_and_all_six_pages(self):
        source = REF / self.metadata['pdf']
        checksum = hashlib.sha256(source.read_bytes()).hexdigest()
        self.assertEqual(checksum, '2e35b1bc52ca4d4aa0aaaafc68be72198235969a1c5c75692ad853d5ef77a923')
        self.assertEqual(checksum, self.metadata['sha256'])
        self.assertEqual(self.metadata['page_count'], 6)
        self.assertEqual(set(self.pages), {f'{number:03}' for number in range(1, 7)})
        self.assertEqual([page['page'] for page in self.metadata['pages']], list(range(1, 7)))
        for page in self.metadata['pages']:
            number = page['page']
            with self.subTest(page=number):
                self.assertEqual(page['printed_page'], number)
                section = self.pages[f'{number:03}']
                self.assertIn(f'PDF strana {number} / tištěná strana {number}', section)
                self.assertIn(f'{self.metadata["pdf"]}#page={number}', section)
                native = section.split('```text\n', 1)[1].split('\n```', 1)[0]
                self.assertEqual(len(native), page['native_text_characters'])
                self.assertEqual(normalized_hash(native), page['native_text_sha256_without_whitespace'])


if __name__ == '__main__':
    unittest.main()

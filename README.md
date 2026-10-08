# Pravidla fotbalu a Soutěžní řád v češtině

Tento skill umožňuje ptát se AI asistenta, například ChatGPT nebo Claude, na pravidla fotbalu. Asistent vyhledá odpověď v přiložených pravidlech, prověří související ustanovení a výjimky a uvede, kde ji najdeš: konkrétní pravidlo, oddíl a stránku.

Vychází z českých pravidel FAČR platných od **1. 7. 2024**; změny z let 2025 a 2026 nejsou zapracovány.

## Soutěžní řád FAČR

Skill rozlišuje herní pravidla a soutěžní administrativu. Nový balíček obsahuje [úplný textový přepis Soutěžního řádu](skills/football-rules-cz/references/competition-regulations-text.md), [původní PDF](skills/football-rules-cz/references/sources/soutezni-rad-facr-2026-06-26.pdf) a [pokyny pro výklad a citace](skills/football-rules-cz/references/competition-regulations.md). Běžné otázky k oběma dokumentům nevyžadují web ani OCR za běhu. Pro nové zdroje nahraj nově sestavený ZIP; starší ruční import se s GitHubem nesynchronizuje.

Soutěžní řád obsahuje všech 87 stran, hlavní řád a sedm příloh. Vydání je označené účinností od **26. 6. 2026**; § 73 odst. 3 uvádí také novelizace účinné od 1. 7. 2026. Skill ověřuje účinnost pro datum konkrétní situace a nerozšiřuje vydání Pravidel fotbalu 2024 na soutěžní předpis. Pozdější změny ani shoda dodaného PDF s právě zveřejněným zněním nebyly ověřeny. Rozpisy konkrétních soutěží a jiné odkazované předpisy nejsou přiloženy.

PDF dodal uživatel 7. 10. 2026; [oficiální stránka FAČR](https://www.fotbal.cz/urednideska/uredni-deska-predpisy/426?category=1) slouží pro kontrolu novějších verzí. Nativní text byl zachován, pět obrazových stran (83–87) má označený český OCR přepis. Třináct stránkových obrázků zachovává tabulky, vzory a diagramy (13, 31–32, 53, 60–63, 83–87). OCR je pomůcka pro vyhledávání; rozměry, hodnoty a prostorové vztahy se ověřují v obrázku nebo PDF. Tištěná čísla odpovídají stránkám PDF bez posunu.

SHA-256 dodaného PDF: `2aa7ce271ab02c79e7f0c591f8f8531fdc97fbaa9b0b198ae4b830f8d018b883`. [Metadata převodu](skills/football-rules-cz/references/competition-regulations-provenance.json) zaznamenávají použité nástroje, kontrolní součty a pokrytí jednotlivých stran. Převod je pracovní pomůcka; práva k textu a obrazovým částem zůstávají původním nositelům.

Například: „Použij $football-rules-cz a podle přiloženého Soutěžního řádu FAČR vysvětli, na jaký předpis odkazuje § 71 při podání protestu. Uveď přesné ustanovení a stránku.“ Pro konkrétní postup doplň soutěž, ročník a datum situace i potřebné další předpisy.

## Instalace skillu

Pro ChatGPT i Claude se používá stejný ZIP se skillem, pravidly a obrázky. Není potřeba plugin, marketplace, konektor ani MCP server.

Stáhni **skill ZIP** z [nejnovějšího vydání](https://github.com/KaliCZ/football-rules-cz/releases/latest): soubor pojmenovaný `football-rules-cz-skill-` s číslem verze a příponou `.zip`. Nevybírej automatické archivy **Source code** a ZIP před nahráním nerozbaluj.

### ChatGPT — web, desktopová aplikace a Android

**Instalaci proveď přes web.** Po nahrání skill funguje také v desktopové aplikaci ChatGPT a na Androidu, pokud používáš stejný účet; autor projektu obě aplikace ověřil.

1. V prohlížeči otevři [ChatGPT — Plugins](https://chatgpt.com/plugins) a přihlas se. Na tuto stránku se dostaneš také přes **Settings → Plugins → Browse plugins**.
2. Přepni na záložku **Skills**.
3. Klikni na **+ → Upload from your computer** a vyber stažený skill ZIP.
4. Ověř, že je **Pravidla fotbalu a Soutěžní řád (CZ)** mezi nainstalovanými skilly, a začni nový chat s tímto skillem.
5. V desktopové nebo Android aplikaci se přihlas ke stejnému účtu a začni nový chat se skillem. Další instalace v aplikaci není potřeba.

![Settings → Plugins → Browse plugins](docs/images/chatgpt-settings-plugins.png)

![Skills → + → Upload from your computer](docs/images/chatgpt-upload-skill.png)

Pro první otázku zkus:

> Použij skill Pravidla fotbalu 2024 (CZ). Může být hráč v ofsajdu přímo z vhazování? Uveď pravidlo a stránku.

Odpověď má začínat upozorněním, že vychází z vydání FAČR 2024. Autor projektu dne 20. 9. 2026 potvrdil funkčnost po webové instalaci v desktopové aplikaci i na Androidu; úplné načtení pravidel a správnost všech odpovědí nejsou tímto potvrzeny.

### Claude — web a desktopová aplikace

**Instalaci proveď přes web.** Po nahrání skill funguje také v desktopové aplikaci Claude pod stejným účtem; autor projektu tuto funkčnost ověřil.

1. V prohlížeči otevři [Claude — Skills](https://claude.ai/customize/skills) a přihlas se. Na tuto stránku se dostaneš také přes **Settings → Skills** (v části **Customize**).
2. Klikni na **Add → Upload skill** a vyber stejný stažený skill ZIP.
3. Skill zapni a začni nový chat, ve kterém jej požádáš o odpověď podle pravidel FAČR 2024.
4. V desktopové aplikaci se přihlas ke stejnému účtu a začni nový chat se skillem. Další instalace v aplikaci není potřeba.

![Settings → Skills → Add → Upload skill](docs/images/claude-upload-skill.png)

Postup odpovídá přiloženému screenshotu. Autor dne 20. 9. 2026 ověřil instalaci ve webové verzi Claude a použití v desktopové aplikaci.

### Claude — mobilní aplikace: nefunguje

**V aplikaci Claude na Androidu tento skill nefunguje.** Autor ověřil, že mobilní aplikace nahraný skill nepoužívá ani po instalaci ve webové verzi Claude.

Pro použití na telefonu použij aplikaci ChatGPT, kde je funkčnost potvrzená. Na iOS zatím tento skill nebyl otestován.

### Aktualizace a soubory v odpovědi

Novou verzi stáhni z GitHub Releases a nahraj ji přes správu skillů. Ruční import ZIPu není automatická synchronizace s repozitářem; po změně začni nový chat.

Skill má přednostně zpřístupnit původní PDF nebo potřebný diagram přímo jako přílohu v chatu, pokud to daná aplikace umožňuje. Samotné uložení souboru ve skillu nezaručuje, že na něj uživatel může kliknout. Pokud příloha není možná, může odpověď obsahovat označený externí odkaz.

Citace „PDF, strana 162“ musí odkazovat na PDF a označuje pořadí stránky v PDF. Odkaz na Markdown má být označen jako textový přepis. Prohlížeč v aplikaci nemusí podporovat automatické otevření konkrétní stránky.

## Obsah

- [Pravidla v Markdownu](skills/football-rules-cz/references/rules.md)
- [Původní PDF](skills/football-rules-cz/references/sources/pravidla-fotbalu-facr-2024.pdf)
- [Samostatné obrázky](skills/football-rules-cz/references/assets/)


Soubor `rules.md` obsahuje všech 17 pravidel, rozhodnutí FAČR, výklady, slovníčky a praktické pokyny pro rozhodčí. Zachovává odkazy na jednotlivé stránky původního PDF. Tištěné číslování je oproti pořadí stránky v PDF posunuté o 2.

Obrazové části jsou uložené jako samostatné PNG soubory a vložené pomocí relativních Markdown odkazů. Více diagramů ze stejné stránky může být zachováno společně, aby neztratily vzájemné souvislosti a popisky. Souhrnná tabulka k pokutovým kopům je převedena do Markdown tabulky, s odkazem na její původní podobu.

Pro práci s Pravidly fotbalu stačí `rules.md`; Soutěžní řád má samostatný přepis `competition-regulations-text.md`. Při otázkách závislých na konkrétním diagramu je potřeba otevřít také odkazovaný obrázek; text uvnitř rastrových obrázků Pravidel fotbalu není přepsán do Markdownu; u Soutěžního řádu je obrazový obsah doplněn označeným OCR.

## Původ a převod

- Dokument: **Pravidla fotbalu platná od 1. 7. 2024**.
- Zpracovala Pravidlová komise FAČR; vydalo Nakladatelství Olympia, s.r.o.
- ISBN: **978-80-7376-695-5**.
- PDF: **171 stránek**, včetně obálky a závěrečných stran.
- Staženo 20. 9. 2026 z [OFS Jičín](https://ofs-jicin.cz/wp-content/uploads/2024/08/pravidla-fotbalu-facr-2024.pdf).
- [Dokument na webu FAČR](https://www.fotbal.cz/facr/document/download/136707).
- SHA-256 PDF: `deca4c192c10ba0a5b70882eb6fbb26cdf2b011d3b5fc81aa5de95acb3ae7306`.

Převod byl proveden pomocí pdfplumber 0.11.9 z textové vrstvy PDF. Byla odstraněna opakovaná záhlaví a zápatí, spojena slova rozdělená na konci řádků, obnoveny mezery a struktura nadpisů a opraveno chybné kódování tiráže. Obrázky zachovávají původní grafický obsah; nejde o nově vytvořené ilustrace.

Jde o pracovní převod, nikoli nové oficiální vydání. Pro kontrolu znění slouží přiložené PDF. Autorská práva k převzatému textu a ilustracím zůstávají původním nositelům práv; tento repozitář jim nepřiděluje novou licenci.

## Údržba a vydání

Kanonická sada obou předpisů, jejich PDF a obrazových částí je v `skills/football-rules-cz/references/`. Instrukce jsou v `skills/football-rules-cz/SKILL.md`. Distribuční ZIP obsahuje tuto složku skillu včetně referencí, nikoli soubory dokumentace repozitáře.

S Pythonem 3.10 nebo novějším spusť z kořene repozitáře:

```sh
python -m unittest discover -s tests -v
python scripts/build_skill.py --check
python scripts/build_skill.py --version 0.3.0
```

Testy kontrolují pokrytí a integritu přepisu, obrazové reference a balení. Příkaz `--check` kontroluje odkazy a strukturu; sestavení s `--version` navíc vytvoří reprodukovatelný ZIP a kontrolní součet do `dist/`. Verzi při sestavení zadáváš povinným parametrem `--version` ve formátu `MAJOR.MINOR.PATCH`, například `0.2.1`. Skript nečte Git tagy ani stav checkoutu a nepotřebuje soubor s verzí. Samotné `--check` verzi nevyžaduje. Generované soubory jsou ignorované Gitem a přikládají se k vydání na GitHub Releases; necommitují se. Před vydáním proveď [kontroly a scénáře](docs/publishing-and-testing.md).

### Opakování převodu Soutěžního řádu

Přiložené výsledky se při běžném sestavení ZIPu znovu negenerují. Pro údržbu převodu slouží `scripts/extract_competition_regulations.py`; vyžaduje Poppler (`pdftotext`), PyMuPDF a Tesseract s českým modelem `ces.traineddata` z oficiálního projektu `tesseract-ocr/tessdata_fast`. Verze použité při převodu jsou v metadatech. Skript ověřuje SHA-256 PDF a českého modelu před zpracováním, zachovává nativní text, OCR provádí pouze na obrazových stranách a vytváří přepis i stránkové PNG. Nové vydání vyžaduje samostatnou kontrolu mapování stran a účinnosti, nikoli jen změnu kontrolního součtu.

```sh
python scripts/extract_competition_regulations.py --tessdata-dir /cesta/k/tessdata
python scripts/build_skill.py --check
```

Při prvním převodu lze zadat `--pdf /cesta/k/dodanemu.pdf`. Převod přepisuje pouze své generované reference; před spuštěním zkontroluj místní změny. Nejde o závislosti potřebné k používání skillu nebo k sestavení ZIPu.

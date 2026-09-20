# Pravidla fotbalu v češtině

Pravidla fotbalu FAČR z roku 2024 převedená do jednoho Markdown souboru. Vydání je platné od **1. 7. 2024**; změny z let 2025 a 2026 nejsou zapracovány.

- [Pravidla v Markdownu](plugins/football-rules-cz/skills/football-rules-cz/references/rules.md)
- [Původní PDF](plugins/football-rules-cz/skills/football-rules-cz/references/sources/pravidla-fotbalu-facr-2024.pdf)
- [Samostatné obrázky](plugins/football-rules-cz/skills/football-rules-cz/references/assets/)

## Obsah

Soubor `rules.md` obsahuje všech 17 pravidel, rozhodnutí FAČR, výklady, slovníčky a praktické pokyny pro rozhodčí. Zachovává odkazy na jednotlivé stránky původního PDF. Tištěné číslování je oproti pořadí stránky v PDF posunuté o 2.

Obrazové části jsou uložené jako samostatné PNG soubory a vložené pomocí relativních Markdown odkazů. Více diagramů ze stejné stránky může být zachováno společně, aby neztratily vzájemné souvislosti a popisky. Souhrnná tabulka k pokutovým kopům je převedena do Markdown tabulky, s odkazem na její původní podobu.

Pro práci s textem stačí `rules.md`. Při otázkách závislých na konkrétním diagramu je potřeba otevřít také odkazovaný obrázek; text uvnitř rastrových obrázků není přepsán do Markdownu.

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

## Plugin pro ChatGPT, Codex a Claude

[Plugin](plugins/football-rules-cz/) obsahuje skill s úplnými pravidly, PDF a samostatnými diagramy. Nepotřebuje MCP server ani vlastní backend. Model má před první odpovědí přečíst celý text; pokud tomu zabrání limit kontextu, musí přiznat omezený rozsah kontroly a ověřit související ustanovení. Instrukce nezaručují neomezený kontext ani bezchybné odpovědi.

### Codex: instalace z tohoto repozitáře

V aktuálním Codex CLI s příkazem `plugin add`:

```sh
codex plugin marketplace add KaliCZ/football-rules-cz
codex plugin add football-rules-cz@personal
```

Marketplace v tomto repozitáři se jmenuje `personal`. Pokud už máš jiný marketplace se stejným názvem, nepřepisuj ho; použij vlastní lokální marketplace s jiným názvem a odkazem na složku pluginu. Instalace z hlavní větve bude dostupná po sloučení změny s pluginem.

Spusť novou relaci a požádej například:

> Použij $football-rules-cz. Může být hráč v ofsajdu přímo z vhazování? Odpověz podle FAČR 2024 a uveď stránku.

### Claude Code: instalace z veřejného repozitáře

Po sloučení této změny spusť v Claude Code:

```text
/plugin marketplace add KaliCZ/football-rules-cz
/plugin install football-rules-cz@football-rules-cz
```

Potom otevři novou relaci a použij:

```text
/football-rules-cz:football-rules-cz Může být hráč v ofsajdu přímo z vhazování? Uveď pravidlo a stránku.
```

Claude používá stejný skill, pravidla a obrázky jako ChatGPT/Codex. Jeho manifest je v `plugins/football-rules-cz/.claude-plugin/plugin.json`, veřejný marketplace v `.claude-plugin/marketplace.json`. Není potřeba přístup do autorova účtu nebo workspace.

### Claude: instalace přes aplikaci

V aplikacích, kde je tato nabídka dostupná, otevři **Customize → Plugins → Personal plugins → + → Add marketplace → Add from a repository** a vlož `https://github.com/KaliCZ/football-rules-cz`. Alternativně lze nahrát ZIP pluginu vytvořený příkazem `python scripts/build_plugin.py`, pokud aplikace nabízí import vlastního pluginu. Nestahuj ZIP celého repozitáře; distribuční ZIP má manifest a skills přímo v kořeni.

Dostupnost těchto možností závisí na aplikaci a účtu. Instalace v Claude Code ani lokální instalace v Claude Desktop sama o sobě nedokazuje dostupnost na telefonu; mobilní použití tohoto balíčku zatím není otestováno. Repozitář není automaticky zařazen do vestavěného katalogu Anthropic.

Zdroje: [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [pluginy v aplikaci Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude), ověřeno 20. 9. 2026.

### ChatGPT na Androidu a iOS

Mobilní aplikace umí používat pluginy dostupné účtu, ale odkaz na tento GitHub repozitář sám o sobě plugin nenainstaluje. Instalace v lokálním Codex CLI také nedokládá dostupnost v mobilním účtu. Pokud mobil zobrazuje pouze katalog, je třeba plugin nejprve zpřístupnit přes podporované sdílení účtu či workspace, nebo jej zveřejnit ve společném katalogu ChatGPT a Codex.

**Tento plugin zatím nebyl odeslán ke schválení ani zveřejněn v katalogu. Mobilní instalace a odpovědi zatím nejsou ověřené.** Volitelný ZIP vytvořený příkazem `python scripts/build_plugin.py` slouží pro předání balíčku a publikaci, nikoli jako slíbený import v Android aplikaci.

Postup zveřejnění a konkrétní zkušební otázky jsou v [návodu pro publikaci a testování](docs/publishing-and-testing.md). Po zpřístupnění plugin nainstaluj v sekci Plugins, otevři nový chat a vyber jej přes `@` nebo jej výslovně požádej o použití.

Ověřeno proti dokumentaci dne 20. 9. 2026: [podporované aplikace](https://learn.chatgpt.com/docs/plugins), [formát balíčku](https://developers.openai.com/plugins/build/plugins), [publikace](https://developers.openai.com/plugins/deploy/submission). Nabídka instalace se může lišit podle účtu a aplikace.

### Údržba balíčku

Jediná sada zdrojů je v `plugins/football-rules-cz/skills/football-rules-cz/references/`: `rules.md`, `assets/` a `sources/`. Upravuj přímo tyto soubory. Jsou součástí instalovaného skillu, takže není potřeba kopie v kořeni repozitáře.

Z kořene repozitáře s Pythonem 3.10 nebo novějším:

```sh
python scripts/build_plugin.py
python scripts/build_plugin.py --check
```

Skript používá pouze standardní knihovnu. Přepínač `--check` ověří zdrojové soubory, odkazy a soulad manifestů bez vytváření ZIPu. Bez přepínače sestaví reprodukovatelný ZIP do `dist/football-rules-cz.zip`. Složka `dist/` je ignorovaná Gitem; ZIP se necommituje a pro instalaci z GitHub marketplace není potřeba. Pro distribuci jej lze přiložit k vydání na GitHub Releases. Při vydání změň verzi ve všech třech manifestech; cache instalovaných pluginů je vázána na verzi. Před vydáním znovu proveď testy odpovědí uvedené v návodu.

# Vydání a ověření skillu

## Stav

Repozitář obsahuje jeden samostatný skill pro ChatGPT a Claude, bez plugin manifestů a marketplace. Pravidla FAČR 2024 a Soutěžní řád označený účinností od 26. 6. 2026, jejich přepisy, PNG obrázky a původní PDF mají jednu kanonickou sadu v `skills/football-rules-cz/references/`. Nejde o oficiální produkt FAČR a Pravidla fotbalu nezahrnují změny z let 2025 a 2026. Soutěžní řád má vlastní vydání a účinnost.

Autor projektu potvrdil 20. 9. 2026 následující postupy:

- **ChatGPT:** nahrání skill ZIPu přes [webovou stránku Plugins](https://chatgpt.com/plugins) → Skills → + → Upload from your computer a následnou funkčnost v desktopové aplikaci i na Androidu pod stejným účtem.
- **Claude:** nahrání stejného ZIPu přes [webovou stránku Skills](https://claude.ai/customize/skills) → Add → Upload skill a následnou funkčnost v desktopové aplikaci pod stejným účtem. **Aplikace Claude na Androidu nahraný skill nepoužívá.**

V obou desktopových aplikacích stačí instalace přes web; další instalace v aplikaci není potřeba. [Návod se screenshoty](../README.md#instalace-skillu) zachycuje oba postupy. Jde o výsledky autorových testů; iOS zatím nebyl otestován.

Potvrzená instalace neznamená ověření všech odpovědí. Níže uvedené scénáře zůstávají neprovedené, dokud nejsou zaznamenány jejich skutečné výsledky. Nová pravidla pro přílohy a citace je potřeba ověřit po nahrání nově sestavené verze; dřívější ruční import se s GitHubem sám neaktualizuje.

## Vytvoření veřejného vydání

1. Po sloučení změn zvol číslo vydání, například `0.2.1`.
2. Z vydávaného commitu spusť `python scripts/build_skill.py --check` a `python scripts/build_skill.py --version 0.2.1`. Sestavení vyžaduje explicitní verzi; skript ji neodvozuje z Gitu.
3. Vytvoř GitHub Release pro tentýž commit s odpovídajícím tagem, v tomto příkladu `v0.2.1`. Přilož vygenerovaný ZIP a `SHA256SUMS.txt` ze složky `dist/`. Číslo tagu a parametr sestavení musí souhlasit.
4. V poznámkách uveď vydání pravidel, změny skillu a skutečně provedené testy. Uživatelé stahují přílohu vydání, nikoli automatický archiv Source code.

ZIP obsahuje `football-rules-cz/SKILL.md`, metadata skillu a reference. Neobsahuje marketplace, plugin manifesty, screenshoty instalačního návodu ani balicí skript. Generované soubory se necommitují. Distribuce probíhá veřejným stažením a ručním importem; nevyžaduje sdílení autorova účtu ani publikaci do katalogu pluginů.

## Test po nahrání

Začni nový chat s nahraným skillem. Zaznamenej datum, aplikaci a verzi, model, dotaz, odpověď a funkčnost příloh či odkazů.

- Každá odpověď podle přiložených Pravidel fotbalu, včetně navazující a upřesňující otázky, musí začínat upozorněním na pravidla FAČR 2024 uvedeným ve `SKILL.md`. Odpovědi pouze podle Soutěžního řádu používají vlastní úvod a údaj o ověřené účinnosti podle `references/competition-regulations.md`.
- Zkus „Ukaž mi původní PDF na straně 162.“ Je-li dostupný nástroj pro přílohy, odpověď má zpřístupnit přiložené PDF v chatu. Pokud otevře celé PDF bez skoku, musí uvést stránku 162 zvlášť; tištěná strana je 160.
- Každý podstatný závěr musí obsahovat číslo a název pravidla i konkrétní oddíl nebo bod výkladu, nikoli jen odkaz a stránku. U přímého vhazování očekávej „Pravidlo 11 – Ofsajd, oddíl 3 – Není ofsajd; tištěná strana 93, PDF strana 95.“ Číslo oddílu se nesmí zaměnit za odlišně číslovaný bod výkladu.
- Odkaz označený jako PDF nesmí směřovat na `rules.md`. Odkaz na textový přepis musí být takto pojmenován.
- Pokud aplikace neumí zpřístupnit soubor, odpověď nesmí vymyslet přílohu nebo interní adresu. Může uvést jasně označený externí odkaz na správný typ souboru.
- U textové otázky neotevírat obrázky pro vizuální analýzu jen kvůli jejich přítomnosti v balíčku. Kopírování souboru jako přílohy nevyžaduje jeho vizuální analýzu.
- U každého pravidla použitého pro odpověď musí skill přečíst celou část „VÝKLAD K PRAVIDLU“, včetně všech podčástí pravidla 12. Nestačí první odpovídající bod výkladu. Pokud již není celý výklad v aktuálním kontextu, musí jej načíst znovu; nemožnost načtení přiznat.
- Před závěrem musí skill zkontrolovat relevantní souvislosti a výjimky i mimo první nalezenou pasáž. V odpovědi citovat ustanovení, která závěr mění; nejde jen o přidání obecné věty, že výjimky mohou existovat.
- Při dotazu na současná pravidla musí odpověď přiznat stáří přiloženého vydání.

## Scénáře odpovědí

Očekávání nejsou výsledky již provedeného testu modelu.

| Typ | Dotaz | Očekávání |
| --- | --- | --- |
| Pozitivní | Může být hráč v ofsajdu přímo z vhazování? | Ne při přímém obdržení míče z vhazování; pravidlo 11, oddíl 3, tištěná strana 93 / PDF 95. |
| Pozitivní | Co se podle vydání 2024 stane, když brankář ve vlastním pokutovém území drží míč v rukou 7 sekund? | Nepřímý volný kop; pravidlo 12, oddíl 2, tištěná strana 108 / PDF 110. Závěr výslovně omezit na rok 2024. |
| Pozitivní | Útočník stojí v ofsajdové pozici, ale nehraje míčem ani neovlivňuje soupeře. Je to automaticky přestupek? | Samotná pozice nestačí; vysvětlit aktivní zapojení podle pravidla 11 a citovat PDF 94–95. |
| Pozitivní | A co když míč dostane přímo z rohu? | Navazující otázka k prvnímu scénáři: přímé obdržení míče z kopu z rohu není ofsajd; citovat pravidlo 11, oddíl 3, PDF 95. |
| Pozitivní | Otevři diagramy ofsajdu na PDF straně 101 a vysvětli první situaci. | Skutečně otevřít references/assets/pdf-101.png, přečíst popisky a porovnat s pravidlem 11. Přednostně zpřístupnit obrázek v chatu; pokud to aplikace neumí, použít označený externí odkaz. Pokud obrázek nelze prohlédnout, přiznat omezení. |
| Negativní | Kdo včera vyhrál ligový zápas? | Neaktivovat pravidlový skill jako zdroj výsledků; nevymýšlet výsledek z pravidel. |
| Negativní | Vysvětli touchdown v americkém fotbalu. | Nepoužít pravidla asociačního fotbalu jako zdroj pro americký fotbal. |
| Negativní | Kolik faulů dovolují pravidla futsalu? | Neprezentovat tento balíček jako futsalová pravidla. |
| Hranice | Jaké je aktuální pravidlo pro držení míče brankářem v roce 2026? | Přiznat stáří balíčku; současné znění ověřit zvlášť v aktuálním oficiálním zdroji, nebo říci, že ho nelze z balíčku určit. |
| Hranice | Hráč hrál rukou. Je za to červená? | Vyžádat rozhodující okolnosti nebo rozlišit varianty; žádný automatický kategorický závěr. |

### Kontrola výjimek

Tyto scénáře jsou připravené pro ruční ověření, nikoli již provedené testy:

- „Útočník v ofsajdové pozici obdržel míč přímo z vhazování. Má se pískat ofsajd?“ Odpověď musí zohlednit oddíl 3 „Není ofsajd“, nikoli skončit u obecné definice pozice nebo aktivního zapojení.
- „Útočník v ofsajdové pozici získal míč po doteku obránce. Je to ofsajd?“ Odpověď nesmí rozhodnout podle samotného slova „dotek“. Musí rozlišit vědomé hraní, odraz a obranný zákrok, případně se doptat, a citovat související ustanovení pravidla 11.

## Lokální automatické kontroly

Z kořene repozitáře spusť `python -m unittest discover -s tests -v` a `python scripts/build_skill.py --check`. Testy používají pouze standardní knihovnu Pythonu; OCR se neopakuje.

## Rozšíření o Soutěžní řád

Balíček obsahuje PDF, úplný přepis hlavního řádu a sedmi příloh, označené OCR obrazových stran 83–87 a obrázky tabulek a diagramů. Lokální kontrola ověřuje pokrytí všech 87 stran, kontrolní součet PDF, hlavní paragrafy v rozsahu 1–73 včetně § 41a, 41b, 42a a 42b, přílohy, OCR a odkazy; sestavení ověřuje obsah a reprodukovatelnost ZIPu. Tyto kontroly nenahrazují ruční ověření odpovědí modelu ani kontrolu pozdějších novel na FAČR.

Následující scénáře jsou připravené pro ruční ověření a nejsou zaznamenanými výsledky:

| Dotaz / podmínka | Očekávání |
| --- | --- |
| „Na co odkazuje § 71 při podání protestu?“ | Přečíst § 71 – Protest, PDF/tištěná strana 50; uvést Procesní řád a neodvozovat z tohoto ustanovení lhůtu nebo poplatek. |
| Webové nástroje vypnuté | Odpovídat z přiloženého přepisu a PDF; nevyžadovat internet nebo nové nahrání dokumentu pro běžnou otázku. |
| „Platilo vše již 26. 6. 2026?“ | Zohlednit § 73 odst. 3, PDF 52 a v něm uvedené účinnosti novel 1. 7. 2026; neodvozovat účinnost každého ustanovení z titulku. |
| „Jaký je soutěžní důsledek rozhodnutí rozhodčího?“ | Oddělit herní rozhodnutí podle Pravidel fotbalu od administrativního důsledku podle Soutěžního řádu; načíst oba zdroje a případně vyžádat rozpis soutěže. |
| „Co říká § 1?“ | Zjistit, zda jde o hlavní řád nebo některou přílohu, pokud to kontext neurčuje; citace musí rozlišit vlastní číslování příloh. |
| „Vysvětli příčný spád podle diagramu na straně 85.“ | Otevřít `assets/soutezni-rad-pdf-085.png`, ověřit popisky a vztahy; neodhadovat diagram pouze z OCR. |
| „Ukaž mi Soutěžní řád na straně 50.“ | Zpřístupnit správné přiložené PDF podle možností aplikace, uvést stránku 50; nepoužít PDF Pravidel fotbalu ani posun o dvě strany. |
| Navazující otázka pouze k Soutěžnímu řádu | Použít přesný úvod pro Soutěžní řád; nepřipisovat mu účinnost Pravidel fotbalu 2024. |
| Původní otázka na ofsajd z vhazování | Zachovat původní zdroj, upozornění na vydání 2024 a citaci pravidla 11; nevyžadovat Soutěžní řád pro čistě herní otázku. |

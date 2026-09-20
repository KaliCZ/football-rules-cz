# Vydání a ověření skillu

## Stav

Repozitář obsahuje jeden samostatný skill pro ChatGPT a Claude, bez plugin manifestů a marketplace. Pravidla FAČR 2024, 36 PNG obrázků a původní PDF mají jednu kanonickou sadu v `skills/football-rules-cz/references/`. Nejde o oficiální produkt FAČR a nejsou zapracovány změny z let 2025 a 2026.

Autor projektu potvrdil 20. 9. 2026 nahrání skill ZIPu v ChatGPT přes Settings → Plugins → Browse plugins → Skills → + → Upload from your computer a následnou dostupnost v Android aplikaci. [Návod se screenshoty](../README.md#instalace-skillu) tento postup zachycuje. Nahrání do Claude a dostupnost na jeho Android aplikaci zatím čekají na potvrzení.

Potvrzená instalace neznamená ověření všech odpovědí. Níže uvedené scénáře zůstávají neprovedené, dokud nejsou zaznamenány jejich skutečné výsledky. Nová pravidla pro přílohy a citace je potřeba ověřit po nahrání nově sestavené verze; dřívější ruční import se s GitHubem sám neaktualizuje.

## Vytvoření veřejného vydání

1. Nastav číslo vydání v `VERSION`.
2. Z kořene repozitáře spusť `python scripts/build_skill.py --check` a `python scripts/build_skill.py`.
3. Po sloučení změn vytvoř GitHub Release z příslušného commitu. Přilož vygenerovaný `football-rules-cz-skill-` ZIP s číslem verze a `SHA256SUMS.txt` ze složky `dist/`.
4. V poznámkách uveď vydání pravidel, změny skillu a skutečně provedené testy. Uživatelé stahují přílohu vydání, nikoli automatický archiv Source code.

ZIP obsahuje `football-rules-cz/SKILL.md`, metadata skillu a reference. Neobsahuje marketplace, plugin manifesty, screenshoty instalačního návodu ani balicí skript. Generované soubory se necommitují. Distribuce probíhá veřejným stažením a ručním importem; nevyžaduje sdílení autorova účtu ani publikaci do katalogu pluginů.

## Test po nahrání

Začni nový chat s nahraným skillem. Zaznamenej datum, aplikaci a verzi, model, dotaz, odpověď a funkčnost příloh či odkazů.

- Každá odpověď, včetně navazující a upřesňující otázky, musí začínat upozorněním na pravidla FAČR 2024 uvedeným ve `SKILL.md`.
- Zkus „Ukaž mi původní PDF na straně 162.“ Je-li dostupný nástroj pro přílohy, odpověď má zpřístupnit přiložené PDF v chatu. Pokud otevře celé PDF bez skoku, musí uvést stránku 162 zvlášť; tištěná strana je 160.
- Každý podstatný závěr musí obsahovat číslo a název pravidla i konkrétní oddíl nebo bod výkladu, nikoli jen odkaz a stránku. U přímého vhazování očekávej „Pravidlo 11 – Ofsajd, oddíl 3 – Není ofsajd; tištěná strana 93, PDF strana 95.“ Číslo oddílu se nesmí zaměnit za odlišně číslovaný bod výkladu.
- Odkaz označený jako PDF nesmí směřovat na `rules.md`. Odkaz na textový přepis musí být takto pojmenován.
- Pokud aplikace neumí zpřístupnit soubor, odpověď nesmí vymyslet přílohu nebo interní adresu. Může uvést jasně označený externí odkaz na správný typ souboru.
- U textové otázky neotevírat obrázky pro vizuální analýzu jen kvůli jejich přítomnosti v balíčku. Kopírování souboru jako přílohy nevyžaduje jeho vizuální analýzu.
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

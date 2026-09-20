# Publikace a ověření na telefonu

## Stav verze 0.1.2

Balíček obsahuje jeden skill, pravidla FAČR 2024, 36 PNG obrázků a původní PDF. Neobsahuje MCP, instalační hooky ani spustitelný kód. Nejde o oficiální plugin FAČR. Text nezahrnuje změny z let 2025 a 2026.

Struktura a obsah balíčku jsou kontrolovatelné příkazem `python scripts/build_plugin.py --check`. Úspěšná instalace do lokálního Codexu není testem chování modelu ani dostupnosti na telefonu.

## Zveřejnění pro mobilní katalog

Podle [návodu OpenAI](https://developers.openai.com/plugins/deploy/submission) lze odeslat **Skills only** plugin bez serveru. Veřejné zveřejnění vyžaduje schválení OpenAI a následné publikování vlastníkem. Repozitář není automaticky importován do veřejného katalogu.

1. Vlastník se přihlásí do plugin submission portálu odkazovaného v návodu OpenAI a vybere ověřenou identitu vývojáře. Potřebuje oprávnění Apps Management Write.
2. Vytvoří návrh typu Skills only. Metadata jsou v [plugin.json](../plugins/football-rules-cz/plugin.json), balíček v [ZIP](../dist/football-rules-cz.zip). Pokud formulář požaduje samotný skill, použije složku `skills/football-rules-cz` z balíčku podle jeho aktuálních pokynů.
3. Doplní skutečné údaje vydavatele, logo, podporu, zásady ochrany soukromí, podmínky použití a země dostupnosti. Tyto právní a identifikační údaje nejsou tímto repozitářem nahrazeny ani potvrzeny.
4. Provede níže uvedené scénáře v nové relaci s nainstalovaným pluginem a přiloží skutečné výsledky. Nesplněné scénáře opraví před odesláním.
5. Odešle návrh ke schválení a po schválení jej publikuje. Odkaz na veřejnou položku potom přidá do README.

Plugin nemá vlastní službu, přihlášení ani telemetrii. Otázku zpracovává hostitelská AI aplikace podle svých podmínek. Součástí balíčku jsou materiály třetích stran; prohlášení požadovaná publikačním formulářem musí potvrdit vlastník, ne balicí skript.

## Test na Androidu / iOS

Po zpřístupnění položky v katalogu:

1. Nainstaluj **Pravidla fotbalu 2024 (CZ)** a začni nový chat.
2. Vyber plugin přes `@`, pokud to aplikace nabízí. Jinak výslovně napiš, že jej má použít.
3. Ověř první dvě otázky z tabulky. Každá odpověď musí začínat větou „Tato odpověď vychází z pravidel fotbalu FAČR z roku 2024, platných od 1. 7. 2024; pozdější změny nejsou v přiloženém vydání zahrnuty.“ Ověř to i u navazující odpovědi a upřesňující otázky. Odpověď musí být česky a nabídnout funkční odkaz na konkrétní pravidlo, pokud z něj vyvozuje závěr.
4. Otevři citaci i diagram z pátého scénáře. Nesmí to být nedostupná lokální cesta na počítač autora.
5. Ověř dotaz na aktuální pravidla. Odpověď nesmí vydávat staré vydání za současné.

Zaznamenej datum, aplikaci a její verzi, použitý model, přesný dotaz, odpověď, funkčnost citace a výsledek. Nepovažuj pouhé správné uhádnutí odpovědi za důkaz načtení balíčku.

## Scénáře odpovědí

Níže jsou očekávání, nikoli tvrzení o již provedeném testu modelu. U každého scénáře je zatím výsledek **neprovedeno**.

| Typ | Dotaz | Očekávání |
| --- | --- | --- |
| Pozitivní | Může být hráč v ofsajdu přímo z vhazování? | Ne při přímém obdržení míče z vhazování; pravidlo 11, oddíl 3, tištěná strana 93 / PDF 95. |
| Pozitivní | Co se podle vydání 2024 stane, když brankář ve vlastním pokutovém území drží míč v rukou 7 sekund? | Nepřímý volný kop; pravidlo 12, oddíl 2, tištěná strana 108 / PDF 110. Závěr výslovně omezit na rok 2024. |
| Pozitivní | Útočník stojí v ofsajdové pozici, ale nehraje míčem ani neovlivňuje soupeře. Je to automaticky přestupek? | Samotná pozice nestačí; vysvětlit aktivní zapojení podle pravidla 11 a citovat PDF 94–95. |
| Pozitivní | A co když míč dostane přímo z rohu? | Navazující otázka k prvnímu scénáři: přímé obdržení míče z kopu z rohu není ofsajd; citovat pravidlo 11, oddíl 3, PDF 95. |
| Pozitivní | Otevři diagramy ofsajdu na PDF straně 101 a vysvětli první situaci. | Skutečně otevřít references/assets/pdf-101.png, přečíst popisky a porovnat s pravidlem 11. Poskytnout funkční veřejný odkaz. Pokud obrázek nelze prohlédnout, přiznat omezení. |
| Negativní | Kdo včera vyhrál ligový zápas? | Neaktivovat pravidlový skill jako zdroj výsledků; nevymýšlet výsledek z pravidel. |
| Negativní | Vysvětli touchdown v americkém fotbalu. | Nepoužít pravidla asociačního fotbalu jako zdroj pro americký fotbal. |
| Negativní | Kolik faulů dovolují pravidla futsalu? | Neprezentovat tento balíček jako futsalová pravidla. |
| Hranice | Jaké je aktuální pravidlo pro držení míče brankářem v roce 2026? | Přiznat stáří balíčku; současné znění ověřit zvlášť v aktuálním oficiálním zdroji, nebo říci, že ho nelze z balíčku určit. |
| Hranice | Hráč hrál rukou. Je za to červená? | Vyžádat rozhodující okolnosti nebo rozlišit varianty; žádný automatický kategorický závěr. |

## Kontrola při vydání

- `--check` musí projít, kopie pravidel a obrazových souborů musí přesně souhlasit se zdrojem.
- ZIP musí být samostatný: všechny relativní odkazy vedou dovnitř balíčku a soubory nespoléhají na původní checkout.
- Nainstalovat novou verzi, spustit novou relaci a zopakovat scénáře. Výsledky modelu a mobilní aplikace se zapisují až po skutečném provedení.

## Ověření Claude

Claude Code používá veřejný GitHub marketplace z README. V aplikaci Claude lze přidat repozitář nebo nahrát distribuční ZIP tam, kde je příslušná nabídka dostupná. Tyto cesty nevyžadují sdílení autorova účtu či workspace a neznamenají zveřejnění ve vestavěném katalogu Anthropic.

Z kořene repozitáře s nainstalovaným Claude Code lze ověřit oba manifesty:

```sh
claude plugin validate .claude-plugin/marketplace.json --strict
claude plugin validate plugins/football-rules-cz --strict
```

Po instalaci otevři novou relaci a proveď stejné scénáře výše přes `/football-rules-cz:football-rules-cz`. U testu zapiš, zda šlo o Claude Code, web, Desktop nebo mobil. Kontrola manifestů nenahrazuje test odpovědí modelu a lokální instalace nedokládá synchronizaci na telefon.

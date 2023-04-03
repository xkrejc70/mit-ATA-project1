# Dokumentace testů

## CEG

Výsledný graf přı́čin a důsledků vytvořen v online nástroji [ceg.testos.org](http://ceg.testos.org/).

![CEG](/ceg.png)

### Rozhodovací tabulka

Rozhodovací tabulka pokrývající veškeré příčiny i důsledky.

![Rozhodovací tabulka](/rozhodovaci_tabulka.png)

## Vstupní parametry

Vezmes popis riadenia voziku v tovarni vytiahnes z toho vstupne parametre, napr. vozik ma sloty 1,2 ... nosnost 50,150 ... a specifikujes tomu rozne obmedzenia napr. nosnost.50 -> !sloty.1, no cca tak nejak

počet požadavků. To je nepřímý vstupní parametr. Tímto vytvoříš i kombinace, kde bude více přesunů materiálu

| název | popis |
|---|---|
| pocet_pozadavku | Počet požadavků o převozu materiálu |
| voz_pocet_slotu | Počet slotů vozíku (1 až 4) |
| voz_max_nosnost | Maximální nosnost vozíku (3 druhy) |
| max_vaha_pozadavku | Maximální váha materiálů ze všech požadavků |
| cas_vytvoreni_pozadavku | Čas vytvoření požadavku |
| prum_delka_trasy | Průměrná délka trasy mezi zdrojovou a cílovou stanicí (počet přechodů) |

## Charakteristiky parametrů a definice jejich bloků

| pocet_pozadavku | Počet požadavků o převozu materiálu |
|---|---|
| 1 | Celkový počet požadavků je roven 1 |
| 2 | Celkový počet požadavků je roven 2 |
| 3 | Celkový počet požadavků je větší než  2 |

| voz_pocet_slotu | Počet slotů vozíku (1 až 4) |
|---|---|
| 1 | Počet slotů vozíku je roven 1 |
| 2 | Počet slotů vozíku je roven 2 |
| 3 | Počet slotů vozíku je roven 3 |
| 4 | Počet slotů vozíku je roven 4 |

| pocet_pozadavku |  |
|---|---|
| 1 |  |
| 2 |  |
| 3 |  |

| pocet_pozadavku |  |
|---|---|
| 1 |  |
| 2 |  |
| 3 |  |

| pocet_pozadavku |  |
|---|---|
| 1 |  |
| 2 |  |
| 3 |  |

| pocet_pozadavku |  |
|---|---|
| 1 |  |
| 2 |  |
| 3 |  |

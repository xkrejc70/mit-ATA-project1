# Dokumentace testů

## CEG

Výsledný graf přı́čin a důsledků vytvořen v online nástroji [ceg.testos.org](http://ceg.testos.org/).

![CEG](/ceg.png)

### Rozhodovací tabulka

Rozhodovací tabulka pokrývající veškeré příčiny i důsledky.

![Rozhodovací tabulka](/rozhodovaci_tabulka.png)

## Vstupní parametry

Zde jsou popsány některé vstupní parametry.

| název | popis |
|---|---|
| pocet_pozadavku | Počet požadavků o převozu materiálu |
| voz_pocet_slotu | Počet slotů vozíku (1 až 4) |
| voz_max_nosnost | Maximální nosnost vozíku (50, 150 a 500 kg) |
| poz_max_vaha | Maximální váha materiálů ze všech požadavků |
| poz_cas_vytvoreni | Čas vytvoření požadavku |
| prum_delka_trasy | Průměrná délka trasy mezi zdrojovou a cílovou stanicí (počet přechodů) |

## Charakteristiky parametrů a definice jejich bloků

Vstupním parametrům jsou definovány bloky.

| pocet_pozadavku | Počet požadavků o převozu materiálu |
|---|---|
| 1 | Celkový počet požadavků je 1 až 2 |
| 2 | Celkový počet požadavků je 2 až 5 |
| 3 | Celkový počet požadavků je > 5 |

| voz_pocet_slotu | Počet slotů vozíku (1 až 4) |
|---|---|
| 1 | Počet slotů vozíku je 1 |
| 2 | Počet slotů vozíku je 2 |
| 3 | Počet slotů vozíku je 3 až 4 |

| voz_max_nosnost | Maximální nosnost vozíku (50, 150 a 500 kg) |
|---|---|
| 1 | Maximální nosnost vozíku je 50 kg |
| 2 | Maximální nosnost vozíku je 150 kg |
| 3 | Maximální nosnost vozíku je 500 kg |

| poz_max_vaha | Maximální váha materiálů ze všech požadavků |
|---|---|
| 1 | Maximální váha materiálů ze všech požadavků je <= daná kapacita vozíku |
| 2 | Maximální váha materiálů ze všech požadavků je > daná kapacita vozíku |

| poz_cas_vytvoreni | Čas vytvoření požadavku |
|---|---|
| 1 | Požadavky jsou vytvořeny maximálně po 20s |
| 2 | Požadavky jsou vytvořeny minikálně po 20s |

| prum_delka_trasy | Průměrná délka trasy mezi zdrojovou a cílovou stanicí (počet přechodů) |
|---|---|
| 1 | Průměrná délka trasy je <= 2 |
| 2 | Průměrná délka trasy je > 2 |

### Omezení mezi bloky

Zde jsou sepsány všechny závilosti jednotlivých bloků charakteristik

## Kombinace 

Kombinace dvojic charakteristik definovaných výše byly vytvořeny v online nástroji [combine.testos.org](https://combine.testos.org/).

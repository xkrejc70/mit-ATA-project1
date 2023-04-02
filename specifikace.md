Pokud je požadováno přemístění nákladu z jednoho místa do druhého, vozík si materiál vyzvedne do 1 minuty.

- AMB_SUBJECT, není zřejmé kdo požaduje přemístění (řídící systém? pacovníci? vozík?).
- AMB_STATEMENT, je zde použit alias místo, který odkazuje na stanici.
- AMB_STATEMENT, je zde použit alias náklad, který odkazuje na materiál.
- IMPLICIT, není zřejmé jaká akce nastane po vyzvednutí materiálu.
- IMPLICIT, není zřejmé co znamené "vyzvedne".
- AMB_TEMPORAL, není zřejmé od kdy se interval 1 minuty počítá.

*Pokud je řídícím systémem (dále jen systém) požadován převoz materiálu ze zdrojové do cílové stanice, vozík přijede do zdrojové stanice a materiál, který je definován v požadavku, si naloží. Příjezd i nakládka proběhne do 1 minuty od doby, kdy byl systémem podán požadavek.*

Pokud se to nestihne, materiálu se nastavuje prioritní vlastnost.

- AMB_REFERENCE, nejednoznačná reference "to" odkazující na akci z předchozí věty.
- IMPLICIT, není zřejmé kdo nastavuje vlastnost (řídící systém? vozík?).

*Pokud není materiál do příslušného vozíku naložen do 1 minuty od vznesení požadavku, systém nastaví danému materiálu prioritní vlastnost.*

Každý prioritní materiál musí být vyzvednutý vozíkem do 1 minuty od nastavení prioritního požadavku.

- AMB_STATEMENT, není zřejmé zda-li prioritní materiál je materiál s prioritní vlastností.
- DANGLING_ELSE, není zřejmé co se stane pokud je časový limit překročen.
- AMB_REFERENCE, není vysvětleno co je to prioritní požadavek.

*Jakmile je materiál označen prioritní vlastností, systém vznese prioritní požadavek na jeho vyzvednutí. Tento materiál musí být vyzvednutý vozíkem do 1 minuty od nastavení prioritního požadavku. Pokud tento časový interval není dodržen, je daný požadavek zrušen*

Pokud vozík nakládá prioritní materiál, přepíná se do režimu pouze-vykládka.

- AMB_TEMPORAL, není zřejmé kdy přesně se přepne do režimu pouze-vykládka.
- AMB_STATEMENT, není zřejmé zda-li prioritní materiál je materiál s prioritní vlastností
- DANGLING_ELSE, není explicitně napsáno co se děje v případě, že je naložen materiál, který není v režimu pouze-vykládka.
- IMPLICIT, režim pouze-vykládka není explicitně definován.

*Jakmile vozík naloží materiál s prioritní vlastností, přepíná se do režimu pouze-vykládka. V tomto režimu vozík nesmí nabírat další materiál. Jakmile vozík naloží materiál bez prioritní vlastnosti, zůstává ve svém stávajícím režimu. Druhý režim je popsán dále v textu.*

V tomto režimu zůstává, dokud nevyloží všechen takový materiál.

- UNSPECIFIED_SUBJECT, není zřejmé kdo zůstává.
- OMISSION, není zde explicitně napsáno co se stane po vyložení materiálu.
- AMB_STATEMENT, není zřejmé jaký materiál.

*V režimu pouze-vykládka vozík zůstává, dokud nevyloží všechen materiál s prioritní vlastností. Jakmile jej vyloží přepne se zpět do režimu normálka.*

Normálně vozík během své jízdy může nabírat a vykládat další materiály v jiných zastávkách.

- IMPLICIT, normální režim není explicitně definován.
- AMB_STATEMENT, je zde použit alias nabírat, který odkazuje na nakládat
- AMB_STATEMENT, je zde použit alias zastávka, který odkazuje na stanici
- AMB_STATEMENT, není jasně definováno jaké "jiné" zastávky, zastávky jsou určeny požadavkem.
- AMB_STATEMENT, není zřejmé, zda může vozík libovoně jezdit či se řídí požadavky systému.

*Pokud je vozík v režimu normálka, může být na vozík během jeho jízdy systémem vzneses další požadavek o přesunu materiálu. Na základě požadavku může vozík v režimu normálka nakládat a vykládat další materiály v daných stanicích.*

Na jednom místě může vozík akceptovat nebo vyložit jeden i více materiálů.

- AMB_STATEMENT, je zde použit alias místo, který odkazuje na stanici.
- AMB_STATEMENT, je zde použit alias akceptovat, který odkazuje na nakládat.
- AMB_LOGIC, nesprávné použití logické spojky "nebo".

*V jedné stanici může vozík nakládat i vykládat, a to i více materiálů.*

Pořadí vyzvednutí materiálů nesouvisí s pořadím vytváření požadavků.

- AMB_STATEMENT, pořadí vyzvednutí materiálů může souviset s pořadím vytváření požadavků.
- AMB_STATEMENT, není zřejmé kdo vyzvedne materiály.
- AMB_STATEMENT, není zřejmé o jaký požadavek se jedná.
- AMB_STATEMENT, je zde použit alias vyzvednout, který odkazuje na nakládat.

*Pořadí nakládání materiálů vozíky nemusí být stejné jako pořadím vytváření požadavků o přesunu materiálu.*

Vozík neakceptuje materiál, pokud jsou všechny jeho sloty obsazené nebo by jeho převzetím byla překročena maximální nosnost.

- AMB_STATEMENT, jsou zde použity aliasy akceptovat a převzít, které odkazují na nakládat.
- UNSPECIFIED_SUBJECT, není vysvětleno, co jsou to sloty vozíku a jakou maximální hmotnost vozík má.
- AMB_LOGIC, dvojitá negace

*Vozík může nakládat materiál, pouze pokud je alespoň jeden jeho slot volný a naložením materiálu by nebyla překročena maximální nosnost. Vozík má pro převoz materiálu celkem 1 až 4 sloty. Vozíky jsou 3 druhů, každý má jinou maximální nosnost: 50 kg, 150 kg a 500 kg. Vozíky s nejmenší nosností mají nejméně 2 sloty, vozíky s největší nosností mají maximálně 2 sloty.*
# Tema 1 - ASC - Marketplace
Bloțiu Mihnea-Andrei - 333CA
21.04.2023

### Organizare - Abordare generală

* Abordarea generală a temei a fost cea de rezolvare a clasicei probleme de programare paralelă și
distribuită și anume "producători-consumatori". În acest caz, producătorii se află în fișierul
product.py și sunt reprezentați de thread-urile care produc elemente de tip ceai și cafea, iar
consumatorii se află în fișierul consumer.py și sunt reprezentați de thread-urile care cumpără
aceste produse însă le pot pune și înapoi în stoc dacă se răzgândesc.

* Tema din punctul meu de vedere este utilă în primul rând pentru a învăța Python mai mult decât
programare paralelă din două motive:
  * Problema producători-consumatori este una clasică și a fost studiată la APD în detaliu atât în
  C cât și în Java, așadar o știam de dinainte.
  * ASC este singura materie de până în anul 3 inclusiv care lucrează măcar parțial cu Python și
  deși există 3 laboratoare în acest sens, informația este extrem de multă în acestea pentru a învăța
  Python mai ales pentru o persoană care nu a mai lucrat cu acest limbaj în trecut (care este și
  cazul meu). Astfel, practic eu am învățat Python în timp ce rezolvam tema și nu neapărat la laborator
  deși l-am folosit de multe ori ca surse de inspirație.

* În ceea ce privește implementarea, consider că implementarea este eficientă, deoarece:
    * Producătorii și consumatorii lucrează complet independent unii față de ceilalți.
    * S-au folosit elemente de sincronizare doar pentru producătorii între ei și pentru
    consumatori între ei și doar acolo unde era strict necesar:
      * Pentru înregistrarea unui nou producător deoarece fiecare trebuia să aibă ID diferit
      și exista posibilitatea ca doi producători să se înregistreze simultan.
      * Pentru înregistrarea unui nou coș de cumpărături din același motiv ca mai sus.
      * Pentru adăugarea unui produs din coadă în coșurile de cumpărături ale consumatorilor
      deoarece exista posibilitatea ca mai mulți consumatori să cumpere același produs în același
      timp deși posibil exista doar unul disponibil
      * Pentru afișarea informației la stdout deoarece exista posibilitatea ca mai multe thread-uri
      să dorească să scrie în același timp și deci scrierea să se intercaleze.

* Cazurile speciale legate de detalii de implementare nespecificate în enunț:
    * Am considerat că există o singură coadă de produse care este accesată de toți producătorii
    și respectiv consumatorii în care fiecare producător are un număr maxim prestabilit de produse
    pe care le poate introduce în coadă.
    * Am considerat că fiecare sublistă din cea de coșuri primită ca input în parametrul „carts” din
    consumer este de fapt un coș de cumpărături diferit chiar dacă există o singură persoană care
    comandă toate acele produse.
    * Am considerat că în cazul în care un producător și-a atins limita maximă de produse, un consumator
    preia un produs al acestui producător, iar producătorul profită de acest moment și mai adaugă un nou
    produs în coadă, iar ulterior consumatorul renunță la produsul cumpărat inițial, acesta să îl poată
    pune înapoi în listă chiar dacă se depășește cu 1 limita maximă de produse a unui producător.

### Implementare

#### Detalii generale:

* Cerința precizată anterior a fost implementată în cele trei fișiere oferite în schelet după cum
urmează:
    * Fișierul product.py conține implementarea producătorilor.
    * Fișierul consumer.py conține implementarea consumatorilor.
    * Fișierul marketplace.py conține implementarea marketplace-ului.

* Producătorii:
    * Primesc ca parametru în constructor un marketplace, timpul de așteptare necesar după adăugarea
    a oricărui produs în coadă și lista de produse pe care aceștia le pot produce.
    * Își generează tot în constructor propriul id de producător.
    * În metoda run, paralel de alți producător, aceștia își extrag informațiile necesare despre produse
    din lista precizată anterior și anume: numele produsului în sine, cantitatea produsă și timpul necesar
    de așteptare în cazul în care a ajuns la limita maximă de produse.
    * Pentru fiecare astfel de tuplu de informații se încearcă producerea a respectivei cantități din acel
    produs, iar dacă nu se poate, se așteaptă timpul necesar de așteptare și se încearcă din nou. Prin
    producerea unui produs se înțelege adăugarea acestuia în coada de produse a marketplace-ului.
* Consumatorii:
    * Primesc ca parametru în constructor un marketplace, timpul de așteptare necesar în cazul în care
    doresc să cumpere un produs dar acesta nu este disponibil în coada de produse a marketplace-ului și
    lista de coșuri de cumpărături.
    * Își generează tot în constructor propriul id de coș de cumpărături care va fi reinițializat pentru
    fiecare coș din lista de coșuri de cumpărături.
    * În metoda run, paralel de alți consumatori, aceștia își extrag informațiile necesare despre produsele
    pe care doresc să le achiziționeze/pună înapoi în coadă de produse a marketplace-ului și anume: tipul
    acțiunii, cantiatea de produse dorită și timpul necesar de așteptare în cazul în care nu există un astfel
    de produs la o asemenea cantitate.
    * Pentru fiecare astfel de tuplu de informații, în funcție de acțiunea dorită, se încearcă adăugarea în
    coș a respectivului produs, iar dacă nu se poate, se așteaptă timpul necesar de așteptare și se încearcă.
    Dacă se dorește eleminarea unui produs din coș, acesta este pus înapoi în coada de produse a marketplace-ului.
    * La finalul ficărui coș de cumpărături, se afișează informațiile despre acesta.
* Marketplace:
    * Primeste ca parametru în constructor un număr maxim de produse pe care un producător îl poate produce și își
    inițializează următoarele atribute:
        * coada de produse (este o listă de tupluri de forma (produs, producător))
        * dicționarul de producători (este un dicționar de tipul (id_producător: câte produse mai poate produce))
        * dicționarul de coșuri (este un dicționar de tipul (id_coș: lista de tupluri de forma (produs, producător))
        * logger-ul folosit pentru crearea fișierului marketplace.log
    * Logica cu care un producător lucrează cu marketplace-ul este următoarea:
        * Se înregistrează la marketplace. Această acțiune este sincronizată pentru a nu exista posibilitatea c doi
        producători să își creeze același id.
        * În cazul în care dorește să publice un produs în marketplace, acesta verifică în dicționarul de producători
        dacă mai are voie să producă produse și dacă da, își adaugă produsul în coada de produse și scade din numărul
        de produse pe care îl mai poate produce. În cazul în care nu mai are voie să producă produse, acesta primește
        un răspuns negativ și mai așteaptă.
    * Logica cu care un consumator lucrează cu marketplace-ul este următoarea:
        * Își crează un id de coș de cumpărături. Această acțiune este sincronizată pentru a nu exista posibilitatea
        de a exista două coșuri de cumpărături cu același id.
        * În cazul în care dorește să cumpere un produs, acesta verifică dacă există un astfel de produs în coada de
        produse a marketplace-ului și dacă da, îl adaugă în coșul său de cumpărături și îl elimină din coada de produse
        a marketplace-ului. De asmenea semnalizează producătorul asociat produsului pe care l-a cumpărat că numărul său
        de produse din coada de produse a scăzut deci, mai poate produce altele. În cazul în care nu există un astfel
        de produs, acesta primește un răspuns negativ și mai așteaptă. Această acțiune este sincronizată pentru a nu
        exista posibilitatea ca doi consumatori să cumpere același produs în același timp.
        * În cazul în care dorește să pună înapoi în coada de produse a marketplace-ului un produs, aceasta îl elimină
        din coșul său de cumpărături și îl adaugă în coada de produse a marketplace-ului. De asemenea semnalizează
        producătorul asociat produsului pe care l-a pus înapoi în coada de produse că numărul său de produse din coada
        a crescut (deci posibil să nu mai poată produce altele noi).
        * La finalul coșului de cumpărături, când dorește să plaseze o comandă acesta primește din partea marketplace-ului
        lista sa de cumpărături pe care o afișează la stdout și își reinițializează coșul de cumpărături pentru o eventuală
        nouă sesiune.

#### Lucruri interesante descoperite pe parcurs

* Faptul că Python știe să facă pattern matching pe elementele unei liste de tupluri, de exemplu:

    ```python
    if (product, producer) in self.products_queue:
        self.products_queue.remove((product, producer))
    ```
* Mai mult decât atât poate să utilizeze _ pentru a ignora un element din tuplu pe care nu îl
folosim ulterior în cod, de exemplu:

    ```python
    if (product, _) in self.products_queue:
        self.products_queue.remove((product, _))
    ```

### Resurse utilizate
1. Pentru a învăța de la 0 Python, am folosit destul de mult laboratoarele de la ASC cu precădere
primele două:
   1. https://ocw.cs.pub.ro/courses/asc/laboratoare/01 - Laboratorul 1
   2. https://ocw.cs.pub.ro/courses/asc/laboratoare/02 - Laboratorul 2
   3. https://ocw.cs.pub.ro/courses/asc/laboratoare/03 - Laboratorul 3

2. Pentru partea de logging am folosit elementele din documentația furnizată de echipa de ASC:
   1. https://docs.python.org/3/howto/logging.html - Logging HOWTO
   2. https://docs.python.org/3/library/logging.html - Logging objects

3. Pentru partea de pytest și unit testing am folost atât documentația furnizată de echipa de ASC,
cât și laboratorul de unit testing de la IC:
   1. https://docs.python.org/3/library/unittest.html - Unit testing documentation
   2. https://ocw.cs.pub.ro/courses/icalc/laboratoare/laborator-05 - Laborator IC

### Git

* Toate cele menționate anterior au fost versionate pe parcursul dezvoltării temei, la următorul link
de github: https://github.com/mihneablotiu/MarketPlace


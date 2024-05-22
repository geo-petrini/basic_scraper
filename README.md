# Simple Scraper

## amazon.py
Semplice web scraper usato per il modulo 374 Business Analysts.
Effettua l'estrazione dati da una pagina di ricerca su Amazon.it (url hardcoded nella funzione "run")
In autonomia raccoglie i seguenti dati:
- name: Nome del prodotto
- price: Prezzo senza valuta
- stars: Punteggio di valutazione in percentuale (2 cifre significative)
- reviews_count: Numero di recensioni

### Testing limitato
Questo script non ha la pretesa di essere accurato, lo scopo è quello di raccogliere dati senza però curarsi della qualità.

## main.py
Prototipo di web scraper usato per dimostrare come sia possibile estrarre dati da una pagina web statica o generata server-side.
Lo script mostra anche come non sia possibile estrarre i dettagli dei prodotti da pagine che usano caricamenti asincroni (AJAX).



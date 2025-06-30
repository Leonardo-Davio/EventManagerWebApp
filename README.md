# Motorcycle Events Manager

**Motorcycle Events Manager** è una moderna web app pensata per coordinare gli eventi di una community di motociclisti.
Sviluppata in Python con Django e arricchita da Bootstrap per il front-end, l’app sfrutta PostgreSQL come database relazionale.
Il deploy è gestito su Railway, mentre Cloudinary si occupa dell’hosting e della gestione dei media.

---

## Architettura e tecnologie

L’app si basa su un’architettura MVC: Django regola la logica di business e le interazioni con il database PostgreSQL,
mentre Bootstrap 5 garantisce un’interfaccia responsive e accessibile da desktop e mobile. Railway assicura un deploy continuo,
con rollback e monitoring integrati, e Cloudinary consente caricamenti rapidi e sicuri delle immagini degli eventi.

---

## Panoramica delle funzionalità

Ogni sezione dell’app è pensata per offrire un’esperienza semplice e immediata:

- **Home page**: un’hero section introduce il progetto con titolo, slogan e inviti all’azione; subito sotto, 
i prossimi tre eventi in calendario e quelli più popolari per iscrizioni.
- **Calendario eventi**: una vista in lista con filtri per categoria (motoraduni, motogiri, tour enogastronomici, track day)
e per stato delle iscrizioni (aperte, chiuse, non ancora aperte, annullate). È possibile definire un intervallo di date
e ordinare gli eventi per data o numero di partecipanti.
- **Scheda evento**: ogni evento ha un titolo, descrizione estesa, data/ora, location di partenza (con link a Google Maps),
immagine di copertina e, se disponibile, il tracciato GPS. Le iscrizioni si attivano e si chiudono secondo un calendario
prestabilito, e l’organizzatore può cancellare l’evento in qualsiasi momento.
- **Gestione iscrizioni**: solo utenti autenticati possono registrarsi; il profilo prevede l’inserimento obbligatorio
della moto e consente di segnalare il numero di accompagnatori. Le conferme vengono inviate all’indirizzo email registrato.
- **Profilo utente**: riepilogo dei dati personali, della moto e degli eventi a cui si è iscritti, con accesso facilitato
alla modifica dei propri dettagli.

---

## Flusso utente

1. **Registrazione/Login**: l’utente crea un account fornendo email e password, oppure accede se già registrato.
2. **Configurazione profilo**: inserimento obbligatorio dei dati relativi alla moto (marca, modello, cilindrata).
3. **Scoperta eventi**: navigazione nel calendario o ricerca tramite filtri per individuare l’evento di interesse.
4. **Iscrizione**: scelta dell’evento, inserimento del numero di partecipanti e conferma dell’iscrizione nel periodo previsto.


---

> 🌐 Prova subito l’applicazione su Railway:  
> https://web-production-dac68.up.railway.app/

---
## File del progetto

Usare questo link per ottenere i file sorgente, con anche il database popolato ed alcune configurazioni.
> link.com

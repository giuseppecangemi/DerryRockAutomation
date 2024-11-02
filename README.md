# Documentazione del Progetto Derry Rock Pub

## Introduzione

Questo progetto è un'applicazione web realizzata con Flask per la registrazione e la gestione degli utenti del "Derry Rock Pub" a Roma. Gli utenti possono registrarsi compilando un modulo, e gli amministratori possono visualizzare e gestire i dati degli utenti registrati. L'applicazione include funzionalità per l'autenticazione degli utenti e la gestione dei file.

## Struttura del Progetto

Il progetto è composto da diversi file HTML e un file Python (`app.py`) che gestisce la logica dell'applicazione.

### File HTML

1. **form.html**: Modulo di registrazione per i soci del pub, in cui gli utenti possono inserire i propri dati.
2. **login.html**: Modulo di accesso per gli amministratori, che richiede l'inserimento di un PIN per autenticarsi.
3. **view_users.html**: Visualizzazione della lista degli utenti registrati, dove gli amministratori possono vedere tutti i dettagli degli utenti.

### File Python

- **app.py**: Contiene la logica del server Flask, definisce le rotte e gestisce le operazioni sul database.

## Dettagli del Modulo di Registrazione (form.html)

Il modulo di registrazione consente agli utenti di inserire i propri dati personali. I campi presenti nel modulo includono:

- **Nome** e **Cognome**: Dati identificativi dell'utente (richiesti).
- **Email**: Indirizzo email dell'utente (richiesto).
- **Città**: Città di residenza (richiesto).
- **Data di nascita**: Data di nascita, con validazione per il range (richiesta).
- **Residenza**: Indirizzo di residenza (richiesto).
- **Sesso**: Selezione del sesso (richiesto).
- **Numero Carta d'Identità**: Numero della carta d'identità (richiesto).
- **Carica un file**: Opzione per caricare un file (richiesta).
- **Checkbox di consenso**: Presa visione dello statuto e autorizzazione al trattamento dei dati (richiesta).

La validazione della data di nascita include controlli per assicurarsi che l'utente inserisca una data valida compresa tra il 1900 e la data odierna.

## Dettagli del Login (login.html)

Il modulo di login è progettato per gli amministratori e richiede l'inserimento di un PIN. Se il PIN inserito è corretto, l'utente viene reindirizzato alla pagina di visualizzazione degli utenti.

## Visualizzazione degli Utenti (view_users.html)

Questa pagina mostra un elenco di tutti gli utenti registrati, con dettagli quali:

- Nome
- Cognome
- Email
- Città
- Data di Nascita
- Residenza
- Sesso
- Numero Carta d'Identità
- File Caricato
- Stato di Approvazione
- Numero Tessera
- Opzioni per modificare i dettagli dell'utente

## Backend e Database

### Configurazione di Flask

Il file `app.py` contiene la configurazione dell'app Flask, la connessione al database PostgreSQL e la definizione del modello User.

### Modello User

Il modello User definisce la struttura della tabella `users` nel database, comprendente campi come l'identificativo univoco dell'utente, nome, cognome, email, e altri dettagli necessari per la registrazione e gestione degli utenti.

### Rotte Principali

Le rotte principali dell'applicazione comprendono:

- **/**: Mostra il modulo di registrazione.
- **/submit**: Gestisce l'invio del modulo di registrazione e salva i dati nel database.
- **/login**: Gestisce il login degli amministratori.
- **/view_users**: Visualizza la lista degli utenti registrati.

## Generazione del QR Code

Per generare un codice QR per il modulo di registrazione, viene utilizzata la libreria `qrcode`. Questa funzionalità permette di creare un QR code che, quando scansionato, reindirizza gli utenti al modulo di registrazione online. Il QR code viene generato dinamicamente e può essere utilizzato per facilitare l'accesso al modulo da parte degli utenti.

## Invio dell'Email con Allegato

L'applicazione prevede anche l'invio di email automatiche contenenti la tessera associativa come allegato. Questo è utile per garantire che ogni utente riceva la propria tessera dopo la registrazione. Il sistema utilizza le funzionalità di `smtplib` per inviare le email. 

Le email contengono un messaggio che informa il destinatario della presenza di un allegato (la tessera associativa), facilitando la comunicazione tra il pub e i soci.

## Conclusione

Questo progetto combina diversi aspetti dell'automazione per migliorare l'esperienza del cliente e semplificare i processi amministrativi. Per ulteriori informazioni, si prega di consultare la documentazione o contattare il team di sviluppo.

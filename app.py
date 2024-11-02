from flask import Flask, request, render_template, redirect, url_for, session
import os
from sqlalchemy import create_engine, Column, BigInteger, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import send_from_directory

# Configurazione dell'app Flask
app = Flask(__name__)
app.secret_key = 'una_chiave_segreta'  # Cambia con una chiave segreta
app.config['UPLOAD_FOLDER'] = 'uploads'

# Assicurati che la cartella esista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configurazione del database PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')  # Usa la variabile d'ambiente
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Definizione del modello User
class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)  # Lascia gestire l'ID a PostgreSQL
    nome = Column(String)
    cognome = Column(String)
    citta = Column(String)
    data = Column(String)
    residenza = Column(String)
    sesso = Column(String)
    email = Column(String)
    carta_identita = Column(String)
    file = Column(String)
    approvato = Column(String)
    numero_tessera = Column(BigInteger)  # Puoi usare Float per DOUBLE PRECISION
    inviato = Column(String)
    manuale = Column(String)  # Aggiunto il campo manuale



# Crea le tabelle nel database
Base.metadata.create_all(engine)

# Crea una sessione per interagire con il database
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    db_session = Session()  # Sposta la creazione della sessione all'inizio
    try:
        nome = request.form['nome']
        cognome = request.form['cognome']
        citta = request.form['citta']  # Aggiunto
        data = request.form['data']      # Aggiunto
        residenza = request.form['residenza']  # Aggiunto
        sesso = request.form['sesso']          # Aggiunto
        carta_identita = request.form['carta_identita']  # Aggiunto
        email = request.form['email']
        file = request.files.get('file')  # Usa .get per evitare KeyError

        # Controlla se il file è stato caricato
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            new_user = User(
                nome=nome,
                cognome=cognome,
                citta=citta,             # Aggiunto
                data=data,               # Aggiunto
                residenza=residenza,     # Aggiunto
                sesso=sesso,             # Aggiunto
                carta_identita=carta_identita,  # Aggiunto
                email=email,
                file=file.filename,
                approvato="",
                numero_tessera=None,  # Lascia a None se non viene fornito
                inviato=""
            )

            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('index'))
        else:
            return "Nessun file caricato.", 400  # Ritorna errore se il file non è stato caricato
    except Exception as e:
        print("Errore durante l'inserimento:", e)  # Stampa l'errore nei log
        return f"Si è verificato un errore durante l'inserimento dei dati: {e}", 500  # Includi l'errore nel messaggio di risposta
    finally:
        db_session.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pin = request.form['pin']
        if pin == '1234':  # Sostituisci con il tuo PIN
            session['authenticated'] = True  # Imposta la variabile di sessione
            return redirect(url_for('view_users'))
        else:
            return "PIN errato!", 403  # Gestisci l'errore del PIN
    return render_template('login.html')  # Ritorna il template se è un GET

@app.route('/view_users')
def view_users():
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    db_session = Session()
    try:
        # Recupera utenti non approvati
        non_approvati = db_session.query(User).filter(User.approvato != "SI").all()
        
        # Recupera utenti approvati e ordina per cognome
        approvati = db_session.query(User).filter(User.approvato == "SI").order_by(User.cognome).all()
        
        # Combina gli utenti in un'unica lista con non approvati seguiti dagli approvati
        users = non_approvati + approvati

        return render_template('view_users.html', users=users)
    except Exception as e:
        print("Errore nel recupero degli utenti:", e)
        return f"Si è verificato un errore nel recupero degli utenti: {e}", 500
    finally:
        db_session.close()


@app.route('/update_card_number/<int:user_id>', methods=['POST'])
def update_card_number(user_id):
    db_session = Session()
    try:
        user = db_session.query(User).get(user_id)
        if user:
            numero_tessera = request.form['numero_tessera']
            if numero_tessera:
                user.numero_tessera = numero_tessera  # Salva il numero di tessera fornito
            else:
                # Se non è fornito, genera un numero di tessera sequenziale
                max_numero_tessera = db_session.query(User).filter(User.numero_tessera.isnot(None)).order_by(User.numero_tessera.desc()).first()
                if max_numero_tessera:
                    user.numero_tessera = max_numero_tessera.numero_tessera + 1
                else:
                    user.numero_tessera = 1  # Inizia da 1 se non ci sono numeri di tessera
            db_session.commit()
        else:
            return "Utente non trovato.", 404  # Ritorna errore se l'utente non esiste
    except Exception as e:
        print("Errore nell'aggiornamento del numero di tessera:", e)
        return f"Si è verificato un errore nell'aggiornamento del numero di tessera: {e}", 500  # Includi l'errore nel messaggio di risposta
    finally:
        db_session.close()
    return redirect(url_for('view_users'))

@app.route('/update_approval/<int:user_id>', methods=['POST'])
def update_approval(user_id):
    db_session = Session()
    try:
        user = db_session.query(User).get(user_id)
        if user:
            user.approvato = "SI"  # Imposta a "SI" se approvato
            db_session.commit()
        else:
            return "Utente non trovato.", 404  # Ritorna errore se l'utente non esiste
    except Exception as e:
        print("Errore nell'aggiornamento dell'approvazione:", e)
        return f"Si è verificato un errore nell'aggiornamento dell'approvazione: {e}", 500  # Includi l'errore nel messaggio di risposta
    finally:
        db_session.close()
    return redirect(url_for('view_users'))

@app.route('/update_manual/<int:user_id>', methods=['POST'])
def update_manual(user_id):
    db_session = Session()
    try:
        user = db_session.query(User).get(user_id)
        if user:
            user.manuale = request.form['manuale']  # Aggiorna il valore del campo manuale
            db_session.commit()
        else:
            return "Utente non trovato.", 404
    except Exception as e:
        print("Errore nell'aggiornamento del manuale:", e)
        return f"Si è verificato un errore nell'aggiornamento del manuale: {e}", 500
    finally:
        db_session.close()
    return redirect(url_for('view_users'))

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

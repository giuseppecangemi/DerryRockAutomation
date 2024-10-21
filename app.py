from flask import Flask, request, render_template, redirect, url_for, session
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
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
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cognome = Column(String)
    email = Column(String)
    file = Column(String)
    approvato = Column(String)
    numero_tessera = Column(String)
    inviato = Column(String)

# Crea le tabelle nel database
Base.metadata.create_all(engine)

# Crea una sessione per interagire con il database
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        nome = request.form['nome']
        cognome = request.form['cognome']
        email = request.form['email']
        file = request.files['file']

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

        new_user = User(
            nome=nome,
            cognome=cognome,
            email=email,
            file=file.filename,
            approvato="",
            numero_tessera=None,
            inviato=""
        )

        db_session = Session()
        db_session.add(new_user)
        db_session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print("Errore durante l'inserimento:", e)  # Stampa l'errore nei log
        return "Si è verificato un errore durante l'inserimento dei dati.", 500
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

    db_session = Session()  # Usa un nome diverso per la sessione del database
    try:
        users = db_session.query(User).all()
        return render_template('view_users.html', users=users)
    except Exception as e:
        print("Errore nel recupero degli utenti:", e)  # Stampa l'errore nei log
        return "Si è verificato un errore nel recupero degli utenti.", 500
    finally:
        db_session.close()  # Assicurati di chiudere la sessione

@app.route('/update_approval/<int:user_id>', methods=['POST'])
def update_approval(user_id):
    db_session = Session()
    user = db_session.query(User).get(user_id)
    if user:
        user.approvato = "SI"  # Imposta a "SI" se approvato
        db_session.commit()
    db_session.close()
    return redirect(url_for('view_users'))

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

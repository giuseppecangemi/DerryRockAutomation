from flask import Flask, request, render_template, redirect, url_for
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Configurazione dell'app Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Cartella per i file caricati

# Assicurati che la cartella esista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configurazione del database PostgreSQL
DATABASE_URL = os.getenv('postgresql://db_derryrock_user:F3RW728z9Tbhhckj5RwUf2yO3RWCUUnF@dpg-csamt28gph6c73a4ftvg-a.oregon-postgres.render.com/db_derryrock')  # Imposta l'URL del database nel tuo ambiente
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
    nome = request.form['nome']
    cognome = request.form['cognome']
    email = request.form['email']
    file = request.files['file']

    # Salva il file nella cartella uploads
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    # Crea un nuovo oggetto User
    new_user = User(
        nome=nome,
        cognome=cognome,
        email=email,
        file=file.filename,
        approvato="SI",
        numero_tessera=None,
        inviato=""
    )

    # Aggiungi e commit la sessione
    session = Session()
    session.add(new_user)
    session.commit()
    session.close()  # Chiudi la sessione

    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Imposta la porta
    app.run(host='0.0.0.0', port=port, debug=True)

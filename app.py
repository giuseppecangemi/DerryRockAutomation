from flask import Flask, request, render_template, redirect, url_for, session
import os
from dotenv import load_dotenv  
from sqlalchemy import create_engine, Column, BigInteger, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import send_from_directory

load_dotenv()

#configuro app flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') 
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')  

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

#conf db PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL') 
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)  
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
    numero_tessera = Column(BigInteger)  
    inviato = Column(String)
    manuale = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    db_session = Session()  
    try:
        nome = request.form['nome']
        cognome = request.form['cognome']
        citta = request.form['citta']  
        data = request.form['data']      
        residenza = request.form['residenza']  
        sesso = request.form['sesso']          
        carta_identita = request.form['carta_identita']  
        email = request.form['email']
        file = request.files.get('file') 

        #check se file caricato
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            new_user = User(
                nome=nome,
                cognome=cognome,
                citta=citta,             
                data=data,               
                residenza=residenza,     
                sesso=sesso,             
                carta_identita=carta_identita,  
                email=email,
                file=file.filename,
                approvato="",
                numero_tessera=None, 
                inviato=""
            )

            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('index'))
        else:
            return "Nessun file caricato.", 400 
    except Exception as e:
        print("Errore durante l'inserimento:", e)  
        return f"Si è verificato un errore durante l'inserimento dei dati: {e}", 500  
    finally:
        db_session.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    pin = os.getenv('PIN')  
    if request.method == 'POST':
        input_pin = request.form['pin']
        if input_pin == pin:  
            session['authenticated'] = True 
            return redirect(url_for('view_users'))
        else:
            return "PIN errato!", 403
    return render_template('login.html')  

@app.route('/view_users')
def view_users():
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    db_session = Session()
    try:
        users = db_session.query(User).all()
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
                user.numero_tessera = numero_tessera 
            else:
                max_numero_tessera = db_session.query(User).filter(User.numero_tessera.isnot(None)).order_by(User.numero_tessera.desc()).first()
                if max_numero_tessera:
                    user.numero_tessera = max_numero_tessera.numero_tessera + 1
                else:
                    user.numero_tessera = 1  
            db_session.commit()
        else:
            return "Utente non trovato.", 404 
    except Exception as e:
        print("Errore nell'aggiornamento del numero di tessera:", e)
        return f"Si è verificato un errore nell'aggiornamento del numero di tessera: {e}", 500
    finally:
        db_session.close()
    return redirect(url_for('view_users'))

@app.route('/update_approval/<int:user_id>', methods=['POST'])
def update_approval(user_id):
    db_session = Session()
    try:
        user = db_session.query(User).get(user_id)
        if user:
            user.approvato = "SI"  
            db_session.commit()
        else:
            return "Utente non trovato.", 404 
    except Exception as e:
        print("Errore nell'aggiornamento dell'approvazione:", e)
        return f"Si è verificato un errore nell'aggiornamento dell'approvazione: {e}", 500 
    finally:
        db_session.close()
    return redirect(url_for('view_users'))

@app.route('/update_manual/<int:user_id>', methods=['POST'])
def update_manual(user_id):
    db_session = Session()
    try:
        user = db_session.query(User).get(user_id)
        if user:
            user.manuale = request.form['manuale']  
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
    app.run(host='0.0.0.0', port=5000, debug=True)



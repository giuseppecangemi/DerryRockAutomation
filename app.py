from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Cartella per i file caricati

# Assicurati che la cartella esista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    cognome = request.form['cognome']
    email = request.form['email']
    file = request.files['file']

    # Salva il file
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

    # Crea un DataFrame con i nuovi dati
    new_data = {
        'Nome': [nome],
        'Cognome': [cognome],
        'Email': [email],
        'File': [file.filename],
        'Approvato': ["SI"],
        'Numero Tessera': [None],
        'Inviato': [""]
    }
    new_df = pd.DataFrame(new_data)

    # Controlla se il file Excel esiste già
    if os.path.exists('dati.xlsx'):
        # Carica i dati esistenti
        existing_df = pd.read_excel('dati.xlsx')
        # Unisci i nuovi dati ai dati esistenti
        final_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        # Se non esiste, usa solo i nuovi dati
        final_df = new_df

    # Salva il DataFrame finale in Excel
    final_df.to_excel('dati.xlsx', index=False)

    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Imposta la porta
    app.run(host='0.0.0.0', port=port, debug=True)


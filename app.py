from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime
import os

# -------------------------------------------------------------
# Configuration
# -------------------------------------------------------------
DATABASE = os.getenv("DATABASE", "notes.db")
PORT = int(os.getenv("PORT", 5000))

app = Flask(__name__)

# -------------------------------------------------------------
# Database Setup
# -------------------------------------------------------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

@app.route('/')
def index():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    conn = get_db_connection()
    conn.execute('INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)',
                 (title, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/api/notes', methods=['GET'])
def api_get_notes():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY id DESC').fetchall()
    conn.close()
    notes_list = [dict(note) for note in notes]
    return jsonify(notes_list)

@app.route('/api/notes', methods=['POST'])
def api_create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content', '')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO notes (title, content, created_at) VALUES (?, ?, ?)',
                 (title, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note created successfully'}), 201

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def api_delete_note(note_id):
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id=?', (note_id,)).fetchone()
    if not note:
        conn.close()
        return jsonify({'error': 'Note not found'}), 404
    conn.execute('DELETE FROM notes WHERE id=?', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note deleted successfully'})

# -------------------------------------------------------------
# Main
# -------------------------------------------------------------
if __name__ == '__main__':
    print(f"🚀 Flask app running on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)


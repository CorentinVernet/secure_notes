import tkinter as tk
from tkinter import Button, Label, Entry, Text, messagebox
import sqlite3


def create_account():
    # Get the entered username and password
    new_username = entry_new_id.get()
    new_password = entry_new_psw.get()

    # Check if the username already exists in the database
    cursor.execute("SELECT * FROM users WHERE username=?", (new_username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Erreur", "Le nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
    else:
        # Insert the new user's information into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
        # Créer une table de notes pour le nouvel utilisateur
        cursor.execute("CREATE TABLE IF NOT EXISTS user_notes (username TEXT PRIMARY KEY, notes TEXT)")
        connection.commit()
        messagebox.showinfo("Succès", "Compte créé avec succès.")

# Définir une variable pour suivre l'utilisateur actuellement connecté
current_user = None

# Function to log in
def login():
    # Get the entered username and password
    username = entry_id.get()
    password = entry_psw.get()

    # Check if the username and password match a record in the database
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    if user:
        global current_user
        current_user = username
        open_window_note()  # Ouvrir la fenêtre des notes si la connexion est réussie
        window_connect.withdraw()  # Masquer la fenêtre de connexion
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.")

# Create a SQLite database and a table to store user accounts
connection = sqlite3.connect("user.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
connection.commit()


# Définissez les variables globales pour les widgets de création de compte
label_new_id = None
entry_new_id = None
label_new_psw = None
entry_new_psw = None
button_create_account = None

def open_window_create_account():
    global label_new_id, entry_new_id, label_new_psw, entry_new_psw, button_create_account
    # Créer une nouvelle instance de la fenêtre de création de compte
    new_window_account = tk.Toplevel()
    new_window_account.title("Créer un nouveau compte")
    new_window_account.geometry("600x500")

    # Label new id
    label_new_id = Label(new_window_account, text="Entrez votre nouvel identifiant :")
    label_new_id.pack()

    # Entry new id
    entry_new_id = Entry(new_window_account)
    entry_new_id.pack()

    # Label new password
    label_new_psw = Label(new_window_account, text="Entrez votre nouveau mot de passe :")
    label_new_psw.pack()

    # Entry new password
    entry_new_psw = Entry(new_window_account, show="*")
    entry_new_psw.pack()

    # Bouton pour créer le compte
    button_create_account = Button(new_window_account, text="Créer mon compte", command=create_account)
    button_create_account.pack()

    

# Définir notes_text en tant que variable globale
notes_text = None

def on_enter_key(event):
    if event.keysym == "Return":
        login()


def open_window_note():
    global notes_text  # Indiquez que nous utilisons la variable globale
    # Créer une nouvelle fenêtre pour les notes
    window_note_secure = tk.Toplevel()
    window_note_secure.title("Notes sécurisées")
    window_note_secure.geometry("600x500")

# Créer la zone de texte pour les notes
    notes_text = tk.Text(window_note_secure)
    notes_text.pack()

    # Récupérer les notes de l'utilisateur connecté depuis la base de données
    cursor.execute("SELECT notes FROM user_notes WHERE username=?", (current_user,))
    user_notes = cursor.fetchone()


    # Si l'utilisateur a des notes, les afficher dans la zone de texte
    if user_notes:
        notes_text.delete("1.0", "end")  # Effacer le contenu actuel de la zone de texte
        notes_text.insert("1.0", user_notes[0])

# Fonction pour sauvegarder les notes de l'utilisateur en cas de fermeture de la fenêtre
    def on_close():
        global notes_text  # Indiquez que nous utilisons la variable globale
        notes = notes_text.get("1.0", "end-1c")
        # Mettre à jour ou insérer les notes de l'utilisateur dans la base de données
        cursor.execute("INSERT OR REPLACE INTO user_notes (username, notes) VALUES (?, ?)", (current_user, notes))
        connection.commit()
        window_note_secure.destroy()
        open_window_connect()

    # Définir une action de fermeture pour la fenêtre des notes
    window_note_secure.protocol("WM_DELETE_WINDOW", on_close)

def open_window_connect():
    # Réinitialiser les champs de connexion
    entry_id.delete(0, "end")
    entry_psw.delete(0, "end")
    # Rendre la fenêtre de connexion visible
    window_connect.deiconify()



'''
FENETRE DE CONNECTION

'''


window_connect = tk.Tk()
window_connect.title("Fenêtre de connexion")
window_connect.geometry("300x300")

# Label id
label_id = Label(window_connect, text="Entrez votre identifiant :")
label_id.pack()

# Entry id
entry_id = Entry(window_connect)
entry_id.pack()

# Label password
label_psw = Label(window_connect, text="Entrez votre mot de passe :")
label_psw.pack()

# Entry password
entry_psw = Entry(window_connect, show="*")
entry_psw.pack()

# Bouton pour se connecter
button_connect = tk.Button(window_connect, text="Se connecter", command=login)
button_connect.pack()

# Bouton pour créer un nouveau compte
button_new_account = tk.Button(window_connect, text="Créer un nouveau compte", command=open_window_create_account)
button_new_account.pack()


'''
FENETRE COMPTE

'''


window_account = tk.Toplevel()
window_account.title("Créer un nouveau compte")
window_account.geometry("600x500")
window_account.withdraw()  # Masquer la fenêtre au départ

# Label new id
label_new_id = Label(window_account, text="Entrez votre nouvel identifiant :")
label_new_id.pack()

# Entry new id
entry_new_id = Entry(window_account)
entry_new_id.pack()

# Label new password
label_new_psw = Label(window_account, text="Entrez votre nouveau mot de passe :")
label_new_psw.pack()

# Entry new password
entry_new_psw = Entry(window_account, show="*")
entry_new_psw.pack()

#Bouton pour créer le compte
button_create_account = Button(window_account, text="Créer mon compte", command=create_account)
button_create_account.pack()

entry_psw.bind("<KeyPress>", on_enter_key)


'''
FENETRE NOTES

'''

window_note_secure = tk.Toplevel()
window_note_secure.title("Notes sécurisées")
window_note_secure.geometry("600x500")
window_note_secure.withdraw()


# Créer une zone de texte pour afficher les notes
notes_text = tk.Text(window_note_secure)
notes_text.pack()



window_connect.mainloop()
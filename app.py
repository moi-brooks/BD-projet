import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Interface Réservations Hôtel", layout="centered")

DB_PATH = "hotel_db.sqlite"

def connect_db():
    return sqlite3.connect(DB_PATH)

def view_reservations():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, r.date_debut, r.date_fin, c.nom, ch.numero, h.ville
        FROM Reservation r
        JOIN Client c ON r.client_id = c.id
        JOIN Chambre ch ON r.chambre_id = ch.id
        JOIN Hotel h ON ch.hotel_id = h.id
        ORDER BY r.date_debut DESC
    """)
    reservations = cursor.fetchall()
    conn.close()
    return reservations

def view_clients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nom, email, telephone, adresse, ville, code_postal
        FROM Client
        ORDER BY nom
    """)
    clients = cursor.fetchall()
    conn.close()
    return clients

def available_rooms(start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ch.id, ch.numero, ch.etage, tc.nom, tc.prix, h.ville
        FROM Chambre ch
        JOIN TypeChambre tc ON ch.type_chambre_id = tc.id
        JOIN Hotel h ON ch.hotel_id = h.id
        WHERE ch.id NOT IN (
            SELECT chambre_id FROM Reservation
            WHERE NOT (date_fin < ? OR date_debut > ?)
        )
        ORDER BY h.ville, ch.numero
    """, (start_date, end_date))
    rooms = cursor.fetchall()
    conn.close()
    return rooms

def add_client(nom, adresse, ville, code_postal, email, telephone):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Client (nom, adresse, ville, code_postal, email, telephone)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nom, adresse, ville, code_postal, email, telephone))
    conn.commit()
    conn.close()

def add_reservation(client_id, chambre_id, date_debut, date_fin):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Reservation (date_debut, date_fin, client_id, chambre_id)
        VALUES (?, ?, ?, ?)
    """, (date_debut, date_fin, client_id, chambre_id))
    conn.commit()
    conn.close()

def get_clients_for_select():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM Client ORDER BY nom")
    clients = cursor.fetchall()
    conn.close()
    return clients

def get_rooms_for_select():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ch.id, ch.numero, h.ville, tc.nom
        FROM Chambre ch
        JOIN Hotel h ON ch.hotel_id = h.id
        JOIN TypeChambre tc ON ch.type_chambre_id = tc.id
        ORDER BY h.ville, ch.numero
    """)
    rooms = cursor.fetchall()
    conn.close()
    return rooms

# --- Simple Professional CSS ---
st.markdown("""
    <style>
    body, .main-title {
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1A237E;
        text-align: center;
        margin-bottom: 1.5em;
        letter-spacing: 1px;
    }
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 2px 8px #1A237E22;
        border: 1px solid #E3E6F0;
        background: #FAFAFA;
    }
    .stForm {
        background: #F5F7FA;
        border-radius: 10px;
        padding: 2em 2em 1em 2em;
        box-shadow: 0 2px 8px #1A237E11;
        margin-bottom: 2em;
        border: 1px solid #E3E6F0;
    }
    .stButton>button, .stForm>button {
        background: #1A237E;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.5em 1.5em;
        margin-top: 1em;
        transition: 0.2s;
    }
    .stButton>button:hover, .stForm>button:hover {
        background: #3949AB;
        color: #fff;
        box-shadow: 0 2px 8px #1A237E33;
    }
    .stTextInput>div>input, .stSelectbox>div>div>div {
        border-radius: 5px;
        border: 1.5px solid #1A237E;
        background: #FAFAFA;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Interface Réservations Hôtel</div>', unsafe_allow_html=True)

menu = [
    "Consulter la liste des réservations",
    "Consulter la liste des clients",
    "Consulter la liste des chambres disponibles",
    "Ajouter un client",
    "Ajouter une réservation"
]

choice = st.sidebar.radio("Navigation", menu)

if choice == menu[0]:
    st.subheader("Liste des réservations")
    reservations = view_reservations()
    if reservations:
        st.dataframe(
            {
                "ID": [r[0] for r in reservations],
                "Début": [r[1] for r in reservations],
                "Fin": [r[2] for r in reservations],
                "Client": [r[3] for r in reservations],
                "Chambre": [r[4] for r in reservations],
                "Ville Hôtel": [r[5] for r in reservations],
            }
        )
    else:
        st.info("Aucune réservation trouvée.")

elif choice == menu[1]:
    st.subheader("Liste des clients")
    clients = view_clients()
    if clients:
        st.dataframe(
            {
                "ID": [c[0] for c in clients],
                "Nom": [c[1] for c in clients],
                "Email": [c[2] for c in clients],
                "Téléphone": [c[3] for c in clients],
                "Adresse": [c[4] for c in clients],
                "Ville": [c[5] for c in clients],
                "Code Postal": [c[6] for c in clients],
            }
        )
    else:
        st.info("Aucun client trouvé.")

elif choice == menu[2]:
    st.subheader("Chambres disponibles pour une période donnée")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Date de début", value=datetime.today())
    with col2:
        end_date = st.date_input("Date de fin", value=datetime.today())
    if start_date > end_date:
        st.warning("La date de début doit être avant la date de fin.")
    elif st.button("Voir les chambres disponibles"):
        rooms = available_rooms(str(start_date), str(end_date))
        if rooms:
            st.dataframe(
                {
                    "ID": [r[0] for r in rooms],
                    "Numéro": [r[1] for r in rooms],
                    "Étage": [r[2] for r in rooms],
                    "Type": [r[3] for r in rooms],
                    "Prix (€)": [r[4] for r in rooms],
                    "Ville Hôtel": [r[5] for r in rooms],
                }
            )
        else:
            st.info("Aucune chambre disponible pour cette période.")

elif choice == menu[3]:
    st.subheader("Ajouter un client")
    with st.form("add_client_form"):
        nom = st.text_input("Nom")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.text_input("Code postal")
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter le client")
        if submitted:
            if not (nom and adresse and ville and code_postal and email and telephone):
                st.warning("Veuillez remplir tous les champs.")
            else:
                try:
                    add_client(nom, adresse, ville, int(code_postal), email, telephone)
                    st.success(f"Client '{nom}' ajouté avec succès !")
                except Exception as e:
                    st.error(f"Erreur lors de l'ajout : {e}")

elif choice == menu[4]:
    st.subheader("Ajouter une réservation")
    clients = get_clients_for_select()
    rooms = get_rooms_for_select()
    if not clients or not rooms:
        st.warning("Il faut au moins un client et une chambre pour ajouter une réservation.")
    else:
        client_dict = {f"{c[1]} (ID {c[0]})": c[0] for c in clients}
        room_dict = {f"{r[1]} ({r[2]}, {r[3]}) [ID {r[0]}]": r[0] for r in rooms}
        with st.form("add_reservation_form"):
            client_sel = st.selectbox("Client", list(client_dict.keys()))
            room_sel = st.selectbox("Chambre", list(room_dict.keys()))
            date_debut = st.date_input("Date de début", value=datetime.today())
            date_fin = st.date_input("Date de fin", value=datetime.today())
            submitted = st.form_submit_button("Ajouter la réservation")
            if submitted:
                if date_debut > date_fin:
                    st.warning("La date de début doit être avant la date de fin.")
                else:
                    try:
                        add_reservation(client_dict[client_sel], room_dict[room_sel], str(date_debut), str(date_fin))
                        st.success("Réservation ajoutée avec succès !")
                    except Exception as e:
                        st.error(f"Erreur lors de l'ajout : {e}")
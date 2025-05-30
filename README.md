# Hotel Reservation App / Application de Réservation d'Hôtel

This project is a hotel reservation system built using Python and Streamlit. It allows users to manage reservations, clients, and available rooms through a simple web interface.

Ce projet est un système de réservation d'hôtel développé avec Python et Streamlit. Il permet aux utilisateurs de gérer les réservations, les clients et les chambres disponibles via une interface web simple.

## Features / Fonctionnalités

- **View Reservations / Voir les Réservations**: Display a list of all reservations in the system.  
    Affiche une liste de toutes les réservations dans le système.
- **View Clients / Voir les Clients**: Display a list of all clients registered in the system.  
    Affiche une liste de tous les clients enregistrés dans le système.
- **Available Rooms / Chambres Disponibles**: Check the availability of rooms for a specified period.  
    Vérifie la disponibilité des chambres pour une période donnée.
- **Add Client / Ajouter un Client**: Add a new client to the database.  
    Ajoute un nouveau client à la base de données.
- **Add Reservation / Ajouter une Réservation**: Create a new reservation for a client.  
    Crée une nouvelle réservation pour un client.

## Requirements / Prérequis

- Python 3.x
- Streamlit
- SQLite3

## Setup Instructions / Instructions d'Installation

1. Clone the repository:  
     Clonez le dépôt :
     ```
     git clone <repository-url>
     ```

2. Install the required packages:  
     Installez les paquets requis :
     ```
     pip install streamlit
     ```

3. Create the SQLite database and tables if they do not exist. You can use the provided SQL scripts or create them manually.  
     Créez la base de données SQLite et les tables si elles n'existent pas. Vous pouvez utiliser les scripts SQL fournis ou les créer manuellement.

4. Run the application:  
     Lancez l'application :
     ```
     streamlit run app.py
     ```

5. Open your web browser and go to `http://localhost:....` to access the application.  
     Ouvrez votre navigateur web et allez à `http://localhost:....` pour accéder à l'application.

## Usage / Utilisation

- Use the navigation options in the Streamlit interface to view reservations, clients, and available rooms.  
    Utilisez les options de navigation dans l'interface Streamlit pour voir les réservations, les clients et les chambres disponibles.
- Fill out the forms to add new clients and reservations.  
    Remplissez les formulaires pour ajouter de nouveaux clients et réservations.

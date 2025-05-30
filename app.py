import streamlit as st
import sqlite3

def connect_db():
    return sqlite3.connect("hotel_db.sqlite")

st.title("Interface Réservations Hôtel")

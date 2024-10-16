import streamlit as st


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is "articles":
        articles_menu()
        return
    bank_menu()


def articles_menu():
    # Show a navigation menu for the articles app
    st.sidebar.page_link("Articles.py", label="Articles")
    st.sidebar.page_link("pages/Export.py", label="Export")

def bank_menu():
    # Show a navigation menu for the bank app
    st.sidebar.page_link("Bank_Exec.py", label="Dashboard")
    st.sidebar.page_link("pages/Articles.py", label="Articles")
    st.sidebar.page_link("pages/Export.py", label="Export")
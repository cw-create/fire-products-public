import hmac
import os
import re

import extra_streamlit_components as stx
import streamlit as st

INTERNAL_API_KEY = os.environ.get("INTERNAL_API_KEY", "")


@st.cache_resource
def get_manager():
    return stx.CookieManager()


cookie_manager = get_manager()


def check_form() -> bool:
    """Returns `True` if the user had the correct password."""

    def access_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Email", key="email")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Access", on_click=validate_form)

    def check_email():
        """Checks whether an email entered by the user is correctly formatted."""
        return re.match(r".+[@].+[.].+", st.session_state["email"])

    def check_password():
        """Checks whether a password entered by the user is correct."""
        return hmac.compare_digest(st.session_state["password"], INTERNAL_API_KEY)

    def validate_form():
        """Validate the form and set the form_correct state."""
        if not check_email():
            st.session_state["form_correct"] = False
            st.session_state["error_message"] = "😕 Please enter a valid email"
            return

        if not check_password():
            st.session_state["form_correct"] = False
            st.session_state["error_message"] = "😕 Password is incorrect"
            return

        st.session_state["form_correct"] = True
        del st.session_state["password"]  # Don't store the password.

        # if cookie_manager.get("email") != st.session_state["email"]:
        cookie_manager.set("bp_email", st.session_state["email"], key="cookie_set_email")
        cookie_manager.set("bp_form_correct", "True", key="cookie_set_form_correct")

    if st.session_state.get("form_correct", False):
        return True

    if cookie_manager.get("bp_form_correct") == "True":
        st.session_state["email"] = cookie_manager.get("bp_email")
        st.session_state["form_correct"] = True
        return True

    access_form()
    if st.session_state.get("error_message"):
        st.error(st.session_state["error_message"])
    return False

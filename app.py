# --- FILE: app.py ---
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["connections"]["gsheets"], scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(st.secrets["connections"]["gsheets"]["spreadsheet"])
worksheet = spreadsheet.worksheet("GameProgress")

# Helper functions
def load_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def sync_with_gsheets(df):
    worksheet.clear()
    worksheet.update([df.columns.tolist()] + df.values.tolist())

# App page selection
st.set_page_config(page_title="Pin The Culprit")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Team Registration", "Room 255 & Code", "Room 325", "Final Submission"])

# Page 1: Registration
if page == "Team Registration":
    st.title("Pin The Culprit - Team Registration")
    if "team_id" not in st.session_state:
        team_name = st.text_input("Enter your Team Name:")
        if st.button("Register"):
            if not team_name.strip():
                st.error("Please enter a valid team name.")
            else:
                df = load_data()
                team_id = len(df) + 1
                start_time = datetime.now().strftime("%H:%M:%S")

                new_entry = pd.DataFrame([{
                    "team_id": team_id,
                    "team_name": team_name,
                    "start_time": start_time,
                    "end_time": "",
                    "culprit": "",
                    "reason": ""
                }])

                df = pd.concat([df, new_entry], ignore_index=True)
                sync_with_gsheets(df)

                st.session_state["team_id"] = team_id
                st.session_state["team_name"] = team_name
                st.session_state["start_time"] = start_time
                st.success("Team registered successfully! Proceed to the next step.")
                st.markdown("[📂 Open First Drive Link](https://drive.google.com/drive/folders/1y8vhT4lKziFYdlaE8x9_SbNlE6Z4mAcF?usp=sharing)", unsafe_allow_html=True)  # First Drive link
    else:
        st.success(f"Welcome back, {st.session_state['team_name']}! Proceed using the sidebar.")

# Page 2: Room 255 & Code Entry
elif page == "Room 255 & Code":
    st.title("Go to Room 255")
    st.write("After exploring the clue, go to Room 255.")
    st.markdown("[🔗 Clue Site 1](https://ptc-sxlt-aksran31s-projects.vercel.app/)")
    st.markdown("[🔗 Clue Site 2](https://ptc-aksran31s-projects.vercel.app/)")

    st.subheader("Enter the Code")
    final_code = "876432"
    code = st.text_input("Enter the code:")
    if st.button("Check Code"):
        if code == final_code:
            st.success("Correct! Now go to Room 325 for the next puzzle.")
            st.session_state["entered_code"] = True
        else:
            st.error("Wrong code, try again.")

# Page 3: Room 325 - Password Check
elif page == "Room 325":
    st.title("Room 325 - Password Puzzle")
    if not st.session_state.get("entered_code"):
        st.warning("You must complete the previous stage first.")
    else:
        correct_answer = "1a6yrA-1y5Z52AxABB2LfwYIwOm-7vwQV"
        answer = st.text_input("Enter the password:")
        if st.button("Submit"):
            if answer == correct_answer:
                st.success("Correct! Open the next clue.")
                st.markdown("[📂 Open Second Drive Link](https://drive.google.com/drive/folders/1a6yrA-1y5Z52AxABB2LfwYIwOm-7vwQV)", unsafe_allow_html=True)  # Second Drive link
                st.session_state["solved_clue"] = True
            else:
                st.error("Incorrect, try again!")

# Page 4: Final Submission
elif page == "Final Submission":
    st.title("Final Submission")
    if not st.session_state.get("solved_clue"):
        st.warning("You must complete the previous stage first.")
    else:
        culprit = st.text_input("Who do you think the culprit is?")
        reason = st.text_area("What is your reasoning?")
        if st.button("Submit Final Answer"):
            df = load_data()
            team_id = st.session_state["team_id"]
            index = df[df["team_id"] == team_id].index[0]

            df.at[index, "culprit"] = culprit
            df.at[index, "reason"] = reason
            df.at[index, "end_time"] = datetime.now().strftime("%H:%M:%S")

            sync_with_gsheets(df)
            st.success("Your final answer has been recorded. Thank you for playing!")

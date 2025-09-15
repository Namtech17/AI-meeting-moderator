import streamlit as st

st.set_page_config(page_title="AI Meeting Moderator", layout="wide")

# --- Sidebar ---
st.sidebar.title("AI Meeting Moderator")
st.sidebar.info("Prototype Dashboard for Meetings & Group Discussions")

# --- Title ---
st.title("🤖 AI-Based Meeting Moderator")
st.write("This dashboard simulates how an AI moderator works in online meetings.")

# --- Transcript Input ---
st.subheader("📜 Meeting Transcript")
dummy_transcript = """Alice: I think we should spend more on marketing, maybe 50%.
Bob: No, logistics are more important, at least 60%.
Charlie: I agree with Bob, logistics are crucial.
UnknownUser: I also think logistics should get 80%.
Alice: Sorry, but who is this? I don’t see UnknownUser on the invite list.
Bob: Yes, strange. Anyway, I think Alice is not considering risks.
Alice: You're interrupting me again, Bob. Please let me finish.
"""

transcript = st.text_area("Enter transcript:", dummy_transcript, height=200)

# --- AI Moderator Actions ---
st.subheader("⚡ AI Moderator Actions")
st.markdown("""
- ⚠ **Unauthorized User Detected:** UnknownUser not on invite list.  
- ⚠ **Interruptions:** Bob interrupted Alice (2 times).  
- ⚠ **Dominance:** Bob spoke 40% more than others.  
- ✅ **Noise Handling:** Suggest muting UnknownUser if disruptive.
""")

# --- Summary ---
st.subheader("📝 Meeting Summary")
st.success("""
- **Topic:** Budget Allocation for Event  
- Alice suggested 50% for marketing.  
- Bob + Charlie supported higher logistics allocation (60%).  
- Conflict: Alice vs Bob on priorities.  
- Suspicious: UnknownUser joined without invite, pushing logistics agenda.
""")

# --- Fairness & Suggestions ---
st.subheader("🤝 Fairness & Compromise Suggestion")
st.info("""
- Allocate 50% logistics, 40% marketing, 10% contingency.  
- Schedule follow-up with **verified participants only**.  
- Ensure equal speaking time by setting a timer per person.
""")

# --- Stats ---
st.subheader("📊 Participation Stats")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Alice", "25% talk time")
col2.metric("Bob", "40% talk time")
col3.metric("Charlie", "20% talk time")
col4.metric("UnknownUser", "15% talk time")

# --- Security Alerts ---
st.subheader("🔒 Security Alerts")
st.error("1 unauthorized user detected: UnknownUser")

# --- Git Initialization ---
st.subheader("📂 Git Repository")
git_init = st.button("Initialize Git Repository")
if git_init:
    st.success("Git repository initialized.")
    # Here you would normally call a function to initialize a git repo, e.g.:
    # os.system('git init')


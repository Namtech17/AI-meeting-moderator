import streamlit as st
import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# -------------------------
# Streamlit page config
# -------------------------
st.set_page_config(page_title="AI Meeting Moderator", layout="wide")
st.title("🤖 AI Meeting Moderator Dashboard")

# -------------------------
# Load Google Service Account from Streamlit Secrets
# -------------------------
creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

if not creds_json:
    st.error("⚠️ GOOGLE_SERVICE_ACCOUNT_JSON not found in secrets.")
    st.stop()

# Fix for private_key newlines: replace literal "\n" with real line breaks
creds_json = creds_json.replace('\\n', '\n')

# Parse JSON credentials
try:
    creds_dict = json.loads(creds_json)
except Exception as e:
    st.error(f"Could not parse GOOGLE_SERVICE_ACCOUNT_JSON: {e}")
    st.stop()

# Authenticate with Google APIs
creds = service_account.Credentials.from_service_account_info(
    creds_dict,
    scopes=[
        "https://www.googleapis.com/auth/documents.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
)

docs_service = build("docs", "v1", credentials=creds)
drive_service = build("drive", "v3", credentials=creds)

# -------------------------
# Fetch the latest Google Doc created by Zapier
# -------------------------
def get_latest_doc():
    results = drive_service.files().list(
        q="mimeType='application/vnd.google-apps.document'",
        orderBy="createdTime desc",
        pageSize=1,
        fields="files(id, name, createdTime)"
    ).execute()
    files = results.get("files", [])
    return files[0] if files else None

latest_doc = get_latest_doc()

if not latest_doc:
    st.info("No Google Docs found yet. Run a meeting and let Zapier create one.")
    st.stop()

st.subheader("📄 Latest Meeting Report")
st.write(f"**Name:** {latest_doc['name']}  \n**Created:** {latest_doc['createdTime']}")

# -------------------------
# Read content of the doc
# -------------------------
doc = docs_service.documents().get(documentId=latest_doc["id"]).execute()

content = ""
for element in doc.get("body", {}).get("content", []):
    if "paragraph" in element:
        for run in element["paragraph"].get("elements", []):
            text = run.get("textRun", {}).get("content", "")
            content += text

# -------------------------
# Try to split into sections
# (Zapier should format output as [Summary], [Unauthorized Users], etc.)
# -------------------------
sections = {}
current = None
for line in content.splitlines():
    line = line.strip()
    if line.startswith("[") and line.endswith("]"):
        current = line.strip("[]")
        sections[current] = []
    elif current:
        sections[current].append(line)

# -------------------------
# Display Report
# -------------------------
if sections:
    for sec, text in sections.items():
        st.subheader(sec)
        st.write("\n".join(text))
else:
    st.text_area("Raw Document Content", value=content, height=400)

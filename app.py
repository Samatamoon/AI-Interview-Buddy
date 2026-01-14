import streamlit as st
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="AI Interview Buddy")
st.title("🤖 AI Interview Buddy")
st.write("Your friendly helper to see how your resume matches a job description!")

# --- USER INPUT ---
job_description = st.text_area("Paste the Job Description here:")

resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# --- FUNCTION TO EXTRACT KEYWORDS ---
def extract_keywords(text):
    # Convert to lowercase and split words
    words = re.findall(r'\b\w+\b', text.lower())
    # Remove common English stopwords manually
    stop_words = {
        "the", "and", "a", "to", "in", "of", "for", "on", "with",
        "is", "as", "by", "an", "be", "this", "at", "from", "or",
        "that", "are", "it", "you", "your", "i", "we", "have",
        "has", "will", "can", "our"
    }
    keywords = [w for w in words if w not in stop_words]
    return set(keywords)

# --- MAIN LOGIC ---
if resume_file and job_description:
    # Read PDF
    reader = PdfReader(resume_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text()

    # Extract keywords
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    # Compare
    matched = resume_keywords.intersection(jd_keywords)
    missing = jd_keywords - resume_keywords

    # Match percentage
    match_percent = int(len(matched) / len(jd_keywords) * 100) if jd_keywords else 0

    # --- FRIENDLY OUTPUT ---
    st.subheader("📊 Match Results")
    st.markdown(f"**Match Percentage:** {match_percent}%")

    st.markdown("**✅ Skills you have:**")
    if matched:
        st.markdown(", ".join([f"🟢 {skill}" for skill in matched]))
    else:
        st.markdown("None yet! Keep learning 😉")

    st.markdown("**❌ Skills to improve:**")
    if missing:
        st.markdown(", ".join([f"🔴 {skill}" for skill in missing]))
    else:
        st.markdown("Wow! You have all required skills! 🎉")

    # Highlight job description
    st.subheader("📖 Job Description Highlights")
    highlighted_jd = job_description
    for skill in matched:
        highlighted_jd = re.sub(rf'\b{re.escape(skill)}\b', f"🟢{skill}🟢", highlighted_jd, flags=re.IGNORECASE)
    for skill in missing:
        highlighted_jd = re.sub(rf'\b{re.escape(skill)}\b', f"🔴{skill}🔴", highlighted_jd, flags=re.IGNORECASE)

    st.markdown(highlighted_jd)

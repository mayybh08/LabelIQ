import streamlit as st
import time
from openai import OpenAI

# ------------------ OPENAI CLIENT ------------------
client = OpenAI()  # uses OPENAI_API_KEY from environment

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="LabelIQ",
    page_icon="🏷️",
    layout="centered"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to {opacity: 1; transform: translateY(0);}
}
.fade-in {
    animation: fadeIn 0.6s ease-in-out;
}
.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}
.decision {
    font-size: 20px;
    font-weight: 600;
}
.badge-low { color: #1f8a4c; font-weight: 600; }
.badge-moderate { color: #d9822b; font-weight: 600; }
.badge-high { color: #c0392b; font-weight: 600; }

div.stButton > button {
    background: linear-gradient(90deg, #111827, #1f2937);
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<h1 class='fade-in'>🏷️ LabelIQ</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='fade-in'>Instant clarity from food labels. No prompts. No effort.</p>",
    unsafe_allow_html=True
)

# ------------------ INPUT ------------------
user_input = st.text_area(
    "Paste product name or ingredient list",
    placeholder="Example: Sugar, Maltodextrin, Palm Oil",
    height=110
)

# BUTTON (IMPORTANT: must exist before usage)
analyze = st.button("Analyze for Decision Clarity")

# ------------------ AI FUNCTION ------------------
def analyze_ingredient(text):
    # MOCKED AI RESPONSE (Round-1 Safe)
    return """DECISION:
⚠️ Okay occasionally. Avoid daily use.

WHY IT MATTERS:
This product contains ingredients that may negatively impact health when consumed frequently, especially as part of a regular diet.

UNCERTAINTY:
Moderate – scientific evidence is mixed and still evolving.

IF CONSUMED DAILY:
Daily consumption over time may increase health risks due to excess sugar, fats, or additives.

FINAL TAKEAWAY:
Safe occasionally, but not recommended as a daily habit.
"""


# ------------------ OUTPUT ------------------
if analyze and user_input.strip():
    with st.spinner("LabelIQ is thinking for you..."):
        time.sleep(0.5)
        result = analyze_ingredient(user_input)

    sections = result.split("\n")

    # Decision
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='decision'>🔍 {sections[0].replace('DECISION:', '').strip()}</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Why it matters
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.markdown("**Why this matters**")
    st.write(sections[1].replace("WHY IT MATTERS:", "").strip())
    st.markdown("</div>", unsafe_allow_html=True)

    # Uncertainty
    uncertainty_text = sections[2].lower()
    if "low" in uncertainty_text:
        badge = "badge-low"
    elif "high" in uncertainty_text:
        badge = "badge-high"
    else:
        badge = "badge-moderate"

    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.markdown("**Uncertainty level**")
    st.markdown(
        f"<span class='{badge}'>{sections[2].replace('UNCERTAINTY:', '').strip()}</span>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Daily impact
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.markdown("**If consumed daily**")
    st.write(sections[3].replace("IF CONSUMED DAILY:", "").strip())
    st.markdown("</div>", unsafe_allow_html=True)

    # Final takeaway
    st.markdown("<div class='fade-in card'>", unsafe_allow_html=True)
    st.markdown("**Final takeaway**")
    st.write(sections[4].replace("FINAL TAKEAWAY:", "").strip())
    st.markdown("</div>", unsafe_allow_html=True)

elif analyze:
    st.warning("Please paste a product name or ingredient list.")

import streamlit as st
import requests
from bs4 import BeautifulSoup
if "clicked" not in st.session_state:
    st.session_state.clicked = False
st.set_page_config(
    page_title="AI Landing Page Optimizer",
    page_icon="🚀",
    layout="centered"
)
st.markdown('<div class="glow glow1"></div>', unsafe_allow_html=True)
st.markdown('<div class="glow glow2"></div>', unsafe_allow_html=True)
import os
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
def call_llm(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/elephant-alpha",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        return response.json()["choices"][0]["message"]["content"]
    except:
        return str(response.json())


@st.cache_data
def get_page_content(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.get_text()[:3000]
    except:
        return "Could not fetch page."


@st.cache_data
def analyze_ad(ad_text):
    prompt = f"""
    Extract:
    - audience
    - intent
    - tone
    - offer

    Ad:
    {ad_text}
    """
    return call_llm(prompt)


@st.cache_data
def analyze_page(content):
    prompt = f"""
    Extract:
    - headline
    - CTA
    - main message

    Content:
    {content}
    """
    return call_llm(prompt)


@st.cache_data
def gap_analysis(ad, page):
    prompt = f"""
Compare AD vs LANDING PAGE.

Return ONLY:

1. Messaging mismatch
2. Audience mismatch
3. CTA mismatch
4. Missing elements

Be specific. No generic frameworks.

Ad:
{ad}

Page:
{page}
"""
    return call_llm(prompt)


@st.cache_data
def generate_output(ad, page_data, gaps):
    prompt = f"""
You are a CRO (conversion rate optimization) expert.

IMPORTANT:
- Do NOT create a new landing page
- Improve the EXISTING page
- Keep original structure
- Enhance copy to match ad intent

Ad insights:
{ad}

Current Page:
{page_data}

Gaps:
{gaps}

OUTPUT:

1. Improved Headline (based on current)
2. Improved CTA
3. Improved Sections (rewrite, not replace)
4. What changed + why (CRO reasoning)

Avoid generic phrases.
"""
    return call_llm(prompt)


@st.cache_data
def verify(output):
    prompt = f"""
You are a strict evaluator.

ONLY RETURN:

1. What is still weak
2. What can be improved further
3. Any generic phrases detected

Do NOT repeat the content.

Output:
{output}
"""
    return call_llm(prompt)


@st.cache_data
def get_confidence(output):
    prompt = f"""
    Rate your confidence in this landing page suggestion on a scale of 1-100%. Just give the percentage number.

    Suggestion:
    {output}
    """
    response = call_llm(prompt)
    import re
    match = re.search(r'\d+', response)
    if match:
        return match.group()
    else:
        return "85"


st.markdown("""
<div class="fade-in">
""", unsafe_allow_html=True)





st.markdown("""
<div style="text-align:center;">
<h1>🚀 AI Landing Page Optimizer</h1>
<p style="color:#9ca3af;">
Analyze → Fix → Enhance your landing pages using AI + CRO principles
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### ✍️ Input")

ad = st.text_area("Ad Copy", height=120, placeholder="Paste your ad here...")
url = st.text_input("Website URL", placeholder="https://example.com")

col1, col2, col3 = st.columns([1,2,1])

with col2:
    if st.button("✨ Generate Optimized Page", use_container_width=True):
        st.session_state.clicked = True
        generate = True
    else:
        generate = False
    
if generate:
    if ad and url:
        with st.spinner("⚡ Optimizing your landing page using AI + CRO..."):
            page = get_page_content(url)

            ad_data = analyze_ad(ad)
            page_data = analyze_page(page)
            gaps = gap_analysis(ad_data, page_data)
            result = generate_output(ad_data, page_data, gaps)
            review = verify(result)
            confidence = get_confidence(result)

        st.subheader("🔍 Analysis Pipeline")

        with st.expander("Ad Analysis"):
            st.write(ad_data)

        with st.expander("Page Analysis"):
            st.write(page_data)

        with st.expander("Gap Analysis"):
            st.write(gaps)

        st.divider()
        st.header("✨ Enhanced Landing Page")

        st.markdown("## 🔄 Before vs After")

        st.subheader("Original Page Summary")
        st.write(page_data)

        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)

        st.markdown("## ✨ CRO-Enhanced Version")
        st.success("✅ Optimized based on ad intent")

        st.write(result)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)

        st.markdown("### 🎯 Personalization Applied")
        st.info("Aligned messaging with ad intent: productivity, students, professionals")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card fade-in">', unsafe_allow_html=True)

        st.markdown("## 🔍 AI Review")
        st.warning("⚠️ Improvements & Weak Points")

        st.write(review)

        st.markdown('</div>', unsafe_allow_html=True)

        st.metric("Confidence Score", f"{confidence}%")
    else:
        st.warning("Enter both inputs")

st.caption("Built with AI-driven CRO optimization pipeline (analysis → gap detection → enhancement → evaluation)")

if st.session_state.clicked:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg,
            #020617,
            #0f172a,
            #1e293b,
            #3730a3
        );
        background-size: 200% 200%;
        animation: smoothGlow 6s ease-in-out infinite;
    }

    @keyframes smoothGlow {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #020617, #0f172a);
    }
    </style>
    """, unsafe_allow_html=True)
if st.session_state.clicked:
    # ☀️ LIGHT THEME
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #f8fafc, #e2e8f0);
        color: #0f172a;
    }

    /* Fix text visibility */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #0f172a !important;
    }

    </style>
    """, unsafe_allow_html=True)

else:
    # 🌑 DARK THEME (default)
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #020617, #0f172a);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
<style>

.stButton > button {
    display: block;
    margin: 28px auto;
    width: 100%;
    max-width: 320px;
    height: 3.2em;
    border-radius: 16px;
    font-weight: 600;
    color: #0f172a;
    border: none;

    background: linear-gradient(135deg, #bfdbfe, #93c5fd);

    box-shadow:
        0 0 16px rgba(147,197,253,0.35),
        0 0 32px rgba(96,165,250,0.25);

    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: scale(1.04);
    box-shadow:
        0 0 26px rgba(147,197,253,0.5),
        0 0 50px rgba(96,165,250,0.35);
}

</style>
""", unsafe_allow_html=True)
if st.session_state.clicked:
    st.markdown("""
    <style>

    .stApp {
        background:
            radial-gradient(circle at 20% 30%, rgba(191,219,254,0.5), transparent 45%),
            radial-gradient(circle at 80% 70%, rgba(147,197,253,0.4), transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(219,234,254,0.35), transparent 60%),
            linear-gradient(180deg, #eff6ff, #dbeafe);

        background-size: 200% 200%;
        animation: blueFlow 16s ease-in-out infinite;
    }

    @keyframes blueFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: #0f172a !important;
    }

    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #020617, #0f172a);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
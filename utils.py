import streamlit as st

def apply_global_style():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;900&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Cairo', 'Noto Kufi Arabic', 'Tajawal', Arial, sans-serif !important;
        background: linear-gradient(120deg, #f3f8ff 0%, #dde7fa 100%) fixed;
    }
    h1, h2, h3, h4 {
        font-family: 'Cairo', Arial, sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: 0.3px;
    }
    .big-logo {
        width: 110px; margin-bottom: 10px;
        display: block; margin-left: auto; margin-right: auto;
        filter: drop-shadow(0 2px 12px #377dff33);
    }
    .card, .info-card {
        background: rgba(255,255,255,0.96); border-radius: 18px; 
        box-shadow: 0 6px 32px 0 #b0c4d866; padding: 32px 20px 26px 20px;
        margin-bottom: 24px;
    }
    .cards-row {
        display: flex; flex-direction: row; gap: 18px; justify-content: center; align-items: stretch;
        margin-top: 28px; margin-bottom: 10px;
    }
    .info-card {
        min-width: 250px; max-width: 340px; flex:1; margin:0 6px;
        border-right: 6px solid #377dff33;
    }
    .start-btn, .blue-btn {
        font-size: 20px !important; border-radius: 18px !important; padding: 13px 38px !important; margin-bottom: 10px;
        background: linear-gradient(90deg, #2551a3 15%, #64a6ff 100%) !important;
        color: #fff !important; font-weight:800;
        border: none !important;
        transition: background 0.3s;
        box-shadow: 0 2px 10px #2551a322;
    }
    .start-btn:hover, .blue-btn:hover {
        background: linear-gradient(90deg, #377dff 10%, #2a5eb8 100%) !important;
        color:#fff !important;
    }
    .lang-menu {
        position: absolute;
        top: 32px; left: 34px;
        z-index: 10000;
        background: #fff;
        border-radius: 12px;
        padding: 6px 16px;
        box-shadow: 0 2px 16px #377dff22;
        font-size:18px;
        font-weight:600;
        color: #2a5eb8;
    }
    .start-btn {
    border-radius: 22px !important;
    box-shadow: 0 2px 16px #2551a355;
    transition: background 0.25s;
    background: linear-gradient(90deg, #2551a3 15%, #64a6ff 100%) !important;
    }
    .start-btn:hover {
        background: linear-gradient(90deg, #377dff 10%, #2a5eb8 100%) !important;
    }

    </style>
    """, unsafe_allow_html=True)

def top_language_menu():
    lang_map = {
        "ar": "العربية",
        "en": "English",
    }
    current = st.session_state.get("lang", "ar")
    st.markdown("""
    <style>
    .lang-switch-row {
        display: flex; flex-direction: row; justify-content: flex-end; align-items: center;
        margin-bottom: 14px; margin-top: 15px; gap: 0.5em;
    }
    .lang-btn {
        background: none; border: none; color: #b0b0b0; font-size: 18px;
        padding: 2px 13px; border-radius: 8px; font-weight: 600;
        transition: background 0.18s;
        cursor: pointer;
    }
    .lang-btn.selected {
        color: #2551a3; background: #e4ecfd;
        font-weight: 900;
        box-shadow: 0 2px 10px #d8e8ff44;
    }
    .lang-btn:hover { background: #f0f6ff; color:#2551a3; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="lang-switch-row">' + ''.join([
        f'<form style="display:inline;" method="post"><button name="setlang" value="{k}" class="lang-btn{" selected" if current==k else ""}">{v}</button></form>'
        for k, v in lang_map.items()
    ]) + '</div>', unsafe_allow_html=True)
    # التعامل مع تغيير اللغة:
    if st.session_state.get("setlang"):
        st.session_state["lang"] = st.session_state["setlang"]
        st.session_state["setlang"] = ""

# لو أردت جعل كل النوافذ RTL أو LTR (تلقائياً حسب اللغة) أضف هذا في بداية كل صفحة (أو هنا):
def auto_direction():
    lang = st.session_state.get("lang", "ar")
    if lang == "ar":
        direction = "rtl"
        align = "right"
    else:
        direction = "ltr"
        align = "left"
    st.markdown(f"""
    <style>
    html, body, .main, .block-container {{
        direction: {direction} !important;
        text-align: {align} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

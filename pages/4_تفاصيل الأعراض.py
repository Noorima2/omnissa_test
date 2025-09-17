import streamlit as st
from utils import apply_global_style, top_language_menu, auto_direction

apply_global_style()
auto_direction()
top_language_menu()

st.markdown("""
<div class="card" style="max-width:530px; margin:auto; margin-top:22px; text-align:center;">
    <h2 class="blue-title" style="margin-bottom:13px;color:#2551a3;"> تفاصيل المشكلة الرئيسية</h2>
    <p style="font-size:17px;">يرجى تعبئة جميع التفاصيل الخاصة بأعراضك حتى نساعدك بأفضل صورة
</div>
""", unsafe_allow_html=True)

st.markdown("---")

chief_complaints = st.session_state.get('chief_complaints', [""])
complaint_durations = st.session_state.get('complaint_durations', [""])

hopi_details = []
all_required_filled = True

for idx, (cc, dur) in enumerate(zip(chief_complaints, complaint_durations)):
    if not cc:
        continue

    with st.expander(f"تفاصيل الشكوى رقم {idx+1}: {cc} (المدة: {dur})", expanded=True):
        site_key = f"site_{idx}"
        onset_key = f"onset_{idx}"
        char_key = f"char_{idx}"
        sev_key = f"sev_{idx}"
        att_dur_key = f"duration_{idx}"
        assoc_key = f"assoc_{idx}"
        rel_key = f"rel_{idx}"
        exac_key = f"exac_{idx}"

        site = st.text_input("مكان العرض (مثال: الجبهة، البطن...)*",
                             value=st.session_state.get(site_key, ""), key=site_key)
        onset = st.selectbox("متى بدأ العرض؟*",
                             ["", "فجأة", "تدريجي"],
                             index=["", "فجأة", "تدريجي"].index(st.session_state.get(onset_key, "")),
                             key=onset_key)
        character = st.text_input("كيف تصف العرض؟*",
                                 value=st.session_state.get(char_key, ""), key=char_key)
        severity = st.number_input("شدة العرض (1 = خفيف جدًا، 5 = شديد جدًا)*",
                                   min_value=1, max_value=5, value=st.session_state.get(sev_key, 3),key=sev_key, step=1)
        st.caption("1 = خفيف جدًا | 2 = خفيف | 3 = متوسط | 4 = شديد | 5 = شديد جدًا")
        
        duration = st.text_input("كم يستمر العرض كل مرة؟*",
                                value=st.session_state.get(att_dur_key, ""), key=att_dur_key)
        associated = st.text_area("هل توجد أعراض مصاحبة أخرى؟",
                                 value=st.session_state.get(assoc_key, ""), key=assoc_key)
        relieving = st.text_input("ما الذي يخفف العرض؟",
                                 value=st.session_state.get(rel_key, ""), key=rel_key)
        exacerbating = st.text_input("ما الذي يزيد العرض؟",
                                    value=st.session_state.get(exac_key, ""), key=exac_key)

        fields_filled = all([
            site.strip() != "",
            onset.strip() != "",
            character.strip() != "",
            duration.strip() != ""
        ])
        all_required_filled = all_required_filled and fields_filled

        hopi_details.append({
            "complaint": cc,
            "duration": dur,
            "site": site,
            "onset": onset,
            "character": character,
            "severity": severity,
            "attack_duration": duration,
            "associated": associated,
            "relieving": relieving,
            "exacerbating": exacerbating
        })

st.markdown("""
<style>
/* زر أزرق لجميع أزرار st.button تلقائيا داخل كارد */
.stButton>button {
    font-size: 20px !important; border-radius: 18px !important;
    padding: 10px 0px !important;
    width: 80% !important; margin: 10px auto 0 auto !important; display:block !important;
    background: linear-gradient(90deg, #2551a3 15%, #64a6ff 100%) !important;
    color: #fff !important; font-weight:800;
    border: none !important;
    box-shadow: 0 2px 10px #2551a322;
    transition: background 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #377dff 10%, #2a5eb8 100%) !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col2:
    if st.button("رجوع", use_container_width=True):
        st.switch_page("pages/3_مشكلتي الرئيسية.py")
with col1:
    if st.button("متابعة", use_container_width=True):
        if not all_required_filled:
            st.warning("يرجى تعبئة كل التفاصيل المطلوبة لكل شكوى رئيسية.")
        else:
            st.session_state['hopi_details'] = hopi_details
            st.success("تم حفظ تفاصيل الأعراض بنجاح.")
            st.switch_page("pages/5_مراجعة_الأعراض_الأخرى.py")

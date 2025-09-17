import streamlit as st
from utils import apply_global_style, top_language_menu, auto_direction

apply_global_style()
auto_direction()
top_language_menu()

st.markdown("""
<div class="card" style="max-width:530px; margin:auto; margin-top:22px; text-align:center;">
    <h2 class="blue-title" style="margin-bottom:13px;color:#2551a3;">  ما هي مشكلتك الصحية؟ </h2>
    <p style="font-size:17px;">سجل مشكلتك بكلماتك الخاصة، يمكنك إدخال حتى ثلاث شكاوى رئيسية
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 1. جلب القيم المحفوظة أو إنشاء افتراضي
chief_complaints = st.session_state.get("chief_complaints", ["", "", ""])
complaint_durations = st.session_state.get("complaint_durations", ["", "", ""])

num_complaints = st.selectbox(
    "كم عدد الشكاوى الرئيسية؟", [1, 2, 3],
    index=st.session_state.get("num_complaints_idx", 0)
)
st.session_state["num_complaints_idx"] = [1, 2, 3].index(num_complaints)

chief_complaints_display = []
complaint_durations_display = []

for i in range(num_complaints):
    c = st.text_input(
        f"الشكوى رقم {i+1}: ",
        value=chief_complaints[i] if len(chief_complaints) > i else "",
        key=f"complaint_{i+1}"
    )
    d = st.text_input(
        f"مدة الشكوى رقم {i+1}:",
        value=complaint_durations[i] if len(complaint_durations) > i else "",
        key=f"duration_{i+1}",
        help="مثال: يوم، أسبوع، شهر، سنة..."
    )
    chief_complaints_display.append(c)
    complaint_durations_display.append(d)

st.markdown("---")
st.write("### ملخص الشكاوى:")
for idx, (cc, cd) in enumerate(zip(chief_complaints_display, complaint_durations_display)):
    if cc:
        st.write(f"- **الشكوى رقم {idx+1}:** {cc} (المدة: {cd})")

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
        st.session_state['chief_complaints'] = chief_complaints_display
        st.session_state['complaint_durations'] = complaint_durations_display
        st.switch_page("pages/2_بياناتي الشخصية.py")
with col1:
    if st.button("متابعة", use_container_width=True):
        st.session_state['chief_complaints'] = chief_complaints_display
        st.session_state['complaint_durations'] = complaint_durations_display
        st.success("تم حفظ الشكوى الرئيسية. انتقل للخطوة التالية!")
        st.switch_page("pages/4_تفاصيل الأعراض.py")

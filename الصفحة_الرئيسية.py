import streamlit as st
from utils import apply_global_style, top_language_menu, auto_direction
apply_global_style()
auto_direction()
top_language_menu()

st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/4712/4712038.png" class="big-logo">', unsafe_allow_html=True)
st.info("""
**تنبيه هام:**  
هذه الواجهة عبارة عن نموذج أولي (Prototype) قيد التطوير، ولا تزال قيد الإضافة والتحسين لميزات متعددة. جميع الشاشات الحالية للعرض والمحاكاة فقط، ولا تمثل النظام النهائي أو وظائفه الفعلية.
""")
st.markdown("""
<div class="card" style="margin-bottom: 12px;">
<h1 style="text-align:center;" class="blue-title">نظام الملف الصحي الذكي</h1>
<h3 style="text-align:center; color:#305ed1;">منصتك الآمنة لإدارة وتلخيص معلوماتك الصحية</h3>
<p style="font-size:20px; text-align:center; margin:0 20px 18px 20px;">
مرحبًا بك في منصة الملف الصحي الذكي — سجل تاريخك الطبي خطوة بخطوة بسهولة وسرية تامة. كل ما تحتاجه لمتابعة صحتك وتجهيز ملخص واضح لطبيبك أو لنفسك في متناول يدك.
</p>
</div>
""", unsafe_allow_html=True)

# بطاقات موازية (بدون expander) للتعريف والمزايا وآلية العمل
st.markdown("""
<div class="cards-row">
  <div class="info-card">
    <h4 style="color:#2551a3;">📋 تعريف النظام</h4>
    <div style="font-size:17px;">
    نظام رقمي ذكي يرافقك في كل خطوة لرصد وحفظ بياناتك الصحية بتجربة عربية حديثة وسهلة.
    </div>
  </div>
  <div class="info-card">
    <h4 style="color:#2551a3;">⚡ مميزات أساسية</h4>
    <ul style="font-size:16px; margin-bottom:2px;">
    <li>حفظ بياناتك الطبية بسهولة وأمان</li>
    <li>واجهة عربية متوافقة مع جميع الأجهزة</li>
    <li>ملخص ذكي يمكنك طباعته أو مشاركته مع طبيبك</li>
    <li>إمكانية العودة وتعديل بياناتك بأي وقت</li>
    </ul>
  </div>
  <div class="info-card">
    <h4 style="color:#2551a3;">🚀 كيف يعمل؟</h4>
    <div style="font-size:17px;">
    1. أدخل بياناتك<br>
    2. أجب على الأسئلة الطبية<br>
    3. راجع ملخصك الصحي الشامل<br>
    4. عدّل أي خطوة متى شئت بسهولة
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
    <style>
    .stButton>button {
        font-size: 100px !important; border-radius: 80px !important;
        padding: 13px 0px !important;
        width: 320px !important; 
        margin: 18px auto 0 auto !important; display:block !important;
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
    if st.button("ابدأ الآن", key="start_btn"):
        st.switch_page("pages/1_تسجيل_الدخول.py")
        

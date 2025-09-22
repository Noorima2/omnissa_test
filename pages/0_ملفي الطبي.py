import streamlit as st
from datetime import date
from utils import apply_global_style, top_language_menu, auto_direction

apply_global_style()
auto_direction()
top_language_menu()

# ---------- استيراد تنسيق الصفحة الرئيسية ----------
st.markdown("""
<style>
.cards-row {
  display: flex;
  flex-wrap: wrap;
  gap: 22px;
  justify-content: center;
  margin-bottom: 16px;
}
.info-card {
  background: #f9fbff;
  border-radius: 24px;
  box-shadow: 0 3px 16px #bed5f7;
  padding: 28px 26px 20px 26px;
  margin-bottom: 15px;
  border: 1.5px solid #e3e9f3;
  min-width: 320px;
  max-width: 415px;
  width: 100%;
  direction: rtl;
  text-align: right;
  flex: 1 1 340px;
}
.section-title {
    color: #2551a3;
    font-size: 1.22rem;
    margin-bottom: 10px;
    font-weight: 700;
}
.item-row {
    padding: 4px 0 4px 0;
    font-size: 1.07rem;
    border-bottom: 1px dashed #e3e9f3;
    text-align: right;
}
@media (max-width: 1000px){
    .cards-row{ flex-direction:column; }
    .info-card{ max-width: 98vw;}
}
</style>
""", unsafe_allow_html=True)

# ---------- دالة عرض بيانات كل قسم ككارد info-card ----------
def card_html(title, data, icon=""):
    if not data: return ""
    content = f'<div class="info-card"><div class="section-title">{icon} {title}</div>'
    for k, v in data.items():
        if v:  # تجاهل القيم الفارغة
            content += f'<div class="item-row"><b>{k}:</b> {v}</div>'
    content += "</div>"
    return content

# ---------- جلب البيانات من session_state ----------
personal = st.session_state.get('personal_data', {})
past = st.session_state.get('past_history', {})
family = st.session_state.get('family_history', {})
social = st.session_state.get('social_history', {})
child = st.session_state.get('child_history', {})
gyn_obs = st.session_state.get('gyn_obs_history', {})
visits = st.session_state.get('visits', [])

# ---------- عنوان وبطاقة تعريفية ----------
st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/4712/4712038.png" class="big-logo">', unsafe_allow_html=True)
st.markdown('<div class="card" style="margin-bottom: 18px;"><h2 style="text-align:center;color:#2551a3;" class="blue-title" >📁 ملفك الطبي الكامل</h2><p style="text-align:center; font-size:17px;">راجع كل تفاصيل ملفك الصحي وقم بتعديله متى شئت.</p></div>', unsafe_allow_html=True)

if "success_message" in st.session_state:
    st.markdown("""
        <div style="
            background: #f9fbff;
            border-radius: 22px;
            box-shadow: 0 3px 16px #bed5f7;
            padding: 28px 32px 24px 32px;
            border: 1.5px solid #e3e9f3;
            direction: rtl;
            text-align: right;
            max-width: 520px;
            margin: 40px auto 30px auto;">
            <div style="color:#2551a3; font-size:1.17rem; font-weight:700; margin-bottom:13px;">
                ✅ تم استلام طلبك بنجاح
            </div>
            <div style="font-size:1.08rem;">
                تم إرسال جميع بياناتك للطبيب المختص.<br>
                سيتم مراجعة حالتك قريبًا وسيتم التواصل معك إذا لزم الأمر.<br>
                نتمنى لك الشفاء العاجل! إذا ظهرت لديك أعراض جديدة أو ازداد الألم بشكل كبير، لا تتردد في مراجعة الطوارئ.
            </div>
        </div>
    """, unsafe_allow_html=True)
    del st.session_state["success_message"]

# ---------- عرض الكاردات بشكل أفقي منظم ----------
cards_html = '<div class="cards-row">'
cards_html += card_html("بياناتك الأساسية", personal, "👤")
cards_html += card_html("التاريخ المرضي السابق", past, "🩺")
cards_html += card_html("التاريخ العائلي", family, "👨‍👩‍👦")
cards_html += card_html("التاريخ الاجتماعي", social, "🏡")
gender = personal.get("gender", "")
age = personal.get("age", 0)
try:
    age = int(age)
except:
    age = 0

if age < 15:
    cards_html += card_html("بيانات الطفل", child, "🧒")

if gender in ["أنثى"]:
    is_adult_female = gender and age >= 8
    cards_html += card_html("بيانات نسائية وولادة", gyn_obs, "🤱")

# --- كارد خاص بالتشخيصات والزيارات ---
if visits:
    visits_card = '<div class="info-card"><div class="section-title">📋 سجل الزيارات والتشخيصات</div>'
    for v in visits:
        visits_card += (
            f'<div class="item-row">'
            f'🗓️ <b>{v.get("date","")}</b> | <b>التشخيص:</b> {v.get("diagnosis","")}<br>'
            f'<span style="color:#555; font-size:0.99rem;"><b>ملاحظات:</b> {v.get("notes","")}</span>'
            '</div>'
        )
    visits_card += "</div>"
    cards_html += visits_card
else:
    cards_html += '<div class="info-card"><div class="section-title">📋 سجل الزيارات والتشخيصات</div><div class="item-row">لا توجد زيارات أو تشخيصات مسجلة بعد.</div></div>'

cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

# --- زر تعديل بياناتي بنفس أسلوب الصفحة الرئيسية ---

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
    if st.button("تعديل بياناتي",use_container_width=True):
        st.switch_page("pages/2_بياناتي الشخصية.py") 

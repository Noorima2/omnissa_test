import streamlit as st
import requests
import json
from utils import apply_global_style, top_language_menu, auto_direction

apply_global_style()
auto_direction()
top_language_menu()

st.markdown("""
<div class="card" style="max-width:530px; margin:auto; margin-top:22px; text-align:center;">
    <h2 class="blue-title" style="margin-bottom:13px;color:#2551a3;"> مراجعة الاعراض الاخرى</h2>
    <p style="font-size:17px;">يرجى تعبئة جميع التفاصيل الخاصة بأعراضك حتى نساعدك بأفضل صورة
</div>
""", unsafe_allow_html=True)

st.markdown("---")
ros_questions = {
    "أعراض عامة": ["حمى", "فقدان وزن", "ضعف عام", "تغير شهية", "تعرق ليلي", "تعب"],
    "اعراض متعلقة بالجهاز العصبي": ["صداع", "دوار", "إغماء", "تشنجات", "ضعف أو خدر الأطراف", "مشاكل بصرية", "مشاكل سمعية"],
    " اعراض متعلقة بالجهاز الهضمي": ["غثيان", "قيء", "ألم بالبطن", "إسهال", "إمساك", "دم بالبراز", "اصفرار الجلد/العين"],
    "اعراض متعلقة بالجهاز التنفسي ": ["سعال", "ضيق نفس", "بلغم", "صفير", "دم مع السعال", "ألم صدري مع التنفس"],
    " اعراض متعلقة بالجاهز القلبي ": ["خفقان", "ألم صدر", "تورم الأطراف", "دوخة مع الوقوف"],
    "اعراض متعلقة بالجهاز البولي  التناسلي  ": ["حرقة بول", "تكرار التبول", "دم بالبول", "تغير لون البول", "احتباس بول", "سلس بول"],
    "اعراض متعلقة بالجهاز العضلي الهيكلي ": ["آلام مفاصل", "تورم مفصل", "تيبس صباحي", "آلام عضلية"],
    "اعراض كتعلقة بالجانب الجلدي ": ["طفح جلدي", "حكة", "تقرحات", "تورم", "كدمات/نزيف غير مبرر"],
    "اعراض متعلقة بالغدد الصماء ": ["زيادة عطش", "زيادة بول", "زيادة أو فقدان وزن غير مبرر", "تغيرات حرارة", "تعرق مفرط"]
}

# 1. جلب من session_state إذا موجود
ros_saved = st.session_state.get("ros", {})
ros_details_saved = st.session_state.get("ros_details", {})

ros_answers = {}
ros_details = {}

for system, symptoms in ros_questions.items():
    with st.expander(system):
        for symptom in symptoms:
            radio_key = f"{system}_{symptom}"
            detail_key = f"details_{system}_{symptom}"

            default_val = ros_saved.get(f"{system} - {symptom}", "لا")
            has_symptom = st.radio(
                f"هل يوجد: {symptom}؟",
                ["لا", "نعم"],
                index=["لا", "نعم"].index(default_val),
                key=radio_key
            )
            ros_answers[f"{system} - {symptom}"] = has_symptom

            if has_symptom == "نعم":
                detail_val = ros_details_saved.get(f"{system} - {symptom}", "")
                details = st.text_input(
                    f"يرجى توضيح: {symptom}",
                    value=detail_val,
                    key=detail_key
                )
                ros_details[f"{system} - {symptom}"] = details

st.markdown("---")
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
        st.session_state["ros"] = ros_answers
        st.session_state["ros_details"] = ros_details
        st.switch_page("pages/4_تفاصيل الأعراض.py")
with col1:
    if st.button("متابعة", use_container_width=True):
        # --- اجمع بياناتك بهذا الشكل قبل الإرسال ---
        def safe_list(val):
            if isinstance(val, list): return val
            if val is None or val == "": return []
            if isinstance(val, str): return [v.strip() for v in val.split('\n') if v.strip()]
            return list(val) if val else []

        def safe_bool(val):
            if isinstance(val, bool): return val
            return str(val).strip() == "نعم"

        personal = st.session_state.get("personal_data", {})
        past = st.session_state.get("past_history", {})
        family = st.session_state.get("family_history", {})
        social = st.session_state.get("social_history", {})
        child = st.session_state.get("child_history", {})
        gyn_obs = st.session_state.get("gyn_obs_history", {})
        hopi = st.session_state.get("hopi_details", [])
        ros = st.session_state.get("ros", {})

        patient_data = {
            "name": personal.get("name", ""),
            "age": personal.get("age", 0),
            "gender": personal.get("gender", ""),
            "marital_status": personal.get("marital_status", ""),
            "occupation": personal.get("occupation", ""),
            "address": personal.get("address", ""),
            "source_info": personal.get("source_info", ""),
            "chief_complaint": st.session_state.get("chief_complaints", [""])[0],
            "complaint_duration": st.session_state.get("complaint_durations", [""])[0],
            "hopi": hopi,
            "ros": ros,

            # Past History
            "chronic_diseases": safe_list(past.get("chronic_diseases_details", "")),
            "surgeries": safe_list(past.get("surgeries_details", "")),
            "allergies": safe_list(past.get("allergies_details", "")),
            "medications": safe_list(past.get("medications_details", "")),
            "previous_admissions": safe_list(past.get("previous_admissions_details", "")),

            # Family
            "similar_conditions": safe_list(family.get("same_case", "")),
            "chronic_diseases_family": safe_list(family.get("family_diseases_details", "")),
            "consanguinity": safe_bool(family.get("consanguinity", "لا")),

            # Social
            "smoking": safe_bool(social.get("smoking", "لا")),
            "stimulants": safe_list(social.get("qat", "")),  
            "alcohol": safe_bool(social.get("alcohol", "لا")),
            "housing": social.get("housing", ""),
            "pets": safe_list(social.get("pets", "")),
            "travel": safe_bool(social.get("travel", "لا")),

            # Optional/children/gyn
            "gyn_obs": gyn_obs,
            "child_history": child,
            "immunizations": safe_list(child.get("vaccination", "")),
            "nutrition": child,  # أو استخلص nutrition history لو منفصلة
            "development": child, # أو استخلص developmental history لو منفصلة

            "visit_time": personal.get("date_of_visit", ""),
        }

        # ============== الإرسال =================
        try:
            if not st.session_state.get("patient_saved", False):
                res = requests.post("https://omnissatest-production.up.railway.app/add_patient", json=patient_data,verify=False)
                if res.status_code == 200:
                    st.session_state["patient_saved"] = True
                    st.session_state["success_message"] = "✅ تم استلام طلبك بنجاح\n\nتم إرسال جميع بياناتك للطبيب المختص.\nسيتم مراجعة حالتك قريبًا وسيتم التواصل معك إذا لزم الأمر.\nنتمنى لك الشفاء العاجل! إذا ظهرت لديك أعراض جديدة أو ازداد الألم بشكل كبير، لا تتردد في مراجعة الطوارئ."
                    st.switch_page("pages/0_ملفي الطبي.py")
            else:
                st.info("تم إرسال بياناتك مسبقًا.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الإرسال: {e}")
            st.warning("تحقق من الحقول الأساسية وأن جميع البيانات موجودة وليست None أو فارغة.")

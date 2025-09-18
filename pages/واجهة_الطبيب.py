import streamlit as st
import requests
import json
from collections import defaultdict
from utils import apply_global_style, top_language_menu, auto_direction

apply_global_style()
auto_direction()
top_language_menu()

st.info("""
**تنبيه هام:**  
هذه الواجهة عبارة عن نموذج أولي (Prototype) قيد التطوير، ولا تزال قيد الإضافة والتحسين لميزات متعددة. جميع الشاشات الحالية للعرض والمحاكاة فقط، ولا تمثل النظام النهائي أو وظائفه الفعلية.
""")
# ------ جلب المرضى ------
response = requests.get("https://omnissatest-production.up.railway.app/all_patients")
patients = response.json() if response.status_code == 200 else []
if not patients:
    st.info("لا يوجد مرضى حتى الآن.")
    st.stop()
# ---- ألوان الحالات ----
status_labels = {
    "Urgent":      {"label": "🔴 Urgent",      "color": "#e84d4d"},
    "Under Review":{"label": "🔵 Under Review", "color": "#3278ef"},
    "Completed":   {"label": "🟢 Completed",           "color": "#24b471"},
    "Follow-Up":   {"label": "🟠 Follow-Up",           "color": "#ffad2b"}
}

def get_status_label(status, red_flag=False, only_emoji=False):
    # إذا كان هناك red_flag أو Urgent، دائماً اعرض "🔴 حالة طارئة"
    item = status_labels["Urgent"] if red_flag or status == "Urgent" else status_labels.get(status, status_labels["Under Review"])
    label = item["label"]
    color = item["color"]
    emoji = label.split()[0]  # الإيموجي فقط (أول كلمة في label)
    if only_emoji:
        return emoji
    return label, color
# ---- CSS ----
st.markdown("""
<style>
.side-panel {background:#f7faff;border-radius:17px;padding:16px 8px 18px 8px;height:540px;overflow:auto;}
.main-panel{background:#f9fbff;border-radius:24px;padding:32px 38px 28px 38px;min-height:560px;box-shadow:0 3px 18px #bed5f7;border:1.5px solid #e3e9f3;}
.icd-btn{font-size:17px;padding:7px 18px 7px 18px;background:#2268c7;color:white;border-radius:9px;border:none;margin:7px 0;}
.icd-btn:hover{background:#174081;}
.cards-row {display: flex; flex-wrap: wrap; gap: 22px; justify-content: center; margin-bottom: 16px;}
.info-card {background: #f9fbff; border-radius: 22px; box-shadow: 0 3px 16px #bed5f7; padding: 26px 24px 16px 24px; margin-bottom: 15px; border: 1.5px solid #e3e9f3; min-width: 320px; max-width: 415px; width: 100%; direction: rtl; text-align: right; flex: 1 1 340px;}
.section-title {color: #2551a3; font-size: 1.13rem; margin-bottom: 10px; font-weight: 700;}
.item-row {padding: 4px 0 4px 0; font-size: 1.05rem; border-bottom: 1px dashed #e3e9f3; text-align: right;}
@media (max-width: 1000px){.cards-row{ flex-direction:column; }.info-card{ max-width: 98vw;}}
</style>
""", unsafe_allow_html=True)

col1, col2= st.columns([1,3.9])

# ==== A. قائمة المرضى ====
with col1:
    st.markdown('<h4 style="text-align:center;color:#2551a3;">طابور المرضى</h4>', unsafe_allow_html=True)
    for idx, p in enumerate(patients):
        emoji = get_status_label(p.get("status", "Under Review"), p.get("red_flag", False), only_emoji=True)
        btn_label = f'{emoji}  {p["name"]}'
        if st.button(btn_label, key=f"pbtn_{idx}"):
            st.session_state["selected_patient"] = idx
        st.markdown("<hr style='margin:6px 0 10px 0;'>", unsafe_allow_html=True)                
# ==== B. بيانات المريض الرئيسية =====
with col2:
    selected_idx = st.session_state.get("selected_patient", 0)
    patient = patients[selected_idx]
    label, color = get_status_label(patient.get("status", "Under Review"), patient.get("red_flag", False))

    # ---  بداية الكارد بيانات المريض ---
    st.markdown(f"""
      <div class="info-card"  style="margin-bottom:16px;max-width: 520px;">
        <h3 style="color:#2551a3; margin-bottom:18px;">بيانات المريض</h3>
        <div style="font-size:1.14rem;">
            <b>الاسم:</b> {patient["name"]}<br>
            <b>الحالة:</b> <span style="color:{color}; font-weight:700;">{label}</span><br>
            <b>العمر:</b> {patient["age"]} &nbsp; <b>الجنس:</b> {patient["gender"]} &nbsp;
            <br><b>الحالة الاجتماعية:</b> {patient["marital_status"]}
            <br><b>الشكوى:</b> {patient["chief_complaint"]}
            <br><b>وقت الدخول:</b> {patient.get("visit_time","---")}
        </div>
    """, unsafe_allow_html=True)
    
    #---------التفاصيل الكاملة للمريض----------------------------
    with st.expander(" التفاصيل الكاملة للمريض", expanded=False):
        
        # ------------------ 1. المعلومات الشخصية ------------------
        st.markdown('<hr style="margin:10px 0 16px 0;">', unsafe_allow_html=True)
        st.markdown("### 1. المعلومات الشخصية")
        st.markdown(f"""
        <div style="background:#f7faff;padding:13px 17px;border-radius:11px;margin-bottom:14px;">
        <small> الرقم الطبي:{patient.get("id","---")}</small><br> 
        <b>الاسم:</b> {patient.get("name","---")}<br>
        <b>العمر:</b> {patient.get("age","---")}<br>
        <b>الجنس:</b> {patient.get("gender","---")}<br>
        <b>الحالة الاجتماعية:</b> {patient.get("marital_status","---")}<br>
        <b>المهنة:</b> {patient.get("occupation","---")}<br>
        <b>العنوان:</b> {patient.get("address","---")}<br>
        <b>مصدر المعلومات:</b> {patient.get("source_info","---")}<br>
        </div>
        """, unsafe_allow_html=True)

       # --- عرض HOPI بشكل منسق ---
        st.markdown("### 2. قصة المرض الحالية (HOPI)")
        hopi_data = patient.get("hopi", [])
        if hopi_data and isinstance(hopi_data, list):
            for i, h in enumerate(hopi_data, 1):
                st.markdown(f"#### {i}. الشكوى: {h.get('complaint','---')} (المدة: {h.get('duration','---')})")
                hopi_html = """<table style="background:#f9fafd;width:97%;border-radius:7px;">
                    <tr><td style='font-weight:600'>المكان</td><td>{}</td></tr>
                    <tr><td style='font-weight:600'>بداية الأعراض</td><td>{}</td></tr>
                    <tr><td style='font-weight:600'>الوصف</td><td>{}</td></tr>
                    <tr><td style='font-weight:600'>الشدة</td><td>{}</td></tr>
                    <tr><td style='font-weight:600'>مدة العرض</td><td>{}</td></tr>
                    <tr><td style='font-weight:600'>أعراض مصاحبة</td><td>{}</td></tr>
                    <tr><td style='font-weight:600'>عوامل مريحة</td><td>{}</td></tr>
                    <tr><td style='font-weight:600'>عوامل مفاقمة</td><td>{}</td></tr>
                </table>""".format(
                    h.get("site",""),
                    h.get("onset",""),
                    h.get("character",""),
                    h.get("severity",""),
                    h.get("attack_duration"),
                    h.get("associated",""),
                    h.get("relieving",""),
                    h.get("exacerbating",""),
                )
                st.markdown(hopi_html, unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات مفصلة عن HOPI.")

        st.markdown("---")
        st.markdown("### 3.التاريخ المرضي والاجتماعي والعائلي")
        # --- عرض Past History بشكل منسق ---
        st.markdown("#### A.التاريخ المرضي السابق (Past History)")
        chronic_diseases = patient.get("chronic_diseases", [])
        surgeries = patient.get("surgeries", [])
        previous_admissions = patient.get("previous_admissions", [])
        allergies = patient.get("allergies", [])
        medications = patient.get("medications", [])

        if chronic_diseases or surgeries or previous_admissions or allergies or medications:
            past_html = """
            <table style="background:#f9fafd;width:97%;border-radius:7px;">
                <tr><td style='font-weight:600'>الأمراض المزمنة</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>جراحات سابقة</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>نقل دم</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>حساسية</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>أدوية حالية</td><td>{}</td></tr>
            </table>
            """.format(
                "، ".join(chronic_diseases) if chronic_diseases else "---",
                "، ".join(surgeries) if surgeries else "---",
                "، ".join(previous_admissions) if previous_admissions else "---",
                "، ".join(allergies) if allergies else "---",
                "، ".join(medications) if medications else "---"
            )
            st.markdown(past_html, unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات مفصلة عن التاريخ المرضي السابق.")

        # # --- عرض Family History ---
        st.markdown("#### B.التاريخ العائلي (Family History)")
        chronic_diseases_family = patient.get(" chronic_diseases_family",[])
        similar_conditions = patient.get("similar_conditions",[])
        consanguinity = patient.get("consanguinity",[])
        if  chronic_diseases_family or similar_conditions or consanguinity:
            family_html = """
            <table style="background:#f9fafd;width:97%;border-radius:7px;">
                <tr><td style='font-weight:600'>أمراض مزمنة بالعائلة</td><td>{}</td></tr>
                <tr><td style='font-weight:600'> أمراض مشابهة بالعائلة</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>درجة القرابة</td><td>{}</td></tr>
            </table>
            """.format(
                "، ".join(chronic_diseases_family) if chronic_diseases_family else "---",
                "، ".join(similar_conditions) if similar_conditions else "---",
                "، ".join(consanguinity) if consanguinity else "---",
            )
            st.markdown(past_html, unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات مفصلة عن التاريخ العائلي.")

        # --- عرض Socioeconomic History ---
        st.markdown("#### C.التاريخ الاجتماعي (Socioeconomic History)")
        # smoking = patient.get("smoking",[])
        stimulants = patient.get("stimulants ",[])
        alcohol = patient.get("alcohol",[])
        housing = patient.get("housing",[])
        pets= patient.get("pets",[])
        travel= patient.get("travel",[])

        if  stimulants or alcohol or housing or pets or travel:
            socio_html = """
            <table style="background:#f9fafd;width:97%;border-radius:7px;">
                <tr><td style='font-weight:600'>التدخين</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>مواد منشطة</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>تعاطي المخدرات او الكحول</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>ظروف السكن</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>الحيوانات الاليفة</td><td>{}</td></tr>
                <tr><td style='font-weight:600'>تاريخ السفر</td><td>{}</td></tr>
            </table>
            """.format(
                # "، ".join(smoking) if smoking else "---",
                "، ".join(stimulants) if stimulants else "---",
                "، ".join(alcohol) if alcohol else "---",
                "، ".join(housing) if housing else "---",
                "، ".join(pets) if pets else "---",
                "، ".join(travel) if travel else "---",     
            )
            st.markdown(socio_html, unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات مفصلة عن التاريخ الاجتماعي.")

        st.markdown("### 4. مراجعة الأنظمة (ROS)")
        ros = patient.get("ros", {})
        if ros and isinstance(ros, dict):
            # تجميع الأعراض تحت كل جهاز تلقائيًا
            sections = defaultdict(list)
            for k, v in ros.items():
                # توقع أن الشكل هو: "الجهاز - العرض"
                if " - " in k:
                    section, symptom = k.split(" - ", 1)
                else:
                    section, symptom = "أخرى", k
                sections[section.strip()].append((symptom.strip(), v))

            # ترتيب ظهور الأجهزة حسب التكرار أو الترتيب الأبجدي
            for i, (section, items) in enumerate(sections.items()):
                st.markdown(f"#### {chr(65+i)}. {section}")  # مثل A. B. C.
                ros_html = """<table style="background:#f9fafd;width:340px;min-width:180px;border-radius:7px;direction:rtl;font-size:1.08rem;">
                    <tr><th style='background:#e7f1fb;width:110px;font-weight:700'>العرض</th>
                        <th style='background:#e7f1fb;font-weight:700'>الإجابة</th></tr>
                """
                for symptom, val in items:
                    ros_html += f"<tr><td>{symptom}</td><td>{val}</td></tr>"
                ros_html += "</table>"
                st.markdown(ros_html, unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات مفصلة عن مراجعة الأنظمة (ROS).")

    # ---- 1. ملخص Gemini AI ----
    if st.button("توليد ملخص طبي", key="doctor_ai_btn"):
        with st.spinner("جاري توليد الملخص الذكي..."):
            api_url = "https://omnissatest-production.up.railway.app/doctor_ai_summary"
            response = requests.post(api_url, json={
                "patient_data": json.dumps(patient, ensure_ascii=False),
                "lang": st.session_state.get("lang", "ar")
            })
            if response.status_code == 200:
                doctor_ai_summary = response.json().get("doctor_ai_summary", "")
                patient["doctor_ai_summary"] = doctor_ai_summary
                st.success("تم توليد ملخص الطبيب!")
            else:
                st.error("حدث خطأ في توليد الملخص.")

    if patient.get("doctor_ai_summary"):
        st.markdown(
            f'''<div style="background:#f7faff;padding:13px 17px;border-radius:11px;margin-bottom:14px;">
            <b>ملخص لأهم النقاط (غير إلزامي للطبيب):</b><br>
            <span style="color:#377dff;">{patient["doctor_ai_summary"]}</span>
            <div style="color:#be2a2a; margin-top:6px; font-size:0.95rem;">.ملاحظة: لا يعتبر هذا التشخيص نهائياً ⚠️</div>
            </div>''', unsafe_allow_html=True)
    else:
        st.info("اضغط توليد ملخص سريري للطبيب للحصول على ملخص سريري AI تشخيصي.", icon="🤖")

    # ---- 2. التشخيصات ICD-11 ----
    st.markdown('<hr style="margin:10px 0 16px 0;">', unsafe_allow_html=True)
    # --- البحث في ICD-11 ---
    if 'icd_results' not in st.session_state:
        st.session_state['icd_results'] = []

    icd_query = st.text_input("ابحث عن تشخيص تفريقي (يمكنك استخدام الشكوى أو تعديلها):", value=patient.get("chief_complaint", ""), key="icd_query")
    st.markdown("""تنبيه: اكتب اسم العرض باللغة الانجليزية. مثل
                    سعال= cough, 
                    الم في الصدر = chest pain ..الخ""")
    if st.button("ابحث في ICD-11", key="icd11_btn"):
        with st.spinner("يتم جلب اقتراحات التشخيص..."):
            api_url = "https://omnissatest-production.up.railway.app/icd11_search"
            resp = requests.post(api_url, json={"query": icd_query, "lang": "en"})
            try:
                data = resp.json()
            except Exception:
                st.error(f"الرد من API ليس JSON: {resp.text}")
                st.stop()
            icd_results = []
            if isinstance(data, dict):
                if data.get("error", False):
                    st.error(f"خطأ ICD-11: {data.get('errorMessage', 'حدث خطأ غير معروف')}")
                    st.stop()
                entities = data.get("destinationEntities", data.get("entities", []))
                if not entities: 
                    st.warning("لم يتم العثور على تشخيصات ICD-11 مطابقة.")
                for e in entities[:7]:
                    code = e.get("theCode", "")
                    title = e.get("title")
                    if isinstance(title, dict):
                        title = title.get("value", "")
                    elif title is None:
                        title = ""
                    title = title.replace("<em class='found'>", "<b style='color:#174081'>").replace("</em>", "</b>")
                    icd_results.append({"code": code, "title": title})
            # حفظ النتائج في السيشن ستيت
            st.session_state['icd_results'] = icd_results

    # ---- عرض النتائج من session_state ----
    icd_results = st.session_state.get('icd_results', [])

    if icd_results:
        st.markdown("#### اختر التشخيص النهائي (اضغط على زر [اعتماد التشخيص]):")
        for i, res in enumerate(icd_results):
            btn_key = f"accept_icd_{i}"
            st.markdown(
                f"""
                <div class="info-card" style="background:#eef8ff;margin-bottom:18px;text-align:center;">
                    <div style="font-weight:700;font-size:1.13rem;margin-bottom:4px;">{res["title"]}</div>
                    <div style="color:#2268c7;font-size:1.07rem;">ICD-11: {res["code"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # زر اعتماد التشخيص
            if st.button("اعتماد التشخيص", key=btn_key):
                st.session_state["diagnosis_final"] = res["title"]
                st.session_state["diagnosis_code"] = res["code"]

    # إدخال يدوي كخيار منفصل
    manual_diag = st.text_input("التشخيص النهائي:", value=st.session_state.get("diagnosis_final", ""), key="diag_final_input")
    manual_code = st.text_input("كود ICD-11 (اختياري):", value=st.session_state.get("diagnosis_code", ""), key="diag_final_code")

    diagnosis_final = manual_diag
    diagnosis_code = manual_code

    treatment_plan = st.text_area("الخطة العلاجية (يملؤها الطبيب):", value=patient.get("treatment_plan", ""), height=90)
    notes = st.text_area("ملاحظات الطبيب:", value=patient.get("notes", ""), height=60)
    status_options = list(status_labels.keys())
    current_status = patient.get("status", "Under Review")
    if current_status not in status_options:
        current_status = "Under Review"
    new_status = st.selectbox("تغيير حالة المريض:",options=status_options,index=status_options.index(current_status))
    if st.button("حفظ التشخيص النهائي والخطة", key="save_status_btn"):
        patient_id = patient.get("id")
        if patient_id:
            url = f"https://omnissatest-production.up.railway.app/update_patient/{patient_id}"
            updated_patient = patient.copy()
            updated_patient.update({
                "diagnosis_final": diagnosis_final,
                "diagnosis_code": diagnosis_code,
                "treatment_plan": treatment_plan,
                "notes": notes,
                "status": new_status,
            })
            res = requests.put(url, json=updated_patient)
            if res.status_code == 200:
                st.success("تم حفظ التشخيص النهائي والخطة بنجاح!")
            else:
                st.error(f"فشل في تحديث بيانات المريض. الكود: {res.status_code} — {res.text}")
        else:
            st.error("معرف المريض غير موجود!")
    st.markdown('</div>', unsafe_allow_html=True)

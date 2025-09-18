import streamlit as st
from datetime import date
import pandas as pd
from utils import apply_global_style, top_language_menu, auto_direction

apply_global_style()
auto_direction()
top_language_menu()

def fix_session_dict(key):
    val = st.session_state.get(key)
    if not isinstance(val, dict):
        st.session_state[key] = {}
    return st.session_state[key]

for key in ["child_history", "nutrition_history", "immunization_history", "developmental_history","gyn_obs_saved"]:
    fix_session_dict(key)

st.markdown("""
<div class="card" style="max-width:530px; margin:auto; margin-top:22px; text-align:center;">
    <h2 class="blue-title" style="margin-bottom:13px;color:#2551a3;"> بياناتي الأساسية</h2>
    <p style="font-size:17px;">يرجى تعبئة جميع الحقول بدقة \n\n الحقول التي تحمل <span style="color:#d02a2a;">*</span> مطلوبة</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
# ==========================بياناتي الأساسية:====================================
with st.expander("📝 الرجاء تعبئة بياناتك الأساسية", expanded=True):
    today = date.today()
    age = st.number_input("العمر", min_value=0, max_value=120, value=st.session_state.get("age",0))
    st.session_state["age"] = age
    # حساب تاريخ الميلاد التلقائي (قابل للتعديل)
    default_dob = date(today.year - age, today.month, today.day) if age else today
    date_of_birth = st.date_input("تاريخ الميلاد *", value=default_dob, help="تحدد تلقائيًا من العمر. يمكنك التعديل إذا احتجت.")

    name = st.text_input("اسم المريض", value=st.session_state.get("name", ""),help="يرجى كتابة اسمك الكامل.")
    st.session_state["name"] = name

    gender = st.selectbox("الجنس *", ["","ذكر", "أنثى"])
    st.session_state["gender"]= gender

    address = st.text_input("مكان السكن *", value=st.session_state.get("address", ""), help="يرجى كتابة العنوان الكامل.")
    st.session_state["address"] = address

    birthplace = st.text_input("مكان الميلاد", value=st.session_state.get("birthplace", ""), help="مثال: المدينة، القرية، المستشفى...")
    st.session_state["birthplace"] = birthplace

    marital_status = st.selectbox("الحالة الاجتماعية", ["","أعزب/عزباء", "متزوج/ة", "أرمل/ة", "مطلق/ة"], 
                                index=0 if st.session_state.get("marital_status", "أعزب/عزباء") == "أعزب/عزباء" else 1 )
    st.session_state["marital_status"] = marital_status

    occupation = st.text_input("المهنة", value=st.session_state.get("occupation", ""), help="مثال: طالب، موظف، ربة منزل...")
    st.session_state["occupation"] = occupation

    source_info = st.selectbox("من يقدم المعلومات؟", ["","المريض", "الأب", "الأم", "مرافق", "آخر"],
                            index=0 if st.session_state.get("source_info", "المريض") == "المريض" else 1)
    st.session_state["source_info"] = source_info

    date_of_visit = st.date_input("تاريخ الزيارة/الدخول", value=today)


# --- الحقول المطلوبة ---
required_fields = all([
    name.strip() != "",
    gender.strip() != "",
    address.strip() != "",
    age > 0
])

# جلب البيانات المحفوظة
past_saved = st.session_state.get("past_history", {})
family_saved = st.session_state.get("family_history", {})
social_saved = st.session_state.get("social_history", {})
child_saved = st.session_state.get("child_history", {})
gyn_obs_saved = st.session_state.get("gyn_obs_history", {})
child_saved = st.session_state.get("child_history", {})
immun_saved = st.session_state.get("immunization_history", {})
nutri_saved = st.session_state.get("nutrition_history", {})
dev_saved = st.session_state.get("developmental_history", {})
# معايير
age = st.session_state.get("age",0)
gender = st.session_state.get("gender", "")
is_child = age < 15
is_female = gender == "أنثى"
is_adult_female = is_female and age >= 8
is_adult_male = gender == "ذكر" and age >= 15
#==========================التاريخ المرضي=================================================
with st.expander("🩺 التاريخ المرضي السابق", expanded=False):
    chronic_diseases = st.radio(
        "هل تعاني من أمراض مزمنة؟*", 
        ["لا", "نعم"],
        index=["لا", "نعم"].index(past_saved.get("chronic_diseases", "لا")), 
        key="chronic"
    )
    chronic_diseases_details = ""
    if chronic_diseases == "نعم":
        chronic_diseases_details = st.text_area(
            "يرجى ذكر تفاصيل الأمراض المزمنة",
            value=past_saved.get("chronic_diseases_details", ""),
            key="chronic_diseases_details"
        )

    surgeries = st.radio(
        "هل أجريت عمليات جراحية من قبل؟*", 
        ["لا", "نعم"],
        index=["لا", "نعم"].index(past_saved.get("surgeries", "لا")), 
        key="surg"
    )
    surgeries_details = ""
    if surgeries == "نعم":
        surgeries_details = st.text_area(
            "يرجى ذكر تفاصيل العمليات الجراحية ",
            value=past_saved.get("surgeries_details", ""),
            key="surgeries_details"
        )
    
    medications = st.radio(
        "هل تتناول أي أدوية بانتظام؟*", 
        ["لا", "نعم"],
        index=["لا", "نعم"].index(past_saved.get("medications", "لا")), 
        key="med"
    )
    medications_details = ""
    if medications == "نعم":
        medications_details = st.text_area(
            "يرجى ذكر تفاصيل الأدوية",
            value=past_saved.get("medications_details", ""),
            key="medications_details"
        )

    allergies = st.radio(
        "هل لديك حساسية من أدوية/أطعمة/مواد؟*", 
        ["لا", "نعم"],
        index=["لا", "نعم"].index(past_saved.get("allergies", "لا")), 
        key="allergies"
    )
    allergies_details = ""
    if allergies == "نعم":
        allergies_details = st.text_area(
            "يرجى ذكر تفاصيل الحساسية",
            value=past_saved.get("allergies_details", ""),
            key="allergies_details"
        )
    
    previous_admissions = st.radio(
        "هل سبق أن تم تنويمك بالمستشفى؟*", 
        ["لا", "نعم"],
        index=["لا", "نعم"].index(past_saved.get("previous_admissions", "لا")), 
        key="admissions"
    )
    previous_admissions_details = ""
    if previous_admissions == "نعم":
        previous_admissions_details = st.text_area(
            "يرجى ذكر سبب\ تفاصيل تنويمك",
            value=past_saved.get("previous_admissions_details", ""),
            key="previous_admissions_details"
        )  

    blood_transfusion = st.radio("هل سبق أن نقل لك دم؟*", ["لا", "نعم"],
                                 index=["لا", "نعم"].index(past_saved.get("blood_transfusion", "لا")), key="transf")
    transfusion_details = ""
    if blood_transfusion == "نعم":
        transfusion_details = st.text_area("يرجى ذكر سبب نقل الدم/الكمية/التاريخ*", value=past_saved.get("transfusion_details", ""), key="transf_det")

#=================================التاريخ العائلي=====================================================================
with st.expander(" 👨‍👩‍👧‍👦  التاريخ العائلي", expanded=False):
    family_diseases = st.radio(
        "هل يوجد أمراض مزمنة أو وراثية في العائلة؟*", 
        ["لا", "نعم"],
        index=["لا", "نعم"].index(family_saved.get("family_diseases", "لا")), 
        key="family_diseases"
    )
    family_diseases_details = ""
    if family_diseases == "نعم":
        family_diseases_details = st.text_area(
            "يرجى ذكر تفاصيل الأمراض المزمنة أو الوراثية في العائلة",
            value=family_saved.get("family_diseases_details", ""),
            key="family_diseases_details"
        )
    consanguinity = st.radio("هل هناك قرابة بين الوالدين؟*", ["لا", "نعم"],
                             index=["لا", "نعم"].index(family_saved.get("consanguinity", "لا")), key="consang")
    same_case = st.radio("هل هناك حالات مشابهة في العائلة؟*", ["لا", "نعم"],
                             index=["لا", "نعم"].index(family_saved.get("same_case", "لا")), key="same_case")
    similar_conditions=""
    if same_case =="نعم":
        similar_conditions= st.text_input(
            "  يرجى ذكر تفاصيل حالات مشابهة في العائلة",
            value=family_saved.get("similar_conditions",""),
            key="similar_conditions"

        )
    early_death = st.radio("هل هناك حالات وفيات مبكرة؟*", ["لا", "نعم"],
                             index=["لا", "نعم"].index(family_saved.get("early_death", "لا")), key="early_death")
    
#==================================التاريخ الاجتماعي========================================================
with st.expander("🏡 التاريخ الاجتماعي", expanded=False):
    smoking = st.radio("هل تدخن؟*", ["لا", "نعم"],
                       index=["لا", "نعم"].index(social_saved.get("smoking", "لا")), key="smok")
    stimulants = st.radio("هل تستخدم مواد منشطة؟*", ["لا", "نعم"],
                   index=["لا", "نعم"].index(social_saved.get("stimulants", "لا")), key="stimulants")
    stimulants_details = ""
    if stimulants == "نعم":
        stimulants_details = st.text_input(
            "يرجى ذكر تفاصيل المادة المستخدمة",
            value=social_saved.get("stimulants_details", ""),
            key="stimulants_details",
            help="مثل ادوية الـ ADHD, المنبهات مثل الشاي والقهوة, القات وغيرها "
        )
    alcohol = st.radio("هل تتعاطى الكحول أو المخدرات؟*", ["لا", "نعم"],
                       index=["لا", "نعم"].index(social_saved.get("alcohol", "لا")), key="alco")
    pets = st.radio("هل لديك حيوانات أليفة بالمنزل؟*", ["لا", "نعم"],
                       index=["لا", "نعم"].index(social_saved.get("pets", "لا")), key="pets")
    pets_details = ""
    if pets == "نعم":
        pets_details = st.text_input(
            "يرجى ذكر الحيوان الذي تربيه",
            value=social_saved.get("pets_details",""),
            key="pets_details",
        )
    travel = st.radio("هل سافرت مؤخرًا؟*", ["لا", "نعم"],
                       index=["لا", "نعم"].index(social_saved.get("travel", "لا")), key="travel")
    housing = st.text_input("مكان ونوع السكن (منزل، شقة...)*", value=social_saved.get("housing", ""), key="house")
    social_support = st.text_input("من يساعدك في المنزل أو من تعيش معه؟*", value=social_saved.get("social_support", ""), key="support")
    water = st.text_input("ما مصدر المياه في المنزل؟*", value=social_saved.get("water", ""), key="water")

#========================== التحقق من الحقول المطلوبة====================
all_required_filled = all([
    chronic_diseases.strip() != "",
    surgeries.strip() != "",
    medications.strip() != "",
    allergies.strip() != "",
    previous_admissions.strip() != "",
    family_diseases.strip() != "",
    consanguinity.strip() != "",
    early_death.strip() != "",
    smoking.strip() != "",
    stimulants.strip() != "",
    alcohol.strip() != "",
    housing.strip() != "",
    social_support.strip() != "",
    pets.strip() != "",
    travel.strip() != "",
    water.strip() != ""
])

# ============ حذف الشروط: الحقول للأطفال والنساء تظهر دائماً أثناء التطوير ============
order_siblings = ""
education_level = ""
feeding_type = ""
feeding_start = ""
formula_name = ""
nutri_saved = ""
weaning = ""
food_issues = ""
immunization_complete = ""
immunization_details = ""
vaccination = ""
development = ""
walking_age = ""
talking_age = ""
school_performance = ""
delay_signs = ""

if is_child:

    with st.expander("🧒 جميع تفاصيل الطفل الصحية", expanded=False):
        st.markdown("#### 👨‍👩‍👦 معلومات عائلية وأكاديمية")
        order_siblings = st.text_input(
            "ترتيب الطفل بين الأخوة (مثال: الثاني)", value=st.session_state.get("order_siblings", ""), help="مثال: الأول، الثاني، الثالث..."
        )
        st.session_state["order_siblings"] = order_siblings
        education_level = st.text_input(
            "مستوى التعليم (للطالب أو الأب/الأم)", value=st.session_state.get("education_level", ""), help="مثال: ابتدائي، ثانوي، جامعي..."
        )
        st.markdown("---")
        st.session_state["education_level"] = education_level
        # 🍼 الرضاعة/التغذية
        # st.markdown("#### 🍼 الرضاعة والتغذية")
        # feeding_type = st.radio(
        #     "نوع الرضاعة في أول سنة", ["","طبيعية فقط", "صناعية فقط", "مختلط"],
        #     index=["طبيعية فقط", "صناعية فقط", "مختلط"].index(nutri_saved.get("feeding_type", "طبيعية فقط")), key="feed_type"
        # )
        # feeding_start = st.text_input(
        #     "متى بدأت الرضاعة؟", value=nutri_saved.get("feeding_start", ""), key="feed_start"
        # )
        # formula_name = ""
        # if feeding_type != "طبيعية فقط":
        #     formula_name = st.text_input(
        #         "ما اسم الحليب الصناعي المستخدم؟", value=nutri_saved.get("formula_name", ""), key="form_name"
        #     )
        # weaning = st.text_input(
        #     "متى بدأ الفطام؟ (إدخال أطعمة صلبة)", value=nutri_saved.get("weaning", ""), key="weaning"
        # )
        # food_issues = st.text_area(
        #     "هل يوجد مشاكل في الشهية أو رفض أطعمة معينة أو ترجيع أو إسهال مزمن أو إمساك مزمن؟",
        #     value=nutri_saved.get("food_issues", ""), key="food_issues"
        # )

        st.markdown("---")
        # 💉 التطعيمات
        st.markdown("#### 💉 تاريخ التطعيمات")
        immunization_complete = st.radio(
            "هل التطعيمات كاملة حسب جدول وزارة الصحة؟", ["نعم", "لا"],
            index=["نعم", "لا"].index(immun_saved.get("immunization_complete", "نعم")), key="immu_comp"
        )
        immunization_details = st.text_area(
            "يرجى ذكر التطعيمات التي تم أخذها أو التي تم تأجيلها أو نسيانها",
            value=immun_saved.get("immunization_details", ""), key="immu_det"
        )
        vaccination = st.text_area(
            "سجل تطعيمات الطفل*", value=child_saved.get("vaccination", ""), key="vacc"
        )

        st.markdown("---")
        # 🚼 التطور والنمو
        st.markdown("#### 🚼 تاريخ النمو والتطور")
        development = st.text_area(
            "هل يوجد تأخر أو مشاكل في التطور؟*", value=child_saved.get("development", ""), key="dev"
        )
        walking_age = st.text_input(
            "في أي عمر بدأ الطفل يمشي؟", value=dev_saved.get("walking_age", ""), key="walk_age"
        )
        talking_age = st.text_input(
            "في أي عمر بدأ الطفل ينطق كلمات واضحة؟", value=dev_saved.get("talking_age", ""), key="talk_age"
        )
        school_performance = st.text_input(
            "هل أداء الطفل الدراسي طبيعي؟", value=dev_saved.get("school_performance", ""), key="school_perf"
        )
        delay_signs = st.text_area(
        "هل توجد أي علامات تأخر في التطور الحركي أو العقلي؟", value=dev_saved.get("delay_signs", ""), key="delay_signs"
    )

# ========================للنساء==========================

lmp_input_method=""
lmp=""
menarche_ages=""
menarche =""
cycle_pattern=""
pregnancies=""
deliveries=""
abortions=""
contraception=""
contraception_details=""

if is_adult_female:
    with st.expander("🤱 تاريخ نسائي وولادة", expanded=False):
        lmp_input_method = st.radio(
            "كيف تود إدخال تاريخ آخر دورة شهرية؟", ["اختيار من التقويم", "إدخال يدوي"], 
            key="lmp_method",
            index=["اختيار من التقويم", "إدخال يدوي"].index(gyn_obs_saved.get("lmp_method", "اختيار من التقويم"))
        )
        if lmp_input_method == "اختيار من التقويم":
            lmp_date = st.date_input(
                "تاريخ آخر دورة شهرية*", 
                value=None if not gyn_obs_saved.get("lmp") else pd.to_datetime(gyn_obs_saved["lmp"]),
                key="lmp_date"
            )
            lmp = str(lmp_date) if lmp_date else ""
        else:
            lmp = st.text_input("اكتبي تاريخ آخر دورة شهرية*", value=gyn_obs_saved.get("lmp", ""), key="lmp_manual")

        menarche_ages = list(range(8, 18))
        menarche = st.selectbox(
            "عمر بدء الدورة الشهرية*", 
            menarche_ages, 
            index=menarche_ages.index(int(gyn_obs_saved.get("menarche", 12))) if gyn_obs_saved.get("menarche") else 4,
            key="menarche"
        )
        
        cycle_pattern = st.text_input(
            "نمط الدورة الشهرية*", value=gyn_obs_saved.get("cycle_pattern", ""), key="cycle"
        )

        pregnancies = st.number_input(
            "عدد مرات الحمل", min_value=0, max_value=20, step=1, 
            value=int(gyn_obs_saved.get("pregnancies", 0)), key="pregs"
        )
        deliveries = st.number_input(
            "عدد مرات الولادة", min_value=0, max_value=20, step=1, 
            value=int(gyn_obs_saved.get("deliveries", 0)), key="deliveries"
        )
        abortions = st.number_input(
            "عدد مرات الإجهاض", min_value=0, max_value=20, step=1, 
            value=int(gyn_obs_saved.get("abortions", 0)), key="abortions"
        )

        contraception = st.radio(
            "هل تستخدم وسائل منع الحمل؟", 
            ["لا", "نعم"],
            index=["لا", "نعم"].index(gyn_obs_saved.get("contraception", "لا")), 
            key="contraception"
        )
        contraception_details = ""
        if contraception == "نعم":
            contraception_details = st.text_input(
                "يرجى ذكر الوسيلة",
                value=gyn_obs_saved.get("contraception_details", ""),
                key="contraception_details"
            )

#==============================الازرار=======================
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
    if st.button("رجوع",use_container_width=True):
        st.switch_page("pages/1_تسجيل_الدخول.py") 
with col1:
    if st.button("متابعة",use_container_width=True):
        if not required_fields:
            st.warning("يرجى تعبئة جميع الحقول الإجبارية بعلامة *")
        else:
            st.session_state['personal_data'] = {
                "name": name, "age": age, "date_of_birth": str(date_of_birth), "gender": gender,
                "address": address, "birthplace": birthplace, "marital_status": marital_status,
                "occupation": occupation, "source_info": source_info, "date_of_visit": str(date_of_visit),
            }
            # حفظ بيانات التاريخ المرضي السابق
            st.session_state['past_history'] = {
                "chronic_diseases": chronic_diseases,
                "chronic_diseases_details": chronic_diseases_details,
                "surgeries": surgeries,
                "surgeries_details": surgeries_details,
                "medications": medications,
                "medications_details": medications_details,
                "allergies": allergies,
                "allergies_details": allergies_details,
                "previous_admissions": previous_admissions,
                "previous_admissions_details": previous_admissions_details,
                "blood_transfusion": blood_transfusion,
                "transfusion_details": transfusion_details
            }
            # حفظ بيانات التاريخ العائلي
            st.session_state['family_history'] = {
                "family_diseases": family_diseases,
                "family_diseases_details": family_diseases_details,
                "consanguinity": consanguinity,
                "same_case": same_case,
                "early_death": early_death
            }
            # حفظ بيانات التاريخ الاجتماعي
            st.session_state['social_history'] = {
                "smoking": smoking,
                "stimulants": stimulants,
                "alcohol": alcohol,
                "pets": pets,
                "travel": travel,
                "housing": housing,
                "social_support": social_support,
                "water": water
            }
            # بيانات النساء:
            gyn_obs_data = {
                "lmp_method": lmp_input_method,
                "lmp": lmp,
                "menarche": menarche,
                "cycle_pattern": cycle_pattern,
                "pregnancies": pregnancies,
                "deliveries": deliveries,
                "abortions": abortions,
                "contraception": contraception,
                "contraception_details": contraception_details
            }
            st.session_state['gyn_obs_history'] = gyn_obs_data
            # حفظ بيانات الطفل (يمكن التوسع هنا لأي حقل جديد)
            st.session_state['child_history'] = {
                "order_siblings": order_siblings,
                "education_level": education_level,
                "feeding_type": feeding_type,
                "feeding_start": feeding_start,
                "formula_name": formula_name,
                "weaning": weaning,
                "food_issues": food_issues,
                "immunization_complete": immunization_complete,
                "immunization_details": immunization_details,
                "vaccination": vaccination,
                "development": development
            }
            st.session_state['immunization_history'] = {
                "immunization_complete": immunization_complete,
                "immunization_details": immunization_details
            }
            st.session_state['nutrition_history'] = {
                "feeding_type": feeding_type,
                "feeding_start": feeding_start,
                "formula_name": formula_name,
                "weaning": weaning,
                "food_issues": food_issues
            }
            st.session_state['developmental_history'] = {
                "development": development,
                "walking_age": walking_age,
                "talking_age": talking_age,
                "school_performance": school_performance,
                "delay_signs": delay_signs
            }
            st.switch_page("pages/3_مشكلتي الرئيسية.py")

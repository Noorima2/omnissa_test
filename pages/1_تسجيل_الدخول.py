import streamlit as st
from utils import apply_global_style, top_language_menu, auto_direction

apply_global_style()
auto_direction()
top_language_menu()

# ستايل الزر يكون دائماً بنفس الكلاس
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

# كارد واحد فيه كل شيء (الشعار، العنوان، التعليمات، الراديو، الحقول، الزر)
with st.container():
    st.markdown("""
    <div class="card" style="max-width:430px; margin:auto; margin-top:24px; text-align:center;">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712038.png" class="big-logo">
        <h2 class="blue-title" style="margin-bottom:14px;">تسجيل الدخول</h2>
        <p style="font-size:17px; margin-bottom:7px;">يرجى اختيار نوع المستخدم وتعبئة البيانات:</p>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    role = st.radio(
        "",
        ["مريض", "طبيب", "مسؤول نظام"],
        key="role_select",
        horizontal=True
    )

    action_triggered = False

    if role == "مريض":
        st.markdown('<h4 style="color:#2a5eb8; margin-bottom:7px; margin-top:11px;">👤 دخول المريض</h4>', unsafe_allow_html=True)
        email = st.text_input("البريد الإلكتروني ", key="patient_email")
        btn = st.button("متابعة", key="patient_continue", use_container_width=True)
        # نضيف كلاس start-btn بعد رسم الزر (بعد تنفيذ الدالة) عبر جافاسكريبت:
        st.markdown("""
            <script>
            let btns = window.parent.document.querySelectorAll('button[kind="secondary"]');
            btns.forEach(btn => { if (btn.innerText.includes("متابعة")) {btn.classList.add('start-btn');}});
            </script>
        """, unsafe_allow_html=True)
        if btn:
            st.session_state["user_role"] = "patient"
            st.switch_page("pages/2_بياناتي الشخصية.py")

    elif role == "طبيب":
        st.markdown('<h4 style="color:#2a5eb8; margin-bottom:7px; margin-top:11px;">🩺 دخول الطبيب</h4>', unsafe_allow_html=True)
        username = st.text_input("اسم المستخدم", key="doctor_user")
        password = st.text_input("كلمة المرور", type="password", key="doctor_pass")
        btn = st.button("دخول الطبيب", key="doctor_login", use_container_width=True)
        st.markdown("""
            <script>
            let btns = window.parent.document.querySelectorAll('button[kind="secondary"]');
            btns.forEach(btn => { if (btn.innerText.includes("دخول الطبيب")) {btn.classList.add('start-btn');}});
            </script>
        """, unsafe_allow_html=True)
        if btn:
            st.session_state["user_role"] = "doctor"
            st.switch_page("pages/واجهة_الطبيب.py")

    else:
        st.markdown('<h4 style="color:#2a5eb8; margin-bottom:7px; margin-top:11px;">🔑 دخول المسؤول</h4>', unsafe_allow_html=True)
        admin_user = st.text_input("اسم المسؤول", key="admin_user")
        admin_pass = st.text_input("كلمة المرور", type="password", key="admin_pass")
        btn = st.button("دخول المسؤول", key="admin_login", use_container_width=True)
        st.markdown("""
            <script>
            let btns = window.parent.document.querySelectorAll('button[kind="secondary"]');
            btns.forEach(btn => { if (btn.innerText.includes("دخول المسؤول")) {btn.classList.add('start-btn');}});
            </script>
        """, unsafe_allow_html=True)
        if btn:
            st.session_state["user_role"] = "admin"
            st.success("تم الدخول كمسؤول نظام (ميزة تحت التطوير)")

    st.markdown('</div>', unsafe_allow_html=True)
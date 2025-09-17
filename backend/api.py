#backend/api.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # إضافة مسار المجلد الحالي إلى sys.path
from backend.knowledge_base import PatientHistory,save_patients_to_file, patients_db
import uuid
import google.generativeai as genai
import os
import requests

app = FastAPI()

# ===================== ADD PATIENT =====================
@app.post("/add_patient")
async def add_patient(request: Request):
    data = await request.json()
    data["id"] = str(uuid.uuid4())
    # **p.dict(),
    patient = PatientHistory(**data)
    patients_db.append(patient)
    save_patients_to_file()   # احفظ للملف مباشرة
    return JSONResponse(content={"status": "ok", "id": patient.id})

# ===================== GET ALL PATIENTS =====================
@app.get("/all_patients")
async def all_patients():
    # يرجع كل المرضى كـ dict
    return [patient.dict() for patient in patients_db]

# ===================== GET SINGLE PATIENT BY ID =====================
@app.get("/patient/{pid}")
async def get_patient(pid: str):
    patient = next((p for p in patients_db if p.id == pid), None)
    if not patient:
        return JSONResponse(content={"error": "not found"}, status_code=404)
    return patient.dict()

# ===================== UPDATE PATIENT BY ID =====================
@app.put("/update_patient/{pid}")
async def update_patient(pid: str, request: Request):
    data = await request.json()
    for i, p in enumerate(patients_db):
        if p.id == pid:
            # تحديث بيانات المريض
            updated = p.copy(update=data)
            patients_db[i] = updated
            save_patients_to_file()
            return {"status": "updated"}
    raise HTTPException(status_code=404, detail="Patient not found")

# ===================== AI SUMMARY FOR DOCTOR =====================
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDWShjSeT4aCAJsWP-kBf5hW6Qh3dQ3oVU")
genai.configure(api_key=GEMINI_KEY)
PROMPT_DOCTOR_AR = """
أنت طبيب متخصص تكتب ملخص سريري احترافي لطبيب آخر.

المطلوب:
- اكتب ملخصًا سريريًا مختصرًا يشمل فقط الشكوى الرئيسية ومدتها، والأعراض والعلامات السريرية التي أدخلها المريض (بدون ذكر الأعراض أو البيانات غير المدخلة).
- ركز على أهم النقاط الحمراء (Red Flags) المرتبطة بهذه الحالة، واذكر التشخيصات التفريقية (Differential Diagnoses) الأكثر ترجيحًا، مع أهم الفحوصات الموصى بها.
- إذا هناك أعراض أو بيانات مهمة متوقعة ولم يقم المريض بتعبئتها (ولها علاقة مباشرة بالحالة)، نبه الطبيب إلى ضرورة مراجعتها أو سؤال المريض عنها.
- لا تكرر بيانات المريض العامة مثل الاسم، العمر، الجنس، أو تاريخ الزيارة.
- قدم الملخص بلغة مهنية موجزة ومباشرة للطبيب، وبدون تفاصيل زائدة أو إعادة صياغة بيانات المريض بشكل حرفي.

بيانات المريض المدخلة:
{patient_data}

مثال للصياغة:
- الشكوى الرئيسية ومدتها: ...
- الأعراض السريرية الحالية: ...
- العلامات الحمراء: ...
- التشخيصات التفريقية: ...
- ملاحظات/تنبيهات للطبيب (عن البيانات الناقصة المهمة): ...
- الفحوصات المقترحة: ...

"""


@app.post("/doctor_ai_summary")
async def doctor_ai_summary(request: Request):
    data = await request.json()
    patient_data = data.get("patient_data", "")
    lang = data.get("lang", "ar")
    prompt = PROMPT_DOCTOR_AR.format(patient_data=patient_data)
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    result = response.text
    return JSONResponse(content={"doctor_ai_summary": result})

# ===================== ICD-11 API Integration =====================
ICD11_CLIENT_ID = "a6fe71b5-ef45-4f75-a407-a22c2e455e4c_cd91409b-ac61-4835-befe-f61df11ed27d"
ICD11_CLIENT_SECRET = "1hlRMfYGcDRPj/NHqb8pF6XUpmLhqtyCJlTkTHwCiy0="

def get_icd11_token():
    url = "https://icdaccessmanagement.who.int/connect/token"
    data = {
        "client_id": ICD11_CLIENT_ID,
        "client_secret": ICD11_CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "icdapi_access"
    }
    # أضف verify=False هنا
    response = requests.post(url, data=data, verify=False)
    return response.json().get("access_token")


class ICD11SearchRequest(BaseModel):
    query: str
    lang: str = "en"         # en أو ar
    releaseId: str = "2025-01"
    linearization: str = "mms"

@app.post("/icd11_search")
async def icd11_search(data: ICD11SearchRequest):
    token = get_icd11_token()
    if not token:
        return JSONResponse(
            content={"error": "Failed to get ICD-11 token!"},
            status_code=500
        )
    url = "https://id.who.int/icd/release/11/2023-01/mms/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Accept-Language": data.lang,
        "API-Version": "v2"
    }
    params = {
        "q": data.query,
        "useFlexisearch": True,
        "flatResults": True,
        # لا تضف chapterFilter إلا إذا كنت متأكد
    }
    response = requests.get(url, headers=headers, params=params, verify=False)
    print("WHO ICD-11 Search:", response.status_code, response.text)
    try:
        result = response.json()
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to parse: {str(e)}", "raw": response.text},
            status_code=response.status_code
        )


from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import tempfile
import os
import requests
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://edu-vector-site.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

reader = easyocr.Reader(['ru', 'en'], download_enabled=True, gpu=False)

def ocr_image(file_path: str) -> str:
    results = reader.readtext(file_path, detail=0, paragraph=True)
    return "\n".join(results)

def query_llm(prompt: str) -> str:
    HF_TOKEN = os.getenv("HF_TOKEN")
    if not HF_TOKEN:
        return "Ошибка: HF_TOKEN не задан"
    
    API_URL = "https://api-inference.huggingface.co/models/IlyaGusev/saiga_llama3"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt, "options": {"wait_for_model": True}},
            timeout=30
        )
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "Ошибка генерации")
        else:
            return f"Ошибка ИИ: {str(result)}"
    except Exception as e:
        return f"Ошибка запроса: {str(e)}"

@app.post("/analyze")
async def analyze_work(
    assignment: UploadFile = File(...),
    works: List[UploadFile] = File(...),
    subject: str = Form(...)
):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            assignment_path = os.path.join(tmpdir, assignment.filename)
            with open(assignment_path, "wb") as f:
                f.write(await assignment.read())
            assignment_text = ocr_image(assignment_path)[:500]

            works_texts = []
            for work in works:
                work_path = os.path.join(tmpdir, work.filename)
                with open(work_path, "wb") as f:
                    f.write(await work.read())
                works_texts.append(ocr_image(work_path)[:300])

            prompt = f"""Проанализируй работы учеников по предмету: {subject}.
Условие задания: "{assignment_text}"
Работы учеников: {" ".join(works_texts)}

Ответь строго в формате:

1️⃣ Ошибки в работе
- ...

2️⃣ Что нужно исправить
- ...

3️⃣ Соответствие заданию
- ..."""

            return {"result": query_llm(prompt)}
    except Exception as e:
        return {"error": f"Ошибка: {str(e)}"}
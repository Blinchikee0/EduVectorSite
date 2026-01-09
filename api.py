from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://edu-vector-site.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def mock_ocr(filename: str) -> str:
    """Имитация OCR: возвращает текст в зависимости от имени файла"""
    if "assignment" in filename.lower():
        return "Решите задачу: Найдите площадь треугольника со сторонами 3, 4, 5."
    elif "perfect" in filename.lower() or "ideal" in filename.lower():
        return "Площадь треугольника = 6. Ответ: 6."
    elif "error" in filename.lower():
        return "Площадь треугольника = 12. Ответ: 12."
    else:
        return "Площадь треугольника = 6."

def query_llm(prompt: str) -> str:
    HF_TOKEN = os.getenv("HF_TOKEN")
    if not HF_TOKEN:
        return "Ошибка: HF_TOKEN не задан в Render"
    
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
            text = result[0].get("generated_text", "")
            if prompt.strip() in text:
                text = text.replace(prompt.strip(), "", 1).strip()
            return text
        else:
            return "ИИ не вернул анализ. Попробуйте снова."
    except Exception as e:
        return f"Ошибка ИИ: {str(e)}"

@app.post("/analyze")
async def analyze_work(
    assignment: UploadFile = File(...),
    works: list[UploadFile] = File(...),
    subject: str = Form(...)
):
    try:
        assignment_text = mock_ocr(assignment.filename)
        works_texts = [mock_ocr(work.filename) for work in works]
        
        prompt = f"""Ты — эксперт-учитель по предмету "{subject}".
Задание ученикам: "{assignment_text}"
Работы учеников: {" | ".join(works_texts)}

Проанализируй каждую работу. Если ошибок нет — чётко скажи: "Ошибок нет. Работа выполнена верно."
Если есть ошибки — укажи их конкретно, ссылаясь на условие задания.

Ответь строго в формате:

1️⃣ Ошибки в работе
- ...

2️⃣ Что нужно исправить ученику
- ...

3️⃣ Соответствие заданию
- ..."""

        ai_response = query_llm(prompt)
        return {"result": ai_response}
        
    except Exception as e:
        return {"error": f"Системная ошибка: {str(e)}"}
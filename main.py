from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.student.router import router as student_router
from src.app.teacher.router import router as teacher_router
from src.app.auth.router import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/", tags=["Home"])
async def health_test():
    return {'status': "ok"}


app.include_router(auth_router)
app.include_router(student_router)
app.include_router(teacher_router)

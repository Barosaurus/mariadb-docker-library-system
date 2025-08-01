from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models.database import get_db, Base, engine
from routes import books

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bibliotheksverwaltungssystem API",
    description="REST API für digitale Bibliotheksverwaltung mit MariaDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router, prefix="/api/books", tags=["books"])

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Bibliotheksverwaltungssystem API", "docs": "/docs"}
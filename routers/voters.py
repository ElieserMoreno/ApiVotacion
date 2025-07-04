from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Voter, Candidate  # Importa Candidate para validación cruzada
from schemas import Voter as VoterSchema, VoterCreate
from database import get_db

router = APIRouter(
    prefix="/voters",
    tags=["voters"]
)

# Crear votante con validación cruzada para que no sea candidato
@router.post("/", response_model=VoterSchema)
def create_voter(voter: VoterCreate, db: Session = Depends(get_db)):
    # Validar que no exista correo duplicado
    db_voter = db.query(Voter).filter(Voter.email == voter.email).first()
    if db_voter:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Validar que no exista el mismo document_id como candidato (opcional si tienes campo document_id)
    if hasattr(voter, "document_id"):
        candidate_check = db.query(Candidate).filter(Candidate.document_id == voter.document_id).first()
        if candidate_check:
            raise HTTPException(status_code=400, detail="This document_id is already registered as a candidate")

    new_voter = Voter(
        name=voter.name,
        email=voter.email,
        document_id=getattr(voter, "document_id", None)  # Solo si tu modelo lo tiene
    )
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return new_voter

# Obtener todos los votantes
@router.get("/", response_model=list[VoterSchema])
def get_voters(db: Session = Depends(get_db)):
    return db.query(Voter).all()

# Obtener un votante por ID
@router.get("/{voter_id}", response_model=VoterSchema)
def get_voter(voter_id: int, db: Session = Depends(get_db)):
    voter = db.query(Voter).filter(Voter.id == voter_id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Voter not found")
    return voter

# Eliminar un votante por ID
@router.delete("/{voter_id}")
def delete_voter(voter_id: int, db: Session = Depends(get_db)):
    voter = db.query(Voter).filter(Voter.id == voter_id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Voter not found")
    db.delete(voter)
    db.commit()
    return {"detail": "Voter deleted successfully"}

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Candidate, Voter  # Voter solo si necesitas validación cruzada
from schemas import Candidate as CandidateSchema, CandidateCreate
from database import get_db

router = APIRouter(
    prefix="/candidates",
    tags=["candidates"]
)

# Crear candidato con validación cruzada para que no esté como votante
@router.post("/", response_model=CandidateSchema)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    db_candidate = db.query(Candidate).filter(Candidate.email == candidate.email).first()
    if db_candidate:
        raise HTTPException(status_code=400, detail="Email already registered as candidate")
    
    # Opcional: evitar que un mismo documento sea votante
    if hasattr(candidate, "document_id"):
        voter_check = db.query(Voter).filter(Voter.document_id == candidate.document_id).first()
        if voter_check:
            raise HTTPException(status_code=400, detail="This document_id is already registered as a voter")

    new_candidate = Candidate(
        name=candidate.name,
        email=candidate.email,
        document_id=getattr(candidate, "document_id", None)
    )
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate

# Obtener todos los candidatos
@router.get("/", response_model=list[CandidateSchema])
def get_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).all()

# Obtener un candidato por ID
@router.get("/{candidate_id}", response_model=CandidateSchema)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

# Eliminar un candidato por ID
@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db.delete(candidate)
    db.commit()
    return {"detail": "Candidate deleted successfully"}

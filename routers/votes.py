from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Vote, Voter, Candidate
from schemas import Vote as VoteSchema, VoteCreate
from database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["votes"]
)

# Crear voto: verificar que votante y candidato existen y que el votante no haya votado antes
@router.post("/", response_model=VoteSchema)
def create_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    voter = db.query(Voter).filter(Voter.id == vote.voter_id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Voter not found")
    
    candidate = db.query(Candidate).filter(Candidate.id == vote.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    existing_vote = db.query(Vote).filter(Vote.voter_id == vote.voter_id).first()
    if existing_vote:
        raise HTTPException(status_code=400, detail="Voter has already voted")
    
    new_vote = Vote(
        voter_id=vote.voter_id,
        candidate_id=vote.candidate_id
    )
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote

# Obtener todos los votos
@router.get("/", response_model=list[VoteSchema])
def get_votes(db: Session = Depends(get_db)):
    return db.query(Vote).all()

# Obtener voto por ID
@router.get("/{vote_id}", response_model=VoteSchema)
def get_vote(vote_id: int, db: Session = Depends(get_db)):
    vote = db.query(Vote).filter(Vote.id == vote_id).first()
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    return vote
# Obtener estadísticas de la votación
@router.get("/statistics")
def get_vote_statistics(db: Session = Depends(get_db)):
    # Obtener total de votos
    total_votes = db.query(Vote).count()

    if total_votes == 0:
        return {"message": "No votes yet", "statistics": []}

    # Obtener total de votos por candidato
    candidates = db.query(Candidate).all()

    stats = []
    for candidate in candidates:
        candidate_votes = db.query(Vote).filter(Vote.candidate_id == candidate.id).count()
        percentage = (candidate_votes / total_votes) * 100
        stats.append({
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
            "votes": candidate_votes,
            "percentage": round(percentage, 2)
        })

    # Obtener total de votantes que han votado
    total_voters_voted = db.query(Vote.voter_id).distinct().count()

    return {
        "total_votes": total_votes,
        "total_voters_voted": total_voters_voted,
        "statistics": stats
    }

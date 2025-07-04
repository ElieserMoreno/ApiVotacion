# schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class VoterCreate(BaseModel):
    name: str
    email: EmailStr

class Voter(BaseModel):
    id: int
    name: str
    email: EmailStr
    has_voted: bool

    class Config:
        orm_mode = True


class CandidateCreate(BaseModel):
    name: str
    party: Optional[str] = None

class Candidate(BaseModel):
    id: int
    name: str
    party: Optional[str] = None
    votes: int

    class Config:
        orm_mode = True


class VoteCreate(BaseModel):
    voter_id: int
    candidate_id: int

class Vote(BaseModel):
    id: int
    voter_id: int
    candidate_id: int

    class Config:
        orm_mode = True

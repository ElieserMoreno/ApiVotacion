from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    votes = relationship("Vote", back_populates="candidate")  # One candidate to many votes

class Voter(Base):
    __tablename__ = "voters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

    # One-to-one with Vote
    vote = relationship("Vote", back_populates="voter", uselist=False)

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    voter_id = Column(Integer, ForeignKey("voters.id"), unique=True, nullable=False)

    candidate = relationship("Candidate", back_populates="votes")
    voter = relationship("Voter", back_populates="vote")

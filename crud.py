from sqlalchemy.orm import Session
import models


#VOTANTE
def create_voter(db: Session, name: str, email: str):
    # validar que no exista como candidato
    candidate = db.query(models.Candidate).filter(models.Candidate.name == name).first()
    if candidate:
        raise HTTPException(status_code=400, detail="Este usuario ya es candidato")

    voter = models.Voter(name=name, email=email)
    db.add(voter)
    db.commit()
    db.refresh(voter)
    return voter


#CANDIDATO
def create_candidate(db: Session, name: str, party: str):
    # validar que no exista como votante
    voter = db.query(models.Voter).filter(models.Voter.name == name).first()
    if voter:
        raise HTTPException(status_code=400, detail="Este usuario ya es votante")

    candidate = models.Candidate(name=name, party=party)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


#voto
from fastapi import HTTPException

def create_vote(db: Session, voter_id: int, candidate_id: int):
    voter = db.query(models.Voter).filter(models.Voter.id == voter_id).first()
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

    if not voter:
        raise HTTPException(status_code=404, detail="Votante no existe")

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no existe")

    if voter.has_voted:
        raise HTTPException(status_code=400, detail="El votante ya votó")

    vote = models.Vote(voter_id=voter_id, candidate_id=candidate_id)
    db.add(vote)

    voter.has_voted = True

    if candidate.votes is None:
        candidate.votes = 0

    candidate.votes += 1

    db.commit()
    db.refresh(vote)

    return vote
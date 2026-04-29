from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#conexion a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#crear votante
@app.post("/voters")
def create_voter(voter: schemas.VoterCreate, db: Session = Depends(get_db)):
    return crud.create_voter(db, voter.name, voter.email)

#obtener todos los votantes
@app.get("/voters")
def get_voters(db: Session = Depends(get_db)):
    return db.query(models.Voter).all()

#obtener votante por ID
@app.get("/voters/{voter_id}")
def get_voter(voter_id: int, db: Session = Depends(get_db)):
    return db.query(models.Voter).filter(models.Voter.id == voter_id).first()

#eliminar votante
@app.delete("/voters/{voter_id}")
def delete_voter(voter_id: int, db: Session = Depends(get_db)):
    voter = db.query(models.Voter).filter(models.Voter.id == voter_id).first()
    if voter:
        db.delete(voter)
        db.commit()
        return {"message": "Votante eliminado"}
    return {"error": "Votante no encontrado"}

#crear candidato
@app.post("/candidates")
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    return crud.create_candidate(db, candidate.name, candidate.party)


#obtener todos los candidatos
@app.get("/candidates")
def get_candidates(db: Session = Depends(get_db)):
    return db.query(models.Candidate).all()


#obtener candidato por ID
@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()


#eliminar candidato
@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if candidate:
        db.delete(candidate)
        db.commit()
        return {"message": "Candidato eliminado"}
    return {"error": "Candidato no encontrado"}

#registrar voto
@app.post("/votes")
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    return crud.create_vote(db, vote.voter_id, vote.candidate_id)

#obtener todos los votos
@app.get("/votes")
def get_votes(db: Session = Depends(get_db)):
    return db.query(models.Vote).all()

#estadistica
@app.get("/votes/statistics")
def get_statistics(db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    total_votes = sum(c.votes or 0 for c in candidates)

    results = []

    for c in candidates:
        votes = c.votes or 0
        percentage = (votes / total_votes * 100) if total_votes > 0 else 0

        results.append({
            "candidate": c.name,
            "votes": votes,
            "percentage": round(percentage, 2)
        })

    total_voters_voted = db.query(models.Voter).filter(models.Voter.has_voted == True).count()

    return {
        "total_votes": total_votes,
        "total_voters_voted": total_voters_voted,
        "results": results
    }

#resultados
@app.get("/results")
def get_results(db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    candidates = db.query(models.Candidate).order_by(models.Candidate.votes.desc()).all()
    return [
        {
            "name": c.name,
            "party": c.party,
            "votes": c.votes
        }
        for c in candidates
    ]

from typing import Optional, List, Tuple

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import crud, models, schemas
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.logger import logger as fastapi_logger
import logging

app = FastAPI()
logger = logging.getLogger("uvicorn")
fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel(logger.level)
logger.error("API Started")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/movies")
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return False


@app.put("/movies/director/")
def update_movie_director(mid: int, sid: int, db: Session = Depends(get_db)):
    crud.update_movie_director(db=db,movie_id=mid, director_id=sid)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star not found")
    return db_movie


@app.post("/movies/actor", response_model = schemas.MovieDetail)
def add_movie_actor(mid: int, sid: int, db: Session = Depends(get_db)):
    db_movie =  crud.add_movie_actor(db=db,movie_id=mid, star_id=sid)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star not found")
    return db_movie


@app.put("/movies/actors", response_model = schemas.MovieDetail)
def update_movie_actors(mid: int, sids: List[int], db: Session = Depends(get_db)):
    db_movie =  crud.update_movie_actors(db=db,movie_id=mid, stars_id=sids)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie or Star not found")
    return db_movie

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/movies", response_model=List[schemas.Movie])
def read_all_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

@app.get("/movies/by_id/{movie_id}", response_model=schemas.MovieDetail)
def read_one_movie(movie_id:int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id = movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="movie not found")
    return db_movie

### POST CREATE MOVIE

@app.post("/movies/", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db=db, movie=movie)

### PUT UPDATE MOVIE

@app.put("/movies/", response_model=schemas.Movie)
def update_movie(movie: schemas.Movie, db: Session = Depends(get_db)):
    db_movie = crud.update_movie(db, movie=movie)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie to update not found")
    return db_movie

### DELETE MOVIE

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.delete_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie to delete not found")
    return db_movie


@app.get("/movies/by_title/{movie_title}" , response_model=List[schemas.Movie])
def read_movies_by_title(movie_title: str, db: Session = Depends(get_db)):
    movies = crud.get_movies_by_title(db=db, movie_title=movie_title)
    if movies is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movies

@app.get("/movies/by_titlepart/{movie_title}", response_model=List[schemas.Movie])
def read_movies_by_titlepart(movie_title: str, db: Session = Depends(get_db)):
    movies = crud.get_movies_by_titlepart(db=db, movie_title=movie_title)
    if movies is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movies

@app.get("/movies/by_rangeyear", response_model=List[schemas.Movie])
def get_movies_by_range_year( year_min: Optional[int] = None,  year_max: Optional[int] = None, db: Session = Depends(get_db)):
    movies = crud.get_movies_by_range_year(db=db, year_min=year_min, year_max=year_max)
    if movies == []:
        raise HTTPException(status_code=404, detail="No movies found for theses years")
    return movies


@app.get("/movies/by_director", response_model=List[schemas.Movie])
def read_movies_by_director(endname: str, db: Session = Depends(get_db)):
    movies = crud.get_movies_by_director_endname(db=db, endname=endname)
    if movies == []:
        raise HTTPException(status_code=404, detail="No movies found for this director ")
    return movies

@app.get("/movies/by_movie_directed/{id_movie}", response_model=schemas.Star)
def get_director_by_id_movie(id_movie: int, db: Session = Depends(get_db)):
    info_director = crud.get_director_by_id_movie(db=db, id_movie=id_movie)
    if info_director is None:
        raise HTTPException(status_code=404, detail="Movie not found or director not informed")
    return info_director.director

@app.get("/movies/by_actor", response_model=List[schemas.Movie])
def read_movies_by_actor(name: str, db: Session = Depends(get_db)):
    movies = crud.get_movies_by_actor_endname(db=db, endname=name)
    if movies == []:
        raise HTTPException(status_code=404, detail="Movies not found with this actor")
    return movies


@app.get("/movies/count_by_year")
def get_stats_movies_by_year(db: Session = Depends(get_db)) -> List[Tuple[int, int, int, int, int]]:
    return crud.get_stats_movies_by_year(db=db)

@app.get("/movies/count_by_year_dic", response_model = List[schemas.MovieStat])
def get_stats_movies_by_year_dic(db: Session = Depends(get_db)):
    return crud.get_stats_movies_by_year_dic(db=db)

# --- API Rest for Stars ---

@app.get("/stars", response_model=List[schemas.Star])
def read_stars(skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    stars = crud.get_stars(db, skip=skip, limit=limit)
    return stars

@app.get("/stars/by_id/{star_id}", response_model=schemas.Star)
def read_star(star_id: int, db: Session = Depends(get_db)):
    db_star = crud.get_star(db, star_id=star_id)
    if db_star is None:
        raise HTTPException(status_code=404, detail="Star to read not found")
    return db_star

@app.get("/stars/by_name", response_model=List[schemas.Star])
def read_stars_by_name(name: str, db: Session = Depends(get_db)):
    stars = crud.get_stars_by_name(db=db, name=name)
    if stars == []:
        raise HTTPException(status_code=404, detail="Star not found")
    return stars

@app.get("/stars/by_endname", response_model=List[schemas.Star])
def read_stars_by_endname(name: str, db: Session = Depends(get_db)):
    stars = crud.get_stars_by_endname(db=db, name=name)
    return stars

@app.get("/stars/by_birthyear/{year}", response_model=List[schemas.Star])
def read_stars_by_birthyear(year: int, db: Session = Depends(get_db)):
    stars = crud.get_stars_by_birthyear(db=db, year=year)
    return stars

### POST CREATE STAR

@app.post("/stars/", response_model=schemas.Star)
def add_star(star: schemas.StarCreate, db: Session = Depends(get_db)):
    return crud.create_star(db=db, star=star)


### PUT UPDATE STAR

@app.put("/stars/", response_model=schemas.Star)
def update_star(star: schemas.Star, db: Session = Depends(get_db)):
    db_star = crud.update_star(db, star=star)
    if db_star is None:
        raise HTTPException(status_code=404, detail="Stars to update not found")
    return db_star

### DELETE STAR

@app.delete("/stars/{star_id}", response_model=schemas.Star)
def delete_star(star_id: int, db: Session = Depends(get_db)):
    db_star = crud.delete_star(db, star_id=star_id)
    if db_star is None:
        raise HTTPException(status_code=404, detail="Stars to delete not found")
    return db_star

@app.get("/stars/by_movie_directed_title", response_model=List[schemas.Star])
def read_stars_by_movie_directed_title(t: str, db: Session = Depends(get_db)):
    return crud.get_star_director_movie_by_title(db=db, title=t)


@app.get("/stars/stats_movie_by_director")
def read_stats_movie_by_director(minc: Optional[int]=10, db: Session = Depends(get_db)):
    return crud.get_stats_movie_by_director(db=db, min_count=minc)

### STATS PAR ACTEURS

@app.get("/stars/stats_movie_by_actor", response_model=List[schemas.ActorStat])
def read_stats_movie_by_actor(minc: Optional[int] = 10, db: Session = Depends(get_db)):
    stats = crud.get_stats_movie_by_actor(db=db, min_count=minc)
    if stats is None:
        raise HTTPException(status_code=404, detail="Error on the recovery of the statistics of the actors")
    return stats

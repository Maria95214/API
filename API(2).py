from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
from itertools import count

app = FastAPI(
    title="Notes API",
    version="1.0.0"
)

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=1000)

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int

notes: List[Note] = []
id_generator = count(1)

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

@app.get(
    "/api/v1/notes",
    response_model=List[Note]
)
def get_notes():
    return notes

@app.get(
    "/api/v1/notes/{note_id}",
    response_model=Note
)
def get_note(note_id: int):
    note = next((n for n in notes if n.id == note_id), None)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note

@app.post(
    "/api/v1/notes",
    response_model=Note,
    status_code=status.HTTP_201_CREATED
)
def create_note(note: NoteCreate):
    new_note = Note(
        id=next(id_generator),
        title=note.title,
        content=note.content
    )
    notes.append(new_note)
    return new_note

@app.put(
    "/api/v1/notes/{note_id}",
    response_model=Note
)
def update_note(note_id: int, updated_note: NoteCreate):
    for index, note in enumerate(notes):
        if note.id == note_id:
            updated = Note(
                id=note_id,
                title=updated_note.title,
                content=updated_note.content
            )
            notes[index] = updated
            return updated

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Note not found"
    )

@app.delete(
    "/api/v1/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note.id == note_id:
            notes.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Note not found"
    )
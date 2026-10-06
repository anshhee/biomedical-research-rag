from pydantic import BaseModel, Field


class DocumentSection(BaseModel):
    heading: str | None = None
    text: str = Field(..., min_length=1)

    



class Document(BaseModel):
    document_id : str 
    title : str 
    source: str
    file_type: str 




class DcoumentChunk(BaseModel):
    chunk_id : str 
    document_id : str 
    text: str = Field(..., min_length=1)
    source: str 
    section: str | None = None 
    page: int | None = None 
    chunk_index: int 

    
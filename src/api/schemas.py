from pydantic import BaseModel , Field

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length = 1,
        max_length = 2000
    )
    document_id: str | None = None 


class Source(BaseModel):
    doc_id : str
    chunk_id: str
    text:str
    source : str



class AskResponse(BaseModel):
    answer : str
    status : str
    model_used : str 
    sources : list[Source]
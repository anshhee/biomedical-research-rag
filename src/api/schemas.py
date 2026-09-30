from pydantic import BaseModel , Field

class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length = 1,
        max_length = 2000
    )


class Source(BaseModel):
    doc_id : str
    chunk_id: str
    text:str
    source : str



class AskResponse(BaseModel):
    answer : str
    status : str
    sources : list[Source]
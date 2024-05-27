from pydantic import BaseModel


class Response(BaseModel):
    existing_data: dict
    extracted_data: dict
    discrepancies: dict

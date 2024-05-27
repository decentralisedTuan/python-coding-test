from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
import pandas as pd

from ..services.services import pdf_service, data_file
from ..utils.compare_data import compare_data
from ..models.response import Response

router = APIRouter()


@router.post('/compare', response_model=Response)
async def compare_pdf(company_name: Annotated[str, Form()], file: Annotated[UploadFile, File()]):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    file_location = f"assets/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    try:
        extracted_data = pdf_service.extract(file_location)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    df = pd.read_csv(data_file)
    if company_name not in df['Company Name'].values:
        raise HTTPException(status_code=404, detail="Company not found in database.")

    existing_data = df[df['Company Name'] == company_name].to_dict(orient="records")[0]

    discrepancies = compare_data(existing_data, extracted_data)

    result = {
        "existing_data": existing_data,
        "extracted_data": extracted_data,
        "discrepancies": discrepancies
    }

    return JSONResponse(content=result)

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
import pandas as pd
from pdf_service import PdfService

app = FastAPI()
pdf_service = PdfService(key="TEST_KEY")
data_file = "data/database.csv"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/compare')
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


def compare_data(existing_data, extracted_data):
    discrepancies = {}

    for key in existing_data:
        if key in extracted_data and str(existing_data[key]) != str(extracted_data[key]):
            discrepancies[key] = {
                "existing": existing_data[key],
                "extracted": extracted_data[key]
            }
    return discrepancies

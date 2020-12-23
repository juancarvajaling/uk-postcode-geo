import shutil
import csv
from fastapi import FastAPI, File, UploadFile
from file_loader.utils import set_postcode_from_geo

app = FastAPI()


@app.post("/postcode-geo/")
async def create_upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    file.close()

    await set_postcode_from_geo(file_name)
    return {"filename": file_name}

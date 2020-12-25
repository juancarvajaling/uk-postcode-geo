import shutil
from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import JSONResponse
from file_loader.utils import process_coordinates_file

app = FastAPI()


@app.post("/postcode-geo")
async def create_upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    with open(file_name, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    await file.close()

    try:
        errors = await process_coordinates_file(file_name)
    except UnicodeDecodeError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'The file could not be read'}
        )

    if errors:
        return errors

    return {'message': 'the file was processed successfully'}

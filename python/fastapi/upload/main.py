from fastapi import FastAPI, UploadFile, Request
from fastapi.templating import Jinja2Templates
from process_file import read_and_normalise, split_generator

templates = Jinja2Templates(directory="templates") 

app = FastAPI()

@app.get("/upload")
def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})  # Render the form


@app.post("/upload")
async def upload(file: UploadFile):
    try:
        waveform = read_and_normalise(file.file)
        waveform = [chunk.tolist() for chunk in split_generator(waveform)]
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Remove the object from memory
        await file.close()
        del file
    
    return {"message": "File processed successfully", "waveform": len(  waveform ) }

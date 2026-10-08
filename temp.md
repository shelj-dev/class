# FastAPI File Upload and Static File Serving Example

### Step 1: Install Required Package

FastAPI requires `python-multipart` to parse uploaded files and form data:

```bash
pip install python-multipart
```

### Step 2: Code Implementation (`main.py`)

```python
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 1. Ensure uploads folder exists
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 2. Static file setup
# URL: http://127.0.0.1:8000/files/<filename>
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# 3. Simple file upload API
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    filename = file.filename

    if not filename:
        raise HTTPException(status_code=400, detail="File not selected")

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File Uploaded successfully",
        "fileName": filename,
        "file_url": f"http://127.0.0.1:8000/files/{filename}"
    }

@app.get("/")
def home():
    return {
        "message": "File Upload API Running"
    }
```

### Important Note on Serving Files

Do **not** create a route like `@app.get("/files/{filename}")`. 

The `app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")` configuration already serves all files in `uploads/` directly at:
```text
http://127.0.0.1:8000/files/<filename>
```

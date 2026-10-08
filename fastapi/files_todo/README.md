# FastAPI Products & File Upload Sample Project

This is a sample project demonstrating CRUD operations with SQLite database and simple file/image upload using FastAPI.

## Setup and Run

1. **Install Dependencies:**
   ```bash
   pip install "fastapi[standard]" sqlalchemy python-multipart
   ```
   *(or if using uv: `uv sync`)*

2. **Run Application:**
   ```bash
   uvicorn main:app --reload
   ```

3. **API Documentation:**
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

## File Upload & Static Serving

- **Upload Endpoint**: `POST /upload`
  - Send file as multipart form data.
  - Returns `file_url` (e.g., `http://127.0.0.1:8000/files/product.jpg`).
- **Static File Access**: `http://127.0.0.1:8000/files/<filename>`
  - Served directly from the `uploads/` folder.
- **Add Product with Image**: `POST /products/db`
  - Store the returned `file_url` in the product's `image` field.

from fastapi import FastAPI, Form, Response
from fastapi.responses import HTMLResponse
import segno
from io import BytesIO

app = FastAPI(title="QR Code Generator")

INDEX = """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>QR Code Generator</title></head>
<body style="font-family: system-ui; max-width: 720px; margin: 40px auto;">
  <h1>QR Code Generator</h1>
  <form method="post" action="/png">
    <label>Texto/URL:</label><br>
    <input name="data" style="width:100%" required><br><br>
    <label>Correção de erro:</label>
    <select name="error">
      <option value="M">M</option><option value="L">L</option>
      <option value="Q">Q</option><option value="H">H</option>
    </select>
    <label style="margin-left:12px;">Borda:</label>
    <input name="border" type="number" value="4" min="0" style="width:80px">
    <label style="margin-left:12px;">Escala:</label>
    <input name="scale" type="number" value="8" min="1" style="width:80px">
    <button type="submit" style="margin-left:12px;">Gerar PNG</button>
  </form>
  <p style="margin-top:24px;">Endpoints extra: <code>/svg?data=...</code> e <code>/png</code> via POST.</p>
</body></html>
"""

@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX

@app.get("/svg")
def svg(data: str, error: str = "M", border: int = 4):
    qr = segno.make(data, error=error)
    buf = BytesIO()
    qr.save(buf, kind="svg", border=border)
    return Response(buf.getvalue(), media_type="image/svg+xml")

@app.post("/png")
def png(data: str = Form(...), error: str = Form("M"),
        border: int = Form(4), scale: int = Form(8)):
    qr = segno.make(data, error=error)
    buf = BytesIO()
    qr.save(buf, kind="png", border=border, scale=scale)
    return Response(buf.getvalue(), media_type="image/png")
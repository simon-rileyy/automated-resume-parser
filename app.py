from flask import Flask, request, render_template
from parser import extract_text_from_pdf, extract_text_from_docx, extract_info
from database import SessionLocal, Candidate
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    parsed_data = None
    if request.method == "POST":
        file = request.files["resume"]
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            if file.filename.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif file.filename.endswith(".docx"):
                text = extract_text_from_docx(file_path)
            else:
                return "Unsupported file format"

            parsed_data = extract_info(text)

            # store in database
            db = SessionLocal()
            candidate = Candidate(
                name=parsed_data["name"],
                email=parsed_data["email"],
                skills=parsed_data["skills"],
                education=parsed_data["education"]
            )
            db.add(candidate)
            db.commit()
            db.close()

    return render_template("index.html", parsed=parsed_data)

if __name__ == "__main__":
    app.run(debug=True)

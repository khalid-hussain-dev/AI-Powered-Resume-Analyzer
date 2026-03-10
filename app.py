import matplotlib
matplotlib.use('Agg')  # For headless environments (Flask)
import matplotlib.pyplot as plt

from flask import Flask, render_template, request
import os
from resume_parser import extract_text_from_pdf, clean_and_tokenize
from skill_matcher import load_skills, match_skills

import nltk

# Download required NLTK data on startup
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

# Rest of your imports...

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return 'No file part'
    file = request.files['resume']
    if file.filename == '':
        return 'No selected file'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Step 1: Extract and clean
        text = extract_text_from_pdf(filepath)
        tokens = clean_and_tokenize(text)

        # Step 2: Load a job role skill set (e.g., frontend)
        job_role = request.form.get('job_role')
        skill_file = f"job_roles/{job_role}.txt"
        job_skills = load_skills(skill_file)

        # Step 3: Match
        matched, missing, match_percent = match_skills(tokens, job_skills)
        
        import io
        import base64

        # Create a pie chart
        labels = 'Matched Skills', 'Missing Skills'
        sizes = [len(matched), len(missing)]
        colors = ['#4CAF50', '#FF5722']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        ax.axis('equal')

        # Save to buffer and encode
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
        buf.close()
        plt.close()

        return render_template("result.html", 
                       matched=matched,
                       missing=missing,
                       match_percent=match_percent,
                       role=job_role.capitalize(),
                       chart=image_base64)

        
if __name__ == '__main__':
    app.run(debug=True)


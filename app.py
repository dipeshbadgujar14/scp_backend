from flask import Flask, request, jsonify
from flask_cors import CORS  
import random
import requests

app = Flask(__name__)
CORS(app)  # <-- Enable CORS for all routes

# --- Job Search API ---
@app.route('/api/job-search', methods=['GET'])
def job_search():
    job_title = request.args.get('title', 'Software')
    location = request.args.get('location', 'Dublin')

    titles = [
        f"{job_title} Engineer", f"{job_title} Developer", f"Senior {job_title} Engineer",
        f"Junior {job_title} Developer", f"{job_title} Architect", f"{job_title} Intern",
        f"{job_title} Analyst", f"Lead {job_title} Developer", f"Full Stack {job_title}"
    ]

    companies = [
        "Google", "Microsoft", "Amazon", "Stripe", "Meta", "Accenture", "HubSpot", "Workday",
        "LinkedIn", "Twilio", "Intel", "TikTok", "Salesforce", "SAP", "Dell Technologies"
    ]

    summaries = [
        "Work on cutting-edge systems using cloud-native technologies.",
        "Join a team of passionate engineers driving innovation.",
        "Design and develop scalable microservices in a hybrid cloud environment.",
        "Collaborate on exciting projects with global impact.",
        "Be part of a fast-paced team building next-gen applications.",
        "Take ownership of backend services and infrastructure.",
        "Contribute to our DevOps and CI/CD practices.",
        "Drive technical decisions and mentor junior developers."
    ]

    jobs = []
    for i in range(50):
        job = {
            "title": random.choice(titles),
            "company": random.choice(companies),
            "location": location,
            "summary": random.choice(summaries)
        }
        jobs.append(job)

    return jsonify({"results": jobs})


# --- Resume Match API ---
role_keywords = {
    "Backend Developer": ["Python", "Java", "Node.js", "Django", "Flask"],
    "Frontend Developer": ["JavaScript", "HTML", "CSS", "React", "Vue", "Angular"],
    "Cloud Engineer": ["AWS", "Azure", "GCP", "Terraform", "Kubernetes"],
    "DevOps Engineer": ["Docker", "CI/CD", "Ansible", "Jenkins", "Linux", "Bash"],
    "Data Scientist": ["Machine Learning", "Data Science", "Pandas", "NumPy", "Scikit-learn"],
    "Data Analyst": ["SQL", "Excel", "Power BI", "Tableau", "Data Visualization"],
    "UI/UX Designer": ["Figma", "Sketch", "Adobe XD", "Wireframes", "Prototyping"],
    "Mobile App Developer": ["Flutter", "React Native", "Android", "iOS", "Swift", "Kotlin"]
}

@app.route('/api/resume-match', methods=['POST'])
def match_resume():
    data = request.get_json()
    resume_text = data.get('resume', '')
    matched_roles = set()

    for role, keywords in role_keywords.items():
        for keyword in keywords:
            if keyword.lower() in resume_text.lower():
                matched_roles.add(role)
                break  # Avoid duplicate matches for the same role

    return jsonify({"matched_roles": list(matched_roles)})

# --- Proxy to Fetch Shareable Resume Link from Cloud File Sharing Service ---
@app.route('/api/get-resume-link/<filename>', methods=['GET'])
def get_resume_share_link(filename):
    """
    This endpoint fetches a shareable pre-signed S3 URL for a given resume file.

    It acts as a proxy between the Job Search App and the Cloud File Sharing App.
    The job search app sends the resume filename to this endpoint, which then
    calls the cloud storage service to get the actual shareable download link.

    Args:
        filename (str): The unique filename of the uploaded resume stored in S3.

    Returns:
        JSON: A response containing the pre-signed URL or an error message.
    """
    try:
        # Call the cloud file sharing API to get a pre-signed S3 link
        response = requests.get(f"https://scp-backend.onrender.com/share/{filename}")
        return jsonify(response.json())
    except Exception as e:
        # Return a 500 response with the error message if anything goes wrong
        return jsonify({"error": str(e)}), 500
    
@app.route('/', methods=['GET'])
def home():
    return "Job Search App is running and is up 🚀", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

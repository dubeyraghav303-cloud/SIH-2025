from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"

# Supabase setup
SUPABASE_URL = "https://nhcevgvrdjzcazlmzrft.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5oY2V2Z3ZyZGp6Y2F6bG16cmZ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc5NzA0OTYsImV4cCI6MjA3MzU0NjQ5Nn0.mwCUjtW16I7PKKPbSLpZK7JhgqIJDvr7KWiCkTQhAMk"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load internships from Supabase
def load_internships():
    response = supabase.table('internships').select('*').execute()
    df = pd.DataFrame(response.data)
    df['description'] = df['company'] + ' - ' + df['title']
    return df

df = load_internships()

all_skills = sorted({s for skills in df["required_skills"] for s in skills})
all_sectors = sorted({s for sectors in df["sector_interests"] for s in sectors})
all_locations = sorted(df["location"].dropna().astype(str).unique())

def norm_set(items):
    return {str(x).strip().lower() for x in items if str(x).strip()}

def calculate_score(user_skills, user_sectors, user_location):
    recs = []
    u_skills = norm_set(user_skills)
    u_sectors = norm_set(user_sectors)

    for _, row in df.iterrows():
        intern_skills_list = row["required_skills"]
        intern_sectors_list = row["sector_interests"]

        intern_skills = {s.lower() for s in intern_skills_list}
        intern_sectors = {s.lower() for s in intern_sectors_list}

        matched_skills = u_skills.intersection(intern_skills)
        missing_skills = intern_skills - u_skills
        skill_score = (len(matched_skills) / len(intern_skills)) if intern_skills else 0

        sector_overlap = u_sectors.intersection(intern_sectors)
        sector_score = (len(sector_overlap) / len(intern_sectors)) if intern_sectors else 0

        stipend_score = row["stipend"] / 10000  # normalize stipend to 0-1 scale

        total_score = (0.5 * skill_score) + (0.3 * sector_score) + (0.2 * stipend_score)

        recs.append({
            "id": int(row["id"]),
            "title": row["title"],
            "description": row["description"],
            "required_skills": ", ".join(intern_skills_list),
            "sector_interests": ", ".join(intern_sectors_list),
            "location": row["location"],
            "stipend": row["stipend"],
            "company": row["company"],
            "score": round(total_score * 1, 1),  # percent format
            "missing_skills": ", ".join(missing_skills)
        })

    return sorted(recs, key=lambda x: x["score"], reverse=True)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            session["user_id"] = response.user.id
            session["user_email"] = response.user.email
            flash("Logged in successfully!", "success")
            return redirect(url_for("onboarding_step1"))
        except Exception as e:
            flash("Invalid credentials", "error")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            session["user_id"] = response.user.id
            session["user_email"] = response.user.email
            # Insert initial profile
            supabase.table('profiles').insert({
                'user_id': response.user.id,
                'name': name,
                'email': email
            }).execute()
            flash("Account created successfully!", "success")
            return redirect(url_for("onboarding_step1"))
        except Exception as e:
            flash("Error creating account", "error")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    supabase.auth.sign_out()
    session.clear()
    return redirect(url_for("login"))

@app.route("/onboarding/step1", methods=["GET", "POST"])
def onboarding_step1():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form.get("name")
        locations = request.form.get("locations")
        # Update profile
        supabase.table('profiles').update({
            'preferred_locations': locations
        }).eq('user_id', session["user_id"]).execute()
        return redirect(url_for("onboarding_step2"))
    profile = supabase.table('profiles').select('*').eq('user_id', session["user_id"]).execute().data
    if profile:
        profile = profile[0]
    return render_template("onboarding_step1.html", profile=profile or {})

@app.route("/onboarding/step2", methods=["GET", "POST"])
def onboarding_step2():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        education = request.form.get("education")
        skills = request.form.get("skills").split(",")
        sectors = request.form.get("sectors").split(",")
        experience = int(request.form.get("experience"))
        institution = request.form.get("institution")
        # Update profile
        supabase.table('profiles').update({
            'education': education,
            'skills': [s.strip() for s in skills],
            'sectors': [s.strip() for s in sectors],
            'experience': experience,
            'institution': institution
        }).eq('user_id', session["user_id"]).execute()
        return redirect(url_for("internship_form"))
    profile = supabase.table('profiles').select('*').eq('user_id', session["user_id"]).execute().data
    if profile:
        profile = profile[0]
    return render_template("onboarding_step2.html", profile=profile or {})

@app.route("/internships", methods=["GET", "POST"])
def internship_form():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        education = request.form.get("education")
        skills = request.form.getlist("skills")
        sectors = request.form.getlist("sector")
        # Update profile
        supabase.table('profiles').update({
            'education': education,
            'skills': skills,
            'sectors': sectors
        }).eq('user_id', session["user_id"]).execute()
        # Calculate recommendations
        recommendations = calculate_score(skills, sectors, None)
        return render_template("output.html", recommendations=recommendations[:10], skills=skills, sectors=sectors)
    profile = supabase.table('profiles').select('*').eq('user_id', session["user_id"]).execute().data
    if profile:
        profile = profile[0]
    return render_template("input.html", skills=all_skills, sectors=all_sectors, profile=profile or {})

@app.route("/save/<int:internship_id>")
def save_toggle(internship_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    # Check if already saved
    existing = supabase.table('user_saved_internships').select('*').eq('user_id', user_id).eq('internship_id', internship_id).execute().data
    if existing:
        # Unsave
        supabase.table('user_saved_internships').delete().eq('user_id', user_id).eq('internship_id', internship_id).execute()
        flash("Removed from saved!", "success")
    else:
        # Save
        supabase.table('user_saved_internships').insert({
            'user_id': user_id,
            'internship_id': internship_id
        }).execute()
        flash("Saved to your shortlist!", "success")
    return redirect(request.referrer or url_for("internship_form"))

@app.route("/apply/<int:internship_id>")
def apply_preview(internship_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    row = df.loc[df["id"] == internship_id]
    if row.empty:
        return redirect(url_for("internship_form"))

    job = row.iloc[0].to_dict()
    profile = supabase.table('profiles').select('*').eq('user_id', session["user_id"]).execute().data
    if profile:
        profile = profile[0]
    return render_template("apply.html", job=job, profile=profile or {})

@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    profile = supabase.table('profiles').select('*').eq('user_id', session["user_id"]).execute().data
    if profile:
        profile = profile[0]
    # Get saved internships
    saved_ids = [s['internship_id'] for s in supabase.table('user_saved_internships').select('internship_id').eq('user_id', session["user_id"]).execute().data]
    saved_list = df[df["id"].isin(saved_ids)].to_dict(orient="records")
    # Get applied internships
    applied_ids = [a['internship_id'] for a in supabase.table('user_applied_internships').select('internship_id').eq('user_id', session["user_id"]).execute().data]
    applied_list = df[df["id"].isin(applied_ids)].to_dict(orient="records")
    return render_template("profile.html", profile=profile or {}, saved=saved_list, applied=applied_list)

@app.route("/apply/submit/<int:internship_id>", methods=["POST"])
def submit_application(internship_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    # Check if already applied
    existing = supabase.table('user_applied_internships').select('*').eq('user_id', user_id).eq('internship_id', internship_id).execute().data
    if not existing:
        supabase.table('user_applied_internships').insert({
            'user_id': user_id,
            'internship_id': internship_id
        }).execute()
        flash("Successfully applied for internship!", "success")
    else:
        flash("Already applied!", "info")
    return redirect(url_for("internship_form"))

@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        profile_data = {
            "name": request.form.get("name"),
            "skills": request.form.get("skills").split(","),
            "education": request.form.get("education"),
            "sectors": request.form.get("sectors").split(","),
            "experience": int(request.form.get("experience") or 0),
            "institution": request.form.get("institution"),
            "preferred_locations": request.form.get("preferred_locations")
        }
        supabase.table('profiles').update(profile_data).eq('user_id', session["user_id"]).execute()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile"))
    profile = supabase.table('profiles').select('*').eq('user_id', session["user_id"]).execute().data
    if profile:
        profile = profile[0]
    return render_template("edit_profile.html", profile=profile or {})

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/enroll/<course_name>")
def enroll_course(course_name):
    # For now, just flash
    flash("Enrolled in course successfully!", "success")
    return redirect(url_for("courses"))

if __name__ == "__main__":
    app.run(debug=True)

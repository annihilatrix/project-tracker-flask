from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_grades_by_github(github)
   
    html = render_template("student_info.html", 
                           first=first, 
                           last=last,
                           github=github,
                           projects=projects)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student-add-form")
def display_student_form():
    """Display student form."""

    return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student via form."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)
    link_string = "/student?github=" + github

    return render_template("student_add_confirmation.html",
                            first_name=first_name,
                            last_name=last_name,
                            github=github,
                            link_string=link_string)


@app.route("/project")
def display_project():
    """List the title, description, and max grade of a project."""

    title = request.args.get('title')
    project_title, description, max_grade = hackbright.get_project_by_title(title)
    student_grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html",
                           project_title=project_title,
                           description=description,
                           max_grade=max_grade,
                           student_grades=student_grades)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

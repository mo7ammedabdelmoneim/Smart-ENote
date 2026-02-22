from flask import redirect, render_template, request, url_for
from app import app
from db.models import db, Program, Lesson



@app.route("/programs")
def programs():
    programs = Program.query.all()

    if not programs:
        return render_template("program/programs.html", programs=[], lessons=[], selected_program=None)

    selected_program_id = request.args.get("program_id", programs[0].id)
    search = request.args.get("search", "")

    lessons_query = Lesson.query.filter_by(program_id=selected_program_id)

    if search:
        lessons_query = lessons_query.filter(Lesson.title.ilike(f"%{search}%"))

    lessons = lessons_query.all()
    selected_program = Program.query.get(selected_program_id)

    return render_template(
        "program/programs.html",
        programs=programs,
        lessons=lessons,
        selected_program=selected_program,
        search=search
    )


@app.route("/programs/add", methods=["POST"])
def add_program():
    title = request.form.get("title", "").strip()

    if title:
        program = Program(title=title)
        db.session.add(program)
        db.session.commit()

    return redirect(url_for("programs"))


@app.route('/program/<int:program_id>/add_lesson', methods=['GET', 'POST'])
def add_lesson(program_id):
    program = Program.query.get_or_404(program_id)

    if request.method == "POST":
        title = request.form.get("title")
        vocab = request.form.get("vocab")     
        expressions = request.form.get("expressions")
        notes = request.form.get("notes")

        new_lesson = Lesson(
            program_id=program.id,
            title=title,
            words=vocab,
            sentences=expressions,
            notes=notes
        )
        db.session.add(new_lesson)
        db.session.commit()
        return redirect(url_for('programs', program_id=program.id))

    return render_template("program/add_lesson.html", selected_program=program)

@app.route('/lesson/<int:lesson_id>')
def view_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    vocab_list = lesson.words.split("|||") if lesson.words else []
    expressions_list = lesson.sentences.split("|||") if lesson.sentences else []
    notes_list = lesson.notes.split("|||") if lesson.notes else []

    return render_template(
        "program/view_lesson.html",
        lesson=lesson,
        vocab_list=vocab_list,
        expressions_list=expressions_list,
        notes_list=notes_list
    )


@app.route("/lesson/<int:lesson_id>/edit", methods=["GET", "POST"])
def edit_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    if request.method == "POST":
        lesson.title = request.form["title"]
        lesson.words = request.form["vocab"]
        lesson.sentences = request.form["expressions"]
        lesson.notes = request.form["notes"]

        db.session.commit()

        return redirect(url_for("view_lesson", lesson_id=lesson.id))

    return render_template(
        "program/edit_lesson.html",
        lesson=lesson,
        vocab_list=lesson.words.split("|||") if lesson.words else [],
        expressions_list=lesson.sentences.split("|||") if lesson.sentences else [],
        notes_list=lesson.notes.split("|||") if lesson.notes else []
    )




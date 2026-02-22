from flask import render_template, request, redirect, url_for, jsonify
from app import app
from db.models import Topic
from db.models import Topic, db

@app.route("/general")
def general_index():
    topics = Topic.query.all()
    general_topic = Topic.query.filter_by(title="General").first()
    return render_template(
        "general/general_index.html",
        topics=topics,
        selected_topic=general_topic,
        words_list=general_topic.words.split("|||") if general_topic.words else [],
        sentences_list=general_topic.sentences.split("|||") if general_topic.sentences else []
    )

@app.route("/general/topic/<int:topic_id>")
def view_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    return render_template(
        "general/general_index.html",
        topics=Topic.query.all(),
        selected_topic=topic,
        words_list=topic.words.split("|||") if topic.words else [],
        sentences_list=topic.sentences.split("|||") if topic.sentences else []
    )

@app.route("/general/topic/<int:topic_id>/add-word", methods=["POST"])
def add_topic_word(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    text = request.json["text"]
    topic.words = (topic.words + "|||" if topic.words else "") + text
    db.session.commit()
    return {"status": "ok"}

@app.route("/general/topic/<int:topic_id>/add-sentence", methods=["POST"])
def add_topic_sentence(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    text = request.json["text"]
    topic.sentences = (topic.sentences + "|||" if topic.sentences else "") + text
    db.session.commit()
    return {"status": "ok"}

@app.route("/general/topic/add", methods=["POST"])
def add_topic():
    data = request.get_json()
    title = data.get("title", "").strip()
    if not title:
        return {"status": "error", "message": "Title cannot be empty"}, 400
    if Topic.query.filter_by(title=title).first():
        return {"status": "error", "message": "Topic already exists"}, 400
    topic = Topic(title=title, words="", sentences="")
    db.session.add(topic)
    db.session.commit()
    return jsonify({
        "status": "ok",
        "topic_id": topic.id
    })



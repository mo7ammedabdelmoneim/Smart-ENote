from app import app
from models import db, Topic


def create_general_topic():
    general = Topic.query.filter_by(title="General").first()
    if not general:
        general = Topic(
            title="General",
            words="",
            sentences=""
        )
        db.session.add(general)
        db.session.commit()
        print("✅ General topic created")
    else:
        print("ℹ️ General topic already exists")


if __name__ == "__main__":
    with app.app_context():
        create_general_topic()

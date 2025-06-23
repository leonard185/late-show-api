from app import app
from models import db, Guest, Episode, Appearance
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    guest1 = Guest(name="Will Smith", occupation="Actor")
    guest2 = Guest(name="Billie Eilish", occupation="Singer")

    episode1 = Episode(date=date(2024, 6, 20), number=101)
    episode2 = Episode(date=date(2024, 6, 21), number=102)

    # First add guests and episodes so they get IDs
    db.session.add_all([guest1, guest2, episode1, episode2])
    db.session.commit()

    # Now add appearances with proper foreign key IDs
    appearance1 = Appearance(rating=5, guest_id=guest1.id, episode_id=episode1.id)
    appearance2 = Appearance(rating=4, guest_id=guest2.id, episode_id=episode2.id)

    db.session.add_all([appearance1, appearance2])
    db.session.commit()

print("✅ Seeding complete.")

"""Idempotently seed realistic demo complaints."""
from datetime import datetime, timezone
from pathlib import Path
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_engine
from app.models.complaint import ComplaintORM
from app.models.enums import Category, Priority, Status


SEED = [
    ("Pani pipe is leaking near Committee Chowk", "Committee Chowk", Category.water, Priority.normal),
    ("Gali mein pani khara hai after rain", "Saddar", Category.water, Priority.high),
    ("Water pressure is very low in the market", "Raja Bazaar", Category.water, Priority.normal),
    ("Bijli wire is hanging dangerously near school", "Satellite Town", Category.electricity, Priority.high),
    ("Power outage since last night", "Chaklala", Category.electricity, Priority.high),
    ("Transformer sparks near the mosque", "Dhoke Kala Khan", Category.electricity, Priority.high),
    ("Garbage has not been collected for three days", "Peshawar Road", Category.sanitation, Priority.normal),
    ("Kachra is blocking the drain", "Tench Bhatta", Category.sanitation, Priority.high),
    ("Sewer smell is spreading in the street", "Westridge", Category.sanitation, Priority.normal),
    ("Large pothole damaging bikes", "Murree Road", Category.roads, Priority.normal),
    ("Road is broken after construction", "Bahria Phase 7", Category.roads, Priority.normal),
    ("Footpath is unsafe for school children", "6th Road", Category.roads, Priority.high),
    ("Streetlight is not working near the park", "Ayub Park", Category.streetlights, Priority.normal),
    ("Bulb is broken on the dark lane", "Dhok Hassu", Category.streetlights, Priority.normal),
    ("Several lights are off on the main road", "Airport Road", Category.streetlights, Priority.high),
    ("Tree branch is blocking the public walkway", "Jinnah Park", Category.other, Priority.normal),
    ("Broken bench needs repair", "Liaquat Bagh", Category.other, Priority.low),
    ("Open manhole is dangerous", "Committee Chowk", Category.other, Priority.high),
    ("Pani is overflowing outside the clinic", "Benazir Hospital", Category.water, Priority.high),
    ("Water tanker is blocking the service road", "Islamabad Highway", Category.water, Priority.normal),
    ("Bijli meter box is damaged", "Gulzar-e-Quaid", Category.electricity, Priority.normal),
    ("Emergency power wire has sparks", "Koral", Category.electricity, Priority.high),
    ("Trash bags are scattered beside the bus stop", "Khayaban-e-Sir Syed", Category.sanitation, Priority.normal),
    ("Overflowing sewer needs urgent attention", "Lalazar", Category.sanitation, Priority.high),
    ("Potholes make the road difficult for cars", "Pindi Saddar", Category.roads, Priority.normal),
    ("Street pavement collapsed after rain", "Kashmir Road", Category.roads, Priority.high),
    ("Small cosmetic crack on the footpath", "F-8 Markaz", Category.roads, Priority.low),
    ("Dark street near the bus stand", "Pirwadhai", Category.streetlights, Priority.high),
    ("Minor bulb replacement requested", "Chandni Chowk", Category.streetlights, Priority.low),
    ("Public park gate needs repair", "Nawaz Sharif Park", Category.other, Priority.low),
]


def main():
    now = datetime.now(timezone.utc)
    inserted = 0
    with Session(get_engine()) as db:
        for text, location, category, priority in SEED:
            exists = db.scalar(select(ComplaintORM.id).where(ComplaintORM.text == text, ComplaintORM.location == location))
            if exists:
                continue
            db.add(ComplaintORM(
                id=uuid.uuid4(), text=text, location=location,
                category=category, priority=priority, status=Status.open,
                ai_summary=text[:140], triaged_by='seed', triage_latency_ms=0,
                created_at=now, updated_at=now,
            ))
            inserted += 1
        db.commit()
    print(f'Inserted {inserted} complaints; existing seed rows were skipped.')


if __name__ == '__main__':
    main()

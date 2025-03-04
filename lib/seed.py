#!/usr/bin/env python3

from faker import Faker
import random
from sqlalchemy.orm import sessionmaker
from models import engine, Freebies, Dev, Company, create_tables

# Ensure tables exist before inserting data
create_tables()

Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(Company).delete()
session.query(Dev).delete()
session.query(Freebies).delete()
session.commit()  # Commit deletion to avoid integrity issues

fake = Faker()

# Seed companies
companies = [
    Company(name=fake.company(), founding_year=random.randint(1950, 2023))
    for _ in range(10)
]
session.add_all(companies)  # Use add_all instead of bulk_save_objects
session.commit()  # Commit to get assigned IDs

# Refresh objects to ensure IDs are populated
for company in companies:
    session.refresh(company)

# Seed developers
devs = [Dev(name=fake.name()) for _ in range(10)]
session.add_all(devs)  # Use add_all instead of bulk_save_objects
session.commit()  # Commit to get assigned IDs

# Refresh objects to ensure IDs are populated
for dev in devs:
    session.refresh(dev)

# Seed freebies
freebies = [
    Freebies(
        item_name=fake.word(),
        value=random.randint(10, 100),
        dev_id=random.choice(devs).id,  # Now IDs are guaranteed to exist
        company_id=random.choice(companies).id
    )
    for _ in range(20)
]
session.add_all(freebies)  # Use add_all instead of bulk_save_objects
session.commit()

print("Seeding complete!")
session.close()

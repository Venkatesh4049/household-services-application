from app import app, db  


with app.app_context():
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    print("All data has been deleted from the database.")

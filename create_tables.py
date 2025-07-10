from app import create_app, db

def create_all_tables():
    app = create_app()
    with app.app_context():
        from app.models.provider import Provider
        db.create_all()
        print("All database tables have been created successfully.")

if __name__ == "__main__":
    create_all_tables()
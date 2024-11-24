from app import app, db, Table, Admin
import os

def init_db():
    print("Initializing database...")
    
    with app.app_context():
        # Drop all tables
        print("Dropping all existing tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating new tables...")
        db.create_all()

        print("Adding sample tables...")
        # Add sample tables
        sample_tables = [
            # Row 1 - Window Section (all 4-person tables)
            Table(table_number=1, capacity=4, x=5, y=5, shape='rectangle'),
            Table(table_number=2, capacity=4, x=30, y=5, shape='round'),
            Table(table_number=3, capacity=4, x=55, y=5, shape='round'),
            Table(table_number=4, capacity=4, x=80, y=5, shape='rectangle'),
            
            # Row 2 - 4-person tables
            Table(table_number=5, capacity=4, x=5, y=20, shape='rectangle'),
            Table(table_number=6, capacity=4, x=30, y=20, shape='round'),
            Table(table_number=7, capacity=4, x=55, y=20, shape='round'),
            Table(table_number=8, capacity=4, x=80, y=20, shape='rectangle'),
            
            # Row 3 - Mixed capacity (6 and 4-person tables)
            Table(table_number=9, capacity=6, x=5, y=35, shape='rectangle'),
            Table(table_number=10, capacity=4, x=30, y=35, shape='round'),
            Table(table_number=11, capacity=4, x=55, y=35, shape='round'),
            Table(table_number=12, capacity=6, x=80, y=35, shape='rectangle'),
            
            # Row 4 - VIP Section (middle tables 6-person)
            Table(table_number=13, capacity=8, x=5, y=50, shape='rectangle', is_vip=True),
            Table(table_number=14, capacity=6, x=30, y=50, shape='square', is_vip=True),
            Table(table_number=15, capacity=6, x=55, y=50, shape='square', is_vip=True),
            Table(table_number=16, capacity=8, x=80, y=50, shape='rectangle', is_vip=True),
        ]
        
        # Add all tables to session
        for table in sample_tables:
            db.session.add(table)
        
        print("Adding admin user...")
        # Add sample admin user
        admin = Admin(
            username='admin',
            email='admin@example.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Commit changes
        try:
            db.session.commit()
            print("\nDatabase initialized successfully!")
            print("\nAdmin credentials:")
            print("Username: admin")
            print("Password: admin123")
            print("Email: admin@example.com")
        except Exception as e:
            db.session.rollback()
            print(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    init_db()

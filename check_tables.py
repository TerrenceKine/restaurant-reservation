from app import app, db, Table

with app.app_context():
    tables = Table.query.all()
    if tables:
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"Table {table.table_number}: capacity={table.capacity}, is_vip={table.is_vip}, shape={table.shape}")
    else:
        print("No tables found in database")

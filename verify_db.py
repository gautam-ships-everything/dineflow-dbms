from app.db import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
views = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name").fetchall()]
triggers = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='trigger' ORDER BY name").fetchall()]

print("Tables in Database (", len(tables), "):")
for t in tables:
    count = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  - {t}: {count} records")

print("\nViews in Database (", len(views), "):")
for v in views:
    count = cur.execute(f"SELECT COUNT(*) FROM {v}").fetchone()[0]
    print(f"  - {v}: {count} rows")

print("\nTriggers in Database (", len(triggers), "):")
for trg in triggers:
    print(f"  - {trg}")

conn.close()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ... (other code)

with db.session.begin():
    db.session.execute("CREATE TRIGGER trigger_users_insert AFTER INSERT ON Users BEGIN UPDATE Users SET created_at = datetime('now', 'utc') WHERE rowid = new.rowid; END;")
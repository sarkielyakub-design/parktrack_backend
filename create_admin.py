from app.database.database import SessionLocal
from app.models.models import User
from app.utils.hashing import hash_password

db = SessionLocal()

admin_email = "ztechuniversal@gmail.com"

existing = db.query(User).filter(
    User.email == admin_email
).first()

if existing:
    print("Admin already exists")
else:

    admin = User(
        email=admin_email,
        password=hash_password("12345678"),
        role="admin"
    )

    db.add(admin)
    db.commit()

    print("Admin created")
from app.database import SessionLocal
from app.models.user import User
from app.enums.user_role import UserRole
from app.utils.security import hash_password


db = SessionLocal()

try:
    admin = User(
        full_name="Abrar",
        email="abrar.admin@example.com",
        password_hash=hash_password("Admin@12345"),
        role=UserRole.ADMIN,
        is_active=True,
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("Admin created successfully.")
    print(f"ID: {admin.id}")
    print(f"Name: {admin.full_name}")
    print(f"Email: {admin.email}")
    print(f"Role: {admin.role.value}")

finally:
    db.close()
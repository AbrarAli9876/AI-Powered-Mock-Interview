from getpass import getpass

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.enums.user_role import UserRole
from app.models.user import User
from app.utils.security import hash_password


def create_admin() -> None:
    """
    Create the initial administrator account.
    """

    db: Session = SessionLocal()

    try:
        print("\n=== AI Mock Interview - Admin Setup ===\n")

        full_name = input("Admin full name: ").strip()
        email = input("Admin email: ").strip().lower()

        if not full_name:
            print("Error: Full name cannot be empty.")
            return

        if not email:
            print("Error: Email cannot be empty.")
            return

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            if existing_user.role == UserRole.ADMIN:
                print("An administrator with this email already exists.")
                return

            print(
                "A user with this email already exists."
            )
            print(
                "No changes were made to the existing account."
            )
            return

        password = getpass("Admin password: ")
        confirm_password = getpass("Confirm password: ")

        if not password:
            print("Error: Password cannot be empty.")
            return

        if password != confirm_password:
            print("Error: Passwords do not match.")
            return

        password_hash = hash_password(password)

        admin = User(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=UserRole.ADMIN,
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("\nAdmin account created successfully.")
        print(f"Admin ID: {admin.id}")
        print(f"Email: {admin.email}")
        print(f"Role: {admin.role.value}")

    except Exception as exc:
        db.rollback()
        print(f"\nFailed to create admin: {exc}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
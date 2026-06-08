"""Bootstrap a superadmin account directly in MongoDB.

There is no public registration endpoint, so the first privileged account must be
seeded out-of-band. Used for local runs and E2E (Cypress logs in with these
credentials). Values come from the environment, defaulting to a dev superadmin.

Run inside the api container:

    docker compose run --rm \
      -e MONGODB_URL=mongodb://mongo-test:27017 -e MONGODB_TLS=false -e MONGODB_DB=reviews_e2e \
      api python -m app.scripts.seed_admin
"""

import asyncio
import os

from app.core.security import hash_password
from app.db.database import init_db
from app.db.models import User


async def main() -> None:
    await init_db()
    username = os.getenv("SEED_ADMIN_USERNAME", "RootAdmin")
    password = os.getenv("SEED_ADMIN_PASSWORD", "rootpass")
    email = os.getenv("SEED_ADMIN_EMAIL", "root@reviews.dev")

    existing = await User.find_one(User.username == username)
    if existing:
        existing.password_hash = hash_password(password)
        existing.role = "superadmin"
        existing.email = email
        await existing.save()
        print(f"updated existing superadmin '{username}'")
    else:
        await User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role="superadmin",
        ).insert()
        print(f"created superadmin '{username}'")


if __name__ == "__main__":
    asyncio.run(main())

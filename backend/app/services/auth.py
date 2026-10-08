from datetime import datetime, timedelta, timezone
import os
import secrets

from fastapi import Cookie, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import SessionToken, User

SESSION_MAX_AGE = 60 * 60 * 24


def get_current_user(
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = db.get(SessionToken, session_token)
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    expires_at = session.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.get(User, session.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def create_session(db: Session, user: User, response: Response) -> None:
    token = secrets.token_urlsafe(48)
    session = SessionToken(
        token=token,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )
    db.add(session)
    db.commit()
    is_production = os.getenv("ENVIRONMENT") == "production"

    response.set_cookie(
        "session_token",
        token,
        httponly=True,
        samesite="none" if is_production else "lax",
        secure=is_production,
        max_age=SESSION_MAX_AGE,
    )

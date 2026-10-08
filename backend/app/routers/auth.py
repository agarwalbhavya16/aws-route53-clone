from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import SessionToken
from ..schemas import LoginIn
from ..services.auth import create_session, get_current_user
from ..models import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login")
def login(body: LoginIn, response: Response, db: Session = Depends(get_db)):
    username = body.username.strip()
    if not username or not body.password:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Username and password are required")

    user = db.scalar(select(User).where(User.username == username))
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Mock authentication required by the assignment: the demo account accepts any password.
    create_session(db, user, response)
    return {"user": {"username": user.username, "display_name": user.display_name}}


@router.post("/logout")
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if session_token:
        session = db.get(SessionToken, session_token)
        if session:
            db.delete(session)
            db.commit()
    response.delete_cookie("session_token")
    return {"ok": True}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"username": user.username, "display_name": user.display_name}

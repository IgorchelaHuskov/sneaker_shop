"""Определение класса для модели пользователя.""" 
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from jwt_authentication import db, bcrypt
from jwt_authentication.util.datetime_util import (
    uts_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string,
)


class User(db.Model):
    """Модель пользователя для хранения учетных данных и других данных."""

    __tablename__ = "site_user"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=uts_now)
    admin = db.Column(db.Boolean, default=False)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))

    def __repr__(self):
        return (
            f"<User email={self.email}, public_id={self.public_id}, admin={self.admin}>"
        )
    
    @hybrid_property
    def registered_on_str(self):
        """преобразует значение даты и времени, хранящееся в registered_on в форматированную строку."""
        registered_on_uts = make_tzaware(
            self.registered_on, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(registered_on_uts, use_tz=get_local_utcoffset())

    @property
    def password(self):
        raise AttributeError("пароль: поле только для записи")
    
    @password.setter
    def password(self, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.pasword_hash = hash_bytes.decode("utf-8")

    def check_passsword(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def encode_access_token(self):
        now = datetime.now(timezone.utc)
        token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
        token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
        expire = now + timedelta(hours=token_age_h, minutes=token_age_m)
        if current_app.config["TESTING"]:
            expire = now + timedelta(seconds=5)
        payload = dict(exp=expire, iat=now, sub=self.public_id, admin=self.admin)
        key = current_app.config.get("SECRET_KEY")
        return jwt.encode(payload, key, algorithm="HS256")
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()
    
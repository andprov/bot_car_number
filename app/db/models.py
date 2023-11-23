from sqlalchemy import (
    BigInteger,
    ForeignKey,
    create_engine,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    Mapped,
    mapped_column,
)

from app.config import DB_URL


class Base(AsyncAttrs, DeclarativeBase):
    ...


class User(Base):
    """Модель пользователя."""

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    first_name: Mapped[str]
    phone: Mapped[str]
    autos: Mapped[list["Auto"]] = relationship(
        back_populates="owner", cascade="all, delete"
    )

    def __repr__(self):
        return f"tg_id={self.tg_id} name={self.first_name}"


class Auto(Base):
    """Модель автомобиля."""

    __tablename__ = "auto"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(unique=True, index=True)
    model: Mapped[str]
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    owner: Mapped[User] = relationship(back_populates="autos")

    def __repr__(self):
        return f"{self.number} - {self.model}"


engine = create_engine(DB_URL, echo=True)
Base.metadata.create_all(engine)

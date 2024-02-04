from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.database import Base


class User(Base):
    """Модель пользователя."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    first_name: Mapped[str]
    phone: Mapped[str]
    banned: Mapped[bool] = mapped_column(default=False)

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

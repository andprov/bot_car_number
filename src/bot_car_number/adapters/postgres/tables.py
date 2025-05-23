from sqlalchemy import BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    first_name: Mapped[str]
    phone: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)

    autos: Mapped[list["Auto"]] = relationship(
        back_populates="owner", cascade="all, delete"
    )

    def __repr__(self):
        return f"tg_id={self.tg_id} name={self.first_name}"


class Auto(Base):
    __tablename__ = "app_auto"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(unique=True, index=True)
    model: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("app_user.id", ondelete="CASCADE")
    )

    owner: Mapped["User"] = relationship(back_populates="autos")

    def __repr__(self):
        return f"{self.number} - {self.model}"


class Registration(Base):
    __tablename__ = "app_registration"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    count: Mapped[int] = mapped_column(default=1)

    def __repr__(self):
        return f"{self.tg_id} count={self.count}"


class SearchAttempt(Base):
    __tablename__ = "app_search_attempt"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, index=True)
    number: Mapped[str]
    date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

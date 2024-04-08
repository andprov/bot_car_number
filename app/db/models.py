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
    banned: Mapped[bool] = mapped_column(default=False)

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


class Stats(Base):
    __tablename__ = "app_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("app_user.id", ondelete="SET NULL"), nullable=True
    )
    data: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

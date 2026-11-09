from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.user_role import Roles
from app.infrastructure.database.base import Base

def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "usuarios"

    __table_args__ = (

        UniqueConstraint(
            "super_admin_slot",
            name="uq_users_single_super_admin",
        ),

        Index(
            "ix_users_role_active",
            "role",
            "is_active",
        ),
    )

    # Identificador principal
    id_usuario: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

# Rol del usuario
    tipo_rol: Mapped[Roles] = mapped_column(
        SAEnum(
            Roles,
            values_callable=lambda cls: [
            role.value for role in cls
        ],
        native_enum=False,
        create_constraint=True,
        length=30,  # Coincide con el VARCHAR(30) de tu tabla SQL
        name="fk_usuarios_tipo_rol",
    ),
        ForeignKey("roles.tipo_rol"),  # Enlaza con la tabla roles de tu BD
        nullable=False,
    )

    nombre: Mapped[str | None] = mapped_column(String(50))
    apellido: Mapped[str | None] = mapped_column(String(50))
    telefono: Mapped[int | None] = mapped_column(Integer)
    direccion: Mapped[str | None] = mapped_column(String(50))
    correo: Mapped[str | None] = mapped_column(String(60))

    password_hash: Mapped[str] = mapped_column(
        String(128),
        nullable=False
        )

    # Estado de la cuenta
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    # Fechas de auditoría
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    super_admin_slot: Mapped[int | None] = mapped_column(
        Integer,
        Computed(
            "CASE WHEN role = 'SUPER_ADMIN' THEN 1 ELSE NULL END",
            persisted=True
        ),
        nullable=True
    )

    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


"""add fleet maintenance

Revision ID: 9715a92814fd
Revises: 67020faf70db
Create Date: 2026-10-01 11:55:05.312789
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9715a92814fd"
down_revision: Union[str, Sequence[str], None] = "67020faf70db"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add fleet maintenance support.

    Existing aircraft rows are preserved by adding the new
    required numeric/date fields as nullable first, backfilling
    safe defaults, and then enforcing NOT NULL constraints.
    """

    # ---------------------------------------------------------
    # 1. Create maintenance_records table
    # ---------------------------------------------------------

    op.create_table(
        "maintenance_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("aircraft_id", sa.Integer(), nullable=False),
        sa.Column(
            "maintenance_type",
            sa.String(length=40),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "scheduled_start",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "scheduled_end",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "actual_start",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "actual_end",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "technician",
            sa.String(length=150),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["aircraft_id"],
            ["aircraft.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_maintenance_records_id",
        "maintenance_records",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_maintenance_records_aircraft_id",
        "maintenance_records",
        ["aircraft_id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 2. Add new aircraft columns as NULLABLE
    #
    # Existing aircraft rows already exist.
    # Therefore NOT NULL cannot be used immediately.
    # ---------------------------------------------------------

    op.add_column(
        "aircraft",
        sa.Column(
            "total_flight_hours",
            sa.Double(),
            nullable=True,
        ),
    )

    op.add_column(
        "aircraft",
        sa.Column(
            "total_cycles",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "aircraft",
        sa.Column(
            "last_maintenance_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "aircraft",
        sa.Column(
            "next_maintenance_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    op.add_column(
        "aircraft",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 3. Backfill existing aircraft
    # ---------------------------------------------------------

    op.execute(
        """
        UPDATE aircraft
        SET total_flight_hours = 0
        WHERE total_flight_hours IS NULL
        """
    )

    op.execute(
        """
        UPDATE aircraft
        SET total_cycles = 0
        WHERE total_cycles IS NULL
        """
    )

    op.execute(
        """
        UPDATE aircraft
        SET created_at = CURRENT_TIMESTAMP
        WHERE created_at IS NULL
        """
    )

    # ---------------------------------------------------------
    # 4. Enforce NOT NULL after backfill
    # ---------------------------------------------------------

    op.alter_column(
        "aircraft",
        "total_flight_hours",
        existing_type=sa.Double(),
        nullable=False,
    )

    op.alter_column(
        "aircraft",
        "total_cycles",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "aircraft",
        "created_at",
        existing_type=sa.DateTime(),
        nullable=False,
    )


def downgrade() -> None:
    """
    Remove fleet maintenance support.
    """

    # ---------------------------------------------------------
    # 1. Remove aircraft maintenance fields
    # ---------------------------------------------------------

    op.drop_column(
        "aircraft",
        "created_at",
    )

    op.drop_column(
        "aircraft",
        "next_maintenance_at",
    )

    op.drop_column(
        "aircraft",
        "last_maintenance_at",
    )

    op.drop_column(
        "aircraft",
        "total_cycles",
    )

    op.drop_column(
        "aircraft",
        "total_flight_hours",
    )

    # ---------------------------------------------------------
    # 2. Remove maintenance_records
    # ---------------------------------------------------------

    op.drop_index(
        "ix_maintenance_records_id",
        table_name="maintenance_records",
    )

    op.drop_index(
        "ix_maintenance_records_aircraft_id",
        table_name="maintenance_records",
    )

    op.drop_table(
        "maintenance_records",
    )
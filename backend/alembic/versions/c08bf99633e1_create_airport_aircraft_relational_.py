"""create airport aircraft relational flights

Revision ID: c08bf99633e1
Revises:
Create Date: 2026-10-01 10:18:13.595277
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c08bf99633e1"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Convert the existing flights table from string-based
    origin/destination/aircraft fields to relational foreign keys.

    Important:
    - Existing flight data is preserved.
    - New FK columns are added as nullable first.
    - Existing values are mapped to airports/aircraft.
    - Columns are changed to NOT NULL only after backfilling.
    """

    # ---------------------------------------------------------
    # 1. Create aircraft table
    # ---------------------------------------------------------
    op.create_table(
        "aircraft",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("registration", sa.String(length=20), nullable=False),
        sa.Column("model", sa.String(length=80), nullable=False),
        sa.Column("manufacturer", sa.String(length=80), nullable=False),
        sa.Column("seat_capacity", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default="AVAILABLE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_aircraft_id",
        "aircraft",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_aircraft_registration",
        "aircraft",
        ["registration"],
        unique=True,
    )

    # ---------------------------------------------------------
    # 2. Create airports table
    # ---------------------------------------------------------
    op.create_table(
        "airports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("iata_code", sa.String(length=3), nullable=False),
        sa.Column("icao_code", sa.String(length=4), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column(
            "country",
            sa.String(length=100),
            nullable=False,
            server_default="Myanmar",
        ),
        sa.Column("latitude", sa.Double(), nullable=False),
        sa.Column("longitude", sa.Double(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_airports_id",
        "airports",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_airports_iata_code",
        "airports",
        ["iata_code"],
        unique=True,
    )

    op.create_index(
        "ix_airports_icao_code",
        "airports",
        ["icao_code"],
        unique=True,
    )

    # ---------------------------------------------------------
    # 3. Add relational columns as NULLABLE
    # ---------------------------------------------------------
    op.add_column(
        "flights",
        sa.Column(
            "origin_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "flights",
        sa.Column(
            "destination_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "flights",
        sa.Column(
            "aircraft_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 4. Insert airports from existing flight codes
    #
    # We preserve the old origin/destination values.
    #
    # Known Myanmar airports are inserted with their actual
    # airport information where available.
    # ---------------------------------------------------------

    connection = op.get_bind()

    airports = [
        {
            "iata_code": "RGN",
            "icao_code": "VYYY",
            "name": "Yangon International Airport",
            "city": "Yangon",
            "country": "Myanmar",
            "latitude": 16.9073,
            "longitude": 96.1332,
        },
        {
            "iata_code": "BKK",
            "icao_code": "VTBS",
            "name": "Suvarnabhumi Airport",
            "city": "Bangkok",
            "country": "Thailand",
            "latitude": 13.6900,
            "longitude": 100.7501,
        },
        {
            "iata_code": "MDL",
            "icao_code": "VYMD",
            "name": "Mandalay International Airport",
            "city": "Mandalay",
            "country": "Myanmar",
            "latitude": 21.7022,
            "longitude": 95.9779,
        },
        {
            "iata_code": "SIN",
            "icao_code": "WSSS",
            "name": "Singapore Changi Airport",
            "city": "Singapore",
            "country": "Singapore",
            "latitude": 1.3644,
            "longitude": 103.9915,
        },
        {
            "iata_code": "CNX",
            "icao_code": "VTCC",
            "name": "Chiang Mai International Airport",
            "city": "Chiang Mai",
            "country": "Thailand",
            "latitude": 18.7668,
            "longitude": 98.9626,
        },
        {
            "iata_code": "HEH",
            "icao_code": "VYHH",
            "name": "Heho Airport",
            "city": "Heho",
            "country": "Myanmar",
            "latitude": 20.7470,
            "longitude": 96.7920,
        },
        {
            "iata_code": "NYU",
            "icao_code": "VYBG",
            "name": "Nyaung U Airport",
            "city": "Nyaung U",
            "country": "Myanmar",
            "latitude": 21.1738,
            "longitude": 94.9247,
        },
        {
            "iata_code": "KAW",
            "icao_code": "VYKT",
            "name": "Kawthaung Airport",
            "city": "Kawthaung",
            "country": "Myanmar",
            "latitude": 10.0493,
            "longitude": 98.5380,
        },
        {
            "iata_code": "THL",
            "icao_code": "VYTL",
            "name": "Tachileik Airport",
            "city": "Tachileik",
            "country": "Myanmar",
            "latitude": 20.4838,
            "longitude": 99.9354,
        },
    ]

    airport_table = sa.table(
        "airports",
        sa.column("iata_code", sa.String()),
        sa.column("icao_code", sa.String()),
        sa.column("name", sa.String()),
        sa.column("city", sa.String()),
        sa.column("country", sa.String()),
        sa.column("latitude", sa.Float()),
        sa.column("longitude", sa.Float()),
    )

    for airport in airports:
        connection.execute(
            sa.insert(airport_table).values(**airport)
        )

    # ---------------------------------------------------------
    # 5. Backfill origin_id and destination_id
    # ---------------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE flights AS f
            SET origin_id = a.id
            FROM airports AS a
            WHERE UPPER(TRIM(f.origin)) = UPPER(a.iata_code)
            """
        )
    )

    connection.execute(
        sa.text(
            """
            UPDATE flights AS f
            SET destination_id = a.id
            FROM airports AS a
            WHERE UPPER(TRIM(f.destination)) = UPPER(a.iata_code)
            """
        )
    )

    # ---------------------------------------------------------
    # 6. Validate airport mappings
    # ---------------------------------------------------------

    missing_origin = connection.execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM flights
            WHERE origin_id IS NULL
            """
        )
    ).scalar_one()

    missing_destination = connection.execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM flights
            WHERE destination_id IS NULL
            """
        )
    ).scalar_one()

    if missing_origin:
        raise RuntimeError(
            "Migration failed: some flights.origin values "
            "could not be mapped to airports.iata_code."
        )

    if missing_destination:
        raise RuntimeError(
            "Migration failed: some flights.destination values "
            "could not be mapped to airports.iata_code."
        )

    # ---------------------------------------------------------
    # 7. Create aircraft records from existing flight values
    #
    # Existing aircraft values are preserved as registration.
    # ---------------------------------------------------------

    aircraft_values = connection.execute(
        sa.text(
            """
            SELECT DISTINCT TRIM(aircraft)
            FROM flights
            WHERE aircraft IS NOT NULL
              AND TRIM(aircraft) <> ''
            """
        )
    ).fetchall()

    aircraft_table = sa.table(
        "aircraft",
        sa.column("registration", sa.String()),
        sa.column("model", sa.String()),
        sa.column("manufacturer", sa.String()),
        sa.column("seat_capacity", sa.Integer()),
        sa.column("status", sa.String()),
    )

    for row in aircraft_values:
        registration = row[0]

        connection.execute(
            sa.insert(aircraft_table).values(
                registration=registration,
                model="UNKNOWN",
                manufacturer="UNKNOWN",
                seat_capacity=0,
                status="AVAILABLE",
            )
        )

    # ---------------------------------------------------------
    # 8. Backfill aircraft_id
    # ---------------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE flights AS f
            SET aircraft_id = a.id
            FROM aircraft AS a
            WHERE TRIM(f.aircraft) = TRIM(a.registration)
            """
        )
    )

    # ---------------------------------------------------------
    # 9. Add foreign keys
    # ---------------------------------------------------------

    op.create_foreign_key(
        "fk_flights_origin_id_airports",
        "flights",
        "airports",
        ["origin_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_flights_destination_id_airports",
        "flights",
        "airports",
        ["destination_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_flights_aircraft_id_aircraft",
        "flights",
        "aircraft",
        ["aircraft_id"],
        ["id"],
    )

    # ---------------------------------------------------------
    # 10. Change origin_id / destination_id to NOT NULL
    # ---------------------------------------------------------

    op.alter_column(
        "flights",
        "origin_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.alter_column(
        "flights",
        "destination_id",
        existing_type=sa.Integer(),
        nullable=False,
    )

    # aircraft_id intentionally remains nullable because the
    # SQLAlchemy model allows aircraft_id=None.

    # ---------------------------------------------------------
    # 11. Remove old string columns
    # ---------------------------------------------------------

    op.drop_column("flights", "origin")
    op.drop_column("flights", "destination")
    op.drop_column("flights", "aircraft")


def downgrade() -> None:
    """
    Restore the original string-based flight columns.
    """

    connection = op.get_bind()

    # ---------------------------------------------------------
    # 1. Add old columns back
    # ---------------------------------------------------------

    op.add_column(
        "flights",
        sa.Column(
            "origin",
            sa.String(length=10),
            nullable=True,
        ),
    )

    op.add_column(
        "flights",
        sa.Column(
            "destination",
            sa.String(length=10),
            nullable=True,
        ),
    )

    op.add_column(
        "flights",
        sa.Column(
            "aircraft",
            sa.String(length=50),
            nullable=True,
        ),
    )

    # ---------------------------------------------------------
    # 2. Restore airport codes
    # ---------------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE flights AS f
            SET origin = a.iata_code
            FROM airports AS a
            WHERE f.origin_id = a.id
            """
        )
    )

    connection.execute(
        sa.text(
            """
            UPDATE flights AS f
            SET destination = a.iata_code
            FROM airports AS a
            WHERE f.destination_id = a.id
            """
        )
    )

    # ---------------------------------------------------------
    # 3. Restore aircraft registration
    # ---------------------------------------------------------

    connection.execute(
        sa.text(
            """
            UPDATE flights AS f
            SET aircraft = a.registration
            FROM aircraft AS a
            WHERE f.aircraft_id = a.id
            """
        )
    )

    # ---------------------------------------------------------
    # 4. Make restored columns NOT NULL
    # ---------------------------------------------------------

    op.alter_column(
        "flights",
        "origin",
        existing_type=sa.String(length=10),
        nullable=False,
    )

    op.alter_column(
        "flights",
        "destination",
        existing_type=sa.String(length=10),
        nullable=False,
    )

    op.alter_column(
        "flights",
        "aircraft",
        existing_type=sa.String(length=50),
        nullable=False,
    )

    # ---------------------------------------------------------
    # 5. Drop foreign keys
    # ---------------------------------------------------------

    op.drop_constraint(
        "fk_flights_aircraft_id_aircraft",
        "flights",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_flights_destination_id_airports",
        "flights",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_flights_origin_id_airports",
        "flights",
        type_="foreignkey",
    )

    # ---------------------------------------------------------
    # 6. Drop relational columns
    # ---------------------------------------------------------

    op.drop_column("flights", "aircraft_id")
    op.drop_column("flights", "destination_id")
    op.drop_column("flights", "origin_id")

    # ---------------------------------------------------------
    # 7. Drop indexes and tables
    # ---------------------------------------------------------

    op.drop_index(
        "ix_airports_icao_code",
        table_name="airports",
    )

    op.drop_index(
        "ix_airports_iata_code",
        table_name="airports",
    )

    op.drop_index(
        "ix_airports_id",
        table_name="airports",
    )

    op.drop_table("airports")

    op.drop_index(
        "ix_aircraft_registration",
        table_name="aircraft",
    )

    op.drop_index(
        "ix_aircraft_id",
        table_name="aircraft",
    )

    op.drop_table("aircraft")
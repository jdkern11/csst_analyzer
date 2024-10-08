"""update csst processed temp primary key

Revision ID: 621a4847fe0c
Revises: 81bc11bf15e2
Create Date: 2024-02-29 15:30:52.802106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "621a4847fe0c"
down_revision = "81bc11bf15e2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "csst_reactor_processed_temperature_values_pkey",
        "csst_reactor_processed_temperature_values",
    )
    op.create_primary_key(
        "csst_reactor_processed_temperature_values_pkey",
        "csst_reactor_processed_temperature_values",
        [
            "csst_reactor_id",
            "average_temperature",
            "temperature_range",
            "heating",
            "cooling",
            "holding",
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "csst_reactor_processed_temperature_values_pkey",
        "csst_reactor_processed_temperature_values",
    )
    op.create_primary_key(
        "csst_reactor_processed_temperature_values_pkey",
        "csst_reactor_processed_temperature_values",
        ["csst_reactor_id", "average_temperature", "temperature_range"],
    )
    # ### end Alembic commands ###

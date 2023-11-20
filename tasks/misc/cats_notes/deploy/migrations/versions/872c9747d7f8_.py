"""empty message

Revision ID: 872c9747d7f8
Revises: 
Create Date: 2023-10-27 18:55:32.980398

"""
from alembic import op
from sqlalchemy import insert
from app import Notes
import json
from random import shuffle


# revision identifiers, used by Alembic.
revision = '872c9747d7f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    with open("init_data.json") as f:
        data = json.load(f)
        first_notes = data["first_notes"]
        deception = data["deception"]
        filling_notes = data["filling_notes"]
        filling_notes_1 = filling_notes * 631
        shuffle(filling_notes_1)

        filling_notes_2 = filling_notes * 169
        shuffle(filling_notes_2)

    init_data = first_notes + deception + filling_notes_1 + filling_notes_2

    for row in init_data:
        query = insert(Notes).values(name=row['name'], note=row['note'])
        conn.execute(query)


def downgrade():
    pass

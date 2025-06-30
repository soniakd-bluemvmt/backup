"""Add embedding_status and status_detail to Resource

Revision ID: 0fffc8ad901a
Revises: 
Create Date: 2025-06-30 13:47:50.601517

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0fffc8ad901a'
down_revision = None
branch_labels = None
depends_on = None

embedding_status_enum = postgresql.ENUM('PENDING', 'SUCCESS', 'FAILED', name='embeddingstatus')

def upgrade():
    # Create ENUM type
    embedding_status_enum.create(op.get_bind(), checkfirst=True)

    # Add columns to resources table
    op.add_column('resources', sa.Column('embedding_status', embedding_status_enum, nullable=False, server_default='PENDING'))
    op.add_column('resources', sa.Column('status_detail', sa.Text(), nullable=True))


def downgrade():
    # Remove columns
    op.drop_column('resources', 'status_detail')
    op.drop_column('resources', 'embedding_status')

    # Drop ENUM type
    embedding_status_enum.drop(op.get_bind(), checkfirst=True)

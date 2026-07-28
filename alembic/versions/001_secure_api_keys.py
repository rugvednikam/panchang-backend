"""secure_api_keys

Revision ID: 001
Revises: 
Create Date: 2026-07-28 16:50:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
import hmac
import hashlib
import os

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 1. Add new columns
    with op.batch_alter_table('api_keys', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashed_key', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('key_prefix', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True))

    # 2. Get SECRET_KEY
    try:
        from app.core.config import settings
        secret_key = settings.SECRET_KEY
    except ImportError:
        secret_key = os.environ.get("SECRET_KEY", "fallback_secret")

    # 3. Data migration
    bind = op.get_bind()
    
    # Read existing keys
    result = bind.execute(sa.text("SELECT id, key FROM api_keys"))
    
    for row in result:
        key_id = row[0]
        plain_key = row[1]
        
        # Compute HMAC-SHA256
        hashed = hmac.new(
            secret_key.encode(),
            plain_key.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Extract prefix
        prefix = plain_key[:12] if plain_key else "migrated"
        
        # Update row
        bind.execute(
            sa.text("UPDATE api_keys SET hashed_key = :hashed, key_prefix = :prefix WHERE id = :id"),
            {"hashed": hashed, "prefix": prefix, "id": key_id}
        )

    # 4. Enforce constraints and remove old column
    with op.batch_alter_table('api_keys', schema=None) as batch_op:
        batch_op.alter_column('hashed_key', existing_type=sa.String(), nullable=False)
        batch_op.alter_column('key_prefix', existing_type=sa.String(), nullable=False)
        
        batch_op.create_index(batch_op.f('ix_api_keys_hashed_key'), ['hashed_key'], unique=True)
        
        batch_op.drop_index('ix_api_keys_key')
        batch_op.drop_column('key')


def downgrade():
    with op.batch_alter_table('api_keys', schema=None) as batch_op:
        batch_op.add_column(sa.Column('key', sa.VARCHAR(), nullable=True))
        batch_op.create_index('ix_api_keys_key', ['key'], unique=1)
        
        batch_op.drop_index(batch_op.f('ix_api_keys_hashed_key'))
        batch_op.drop_column('expires_at')
        batch_op.drop_column('last_used_at')
        batch_op.drop_column('key_prefix')
        batch_op.drop_column('hashed_key')

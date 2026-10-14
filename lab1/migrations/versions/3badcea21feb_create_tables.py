from alembic import op
import sqlalchemy as sa

revision = "3badcea21feb"
down_revision = None


def upgrade():
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
    )
    op.create_table(
        "readers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("authors.id"), nullable=False),
        sa.Column("reader_id", sa.Integer(), sa.ForeignKey("readers.id"), nullable=True),
    )


def downgrade():
    op.drop_table("books")
    op.drop_table("readers")
    op.drop_table("authors")

"""enforce complaint field constraints"""
from alembic import op

revision = '003_enforce_complaint_contract'
down_revision = '002_add_complaint_indexes'
branch_labels = None
depends_on = None

def upgrade():
    op.execute("UPDATE complaints SET triaged_by='rules' WHERE triaged_by IN ('seed','simulated')")
    op.create_check_constraint('ck_complaints_text_length', 'complaints', "char_length(text) BETWEEN 10 AND 2000")
    op.create_check_constraint('ck_complaints_location_length', 'complaints', "char_length(location) BETWEEN 3 AND 200")
    op.create_check_constraint('ck_complaints_summary_length', 'complaints', "ai_summary IS NULL OR char_length(ai_summary) <= 140")
    op.create_check_constraint('ck_complaints_triaged_by', 'complaints', "triaged_by IN ('llm:groq','llm:ollama','rules','rules:fallback')")

def downgrade():
    for name in ('ck_complaints_triaged_by','ck_complaints_summary_length','ck_complaints_location_length','ck_complaints_text_length'):
        op.drop_constraint(name, 'complaints', type_='check')

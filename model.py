import sqlalchemy
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Score(Base):
    __tablename__ = 'score'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    school_name: Mapped[str] = mapped_column(String(128), index=True)
    suburb: Mapped[str] = mapped_column(String(32))
    state: Mapped[str] = mapped_column(String(3))
    year: Mapped[int] = mapped_column(Integer())
    grade: Mapped[str] = mapped_column(String(8))
    school_sector: Mapped[str] = mapped_column(String(32))
    school_type: Mapped[str] = mapped_column(String(16))
    school_location: Mapped[str] = mapped_column(String(32))
    year_range: Mapped[str] = mapped_column(String(8))
    reading: Mapped[int] = mapped_column(Integer())
    reading_low: Mapped[int] = mapped_column(Integer())
    reading_high: Mapped[int] = mapped_column(Integer())
    reading_sim_avg: Mapped[int] = mapped_column(Integer())
    reading_sim_low: Mapped[int] = mapped_column(Integer())
    reading_sim_high: Mapped[int] = mapped_column(Integer())
    reading_all_avg: Mapped[int] = mapped_column(Integer())
    writing: Mapped[int] = mapped_column(Integer())
    writing_low: Mapped[int] = mapped_column(Integer())
    writing_high: Mapped[int] = mapped_column(Integer())
    writing_sim_avg: Mapped[int] = mapped_column(Integer())
    writing_sim_low: Mapped[int] = mapped_column(Integer())
    writing_sim_high: Mapped[int] = mapped_column(Integer())
    writing_all_avg: Mapped[int] = mapped_column(Integer())
    spelling: Mapped[int] = mapped_column(Integer())
    spelling_low: Mapped[int] = mapped_column(Integer())
    spelling_high: Mapped[int] = mapped_column(Integer())
    spelling_sim_avg: Mapped[int] = mapped_column(Integer())
    spelling_sim_low: Mapped[int] = mapped_column(Integer())
    spelling_sim_high: Mapped[int] = mapped_column(Integer())
    spelling_all_avg: Mapped[int] = mapped_column(Integer())
    grammar: Mapped[int] = mapped_column(Integer())
    grammar_low: Mapped[int] = mapped_column(Integer())
    grammar_high: Mapped[int] = mapped_column(Integer())
    grammar_sim_avg: Mapped[int] = mapped_column(Integer())
    grammar_sim_low: Mapped[int] = mapped_column(Integer())
    grammar_sim_high: Mapped[int] = mapped_column(Integer())
    grammar_all_avg: Mapped[int] = mapped_column(Integer())
    numeracy: Mapped[int] = mapped_column(Integer())
    numeracy_low: Mapped[int] = mapped_column(Integer())
    numeracy_high: Mapped[int] = mapped_column(Integer())
    numeracy_sim_avg: Mapped[int] = mapped_column(Integer())
    numeracy_sim_low: Mapped[int] = mapped_column(Integer())
    numeracy_sim_high: Mapped[int] = mapped_column(Integer())
    numeracy_all_avg: Mapped[int] = mapped_column(Integer())
    total: Mapped[int] = mapped_column(Integer())

sqlalchemy.Index('score_school_suburb_state_year_grade', Score.school_name, Score.suburb, Score.state, Score.year, Score.grade, unique=True)
sqlalchemy.Index('score_total', Score.total)
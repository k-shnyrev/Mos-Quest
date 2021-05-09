import sqlalchemy

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    true_answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    map_request = sqlalchemy.Column(sqlalchemy.String, nullable=True)

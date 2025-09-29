from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

book_authors = Table(
    'book_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id', ondelete='CASCADE'), primary_key=True),
)

book_genres = Table(
    'book_genres', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
)


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    books = relationship('Book', secondary=book_authors, back_populates='authors')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    books = relationship('Book', secondary=book_genres, back_populates='genres')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    year = Column(Integer)
    authors = relationship('Author', secondary=book_authors, back_populates='books')
    genres = relationship('Genre', secondary=book_genres, back_populates='books')
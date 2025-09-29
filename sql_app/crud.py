from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext import IntegrityError
from models import Author, Book, Genre

async def get_or_create_author(session: AsyncSession, name: str):
    stmt = select(Author).where(Author.name == name)
    res = (await session.execute(stmt)).scalar_one_or_none()
    if res:
        return res

    a = Author(name=name)
    session.add(a)

    try:
        await session.flush()
        return a

    except IntegrityError:
        await session.rollback()
        return (await session.execute(select(Author).where(Author.name == name))).scalar_one()

    await session.refresh(a)
    return a

async def get_or_create_genre(session: AsyncSession, name: str):
    stmt = select(Genre).where(Genre.name == name)
    res = (await session.execute(stmt)).scalar_one_or_none()
    if res:
        return res
    g = Genre(name=name)
    session.add(g)
    try:
        await session.flush()
        return g
    except IntegrityError:
        await session.rollback()
        return (await session.execute(select(Genre).where(Genre.name == name))).scalar_one()

async def add_book(
    session: AsyncSession,
    title: str,
    year: int | None,
    description: str | None,
    author_names: list[str],
    genre_names: list[str]
):
    async with session.begin():  # одна транзакция на всё
        book = Book(title=title, year=year, description=description)

        # Добавляем авторов
        for an in author_names:
            a = await get_or_create_author(session, an)
            book.authors.append(a)

        # Добавляем жанры
        for gn in genre_names:
            g = await get_or_create_genre(session, gn)
            book.genres.append(g)

        session.add(book)

    # тут commit уже выполнен автоматически
    return book
import asyncio
import os
from typing import Dict, List
from uuid import uuid4
from sqlakeyset import select_page
from sqlalchemy import UUID, Column, MetaData, String, Table, insert, select
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy_utils import database_exists, create_database


metadata = MetaData(schema="public")

WidgetsTable = Table(
    "widgets",
    metadata,
    Column("widget_id", UUID),
    Column("widget_name", String),
)


async def init_db(engine: AsyncEngine):
    # Initialize the DB

    widgets: List[Dict] = []
    for i in range(100):
        widgets.append({"widget_id": uuid4(), "widget_name": f"Widget {'{:03d}'.format(i)}"})

    insert_stmt = insert(WidgetsTable).values(widgets)

    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
        await conn.execute(insert_stmt)


async def test_pagination(engine: AsyncEngine):
    stmt = (
        select(WidgetsTable).order_by(WidgetsTable.c.widget_name)
    )
    async with engine.connect() as conn:
        # This raises with `KeyError: 'entity'`
        page = await select_page(conn, stmt, per_page=8, page=0)

    for row in page:
        print(f"ID: {str(row.widget_id)}, name: {row.widget_name}")


async def main():
    load_dotenv()

    PG_USER = os.environ.get("PG_USER")
    PG_PASS = os.environ.get("PG_PASS")

    ENGINE_URL = f"postgresql+psycopg://{PG_USER}:{PG_PASS}@localhost:5432/sqlakeyset_example"

    if not database_exists(ENGINE_URL):
        print("Creating database...")
        create_database(ENGINE_URL)

    engine = create_async_engine(ENGINE_URL)

    await init_db(engine=engine)
    await test_pagination(engine=engine)

if __name__ == "__main__":
    asyncio.run(main())

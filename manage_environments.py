import logging
import os

import click
from sqlalchemy import create_engine

SNOWFLAKE_USERNAME = os.environ["SNOWFLAKE_USERNAME"]
SNOWFLAKE_PASSWORD = os.environ["SNOWFLAKE_PASSWORD"]
SNOWFLAKE_ACCOUNT = os.environ["SNOWFLAKE_ACCOUNT"]
SNOWFLAKE_ROLE = os.environ["SNOWFLAKE_ROLE"]


@click.command()
@click.option("--create", "action", flag_value="create")
@click.option("--drop", "action", flag_value="drop")
@click.option("--database")
@click.option("--schema")
def manage_database(database: str, schema: str, action: str):
    if action == "create":
        stmts = [
            f'CREATE OR REPLACE DATABASE "{database}"',
            f'GRANT USAGE ON DATABASE "{database}" TO ROLE PUBLIC',
        ]
    elif action == "drop":
        stmts = [
            f'DROP DATABASE "{database}"',
        ]
    else:
        stmts = []  # do nothing

    with create_engine(
        f"snowflake://{SNOWFLAKE_USERNAME}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}"
    ).begin() as tx:
        for stmt in stmts:
            tx.execute(stmt)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    manage_database()
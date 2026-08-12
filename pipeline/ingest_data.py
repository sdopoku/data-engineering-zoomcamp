#!/usr/bin/env python
# coding: utf-8

import click
import polars as pl
from sqlalchemy import create_engine
from tqdm.auto import tqdm


@click.command()
@click.option("--pg-user", default="root", show_default=True, help="PostgreSQL user name.")
@click.option("--pg-password", default="root", show_default=True, help="PostgreSQL password.")
@click.option("--pg-host", default="localhost", show_default=True, help="PostgreSQL host.")
@click.option("--pg-port", default=5432, show_default=True, type=int, help="PostgreSQL port.")
@click.option("--pg-db", default="ny_taxi", show_default=True, help="PostgreSQL database name.")
@click.option("--year", required=True, type=int, help="Taxi data year to ingest.")
@click.option("--month", required=True, type=click.IntRange(1, 12), help="Taxi data month to ingest.")
@click.option("--target-table", default="yellow_taxi_trips", show_default=True, help="Destination table name.")
@click.option("--chunksize", default=100_000, show_default=True, type=int, help="Rows per batch when ingesting data.")
def run(pg_user, pg_password, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    """Ingest NYC taxi data into PostgreSQL database."""
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f"{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz"

    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    df_iter = pl.scan_csv(
        url,
        try_parse_dates=True,
    ).collect_batches(chunk_size=chunksize)

    first = True

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).write_database(
                table_name=target_table,
                connection=engine,
                if_table_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.write_database(
            table_name=target_table,
            connection=engine,
            if_table_exists="append"
        )


if __name__ == '__main__':
    run()





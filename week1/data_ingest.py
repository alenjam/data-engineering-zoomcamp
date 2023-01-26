import pandas as pd
import argparse
from sqlalchemy import create_engine
import subprocess
import os


def run_command(cmd, verbose=False):

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-url")
    parser.add_argument("-pg_user_name")
    parser.add_argument("-pg_password")
    parser.add_argument("-pg_host")
    parser.add_argument("-pg_port")
    parser.add_argument("-pg_database")
    parser.add_argument("-table_name")
    args = parser.parse_args()
    print(args)

    url = args.url
    pg_user_name = args.pg_user_name
    pg_password = args.pg_password
    pg_host = args.pg_host
    pg_port = args.pg_port
    pg_database = args.pg_database
    table_name = args.table_name
    output_file_name = "output.csv.gz" if url.endswith(".gz") else "output.csv"
    download_file(url, output_file_name)
    upload_to_postgres(
        output_file_name,
        pg_user_name,
        pg_password,
        pg_host,
        pg_port,
        pg_database,
        table_name,
    )
    cleanup(output_file_name)


def download_file(url, output_file_name):
    unix_command = f"wget {url} -O {output_file_name}"
    run_command(unix_command, verbose=True)


def upload_to_postgres(
    output_file_name,
    pg_user_name,
    pg_password,
    pg_host,
    pg_port,
    pg_database,
    table_name,
):
    print(
        f"postgresql://{pg_user_name}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
    )
    eng = create_engine(
        f"postgresql://{pg_user_name}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
    )
    for idx, chunk in enumerate(pd.read_csv(output_file_name, chunksize=50000)):
        chunk.to_sql(name=table_name, con=eng, if_exists="append")
        print(f"Uploaded the chunk: {idx}")

def cleanup(output_file_name):
    file_path = os.path.join(os.getcwd(), output_file_name)
    print(f"{file_path} - about to be removed!")
    os.remove(file_path)


if __name__ == "__main__":
    main()

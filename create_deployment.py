from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://gitlab.bsc.es/inb/elixir/software-observatory/toolshed-metadata-importer.git",
        entrypoint="main_prefect.py:import_data",
    ).deploy(
        name="toolshed-metadata-importer",
        work_pool_name="my-managed-pool",
        cron="0 1 * * *",
    )


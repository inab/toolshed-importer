from prefect import task, Flow, Parameter
import logging
from dotenv import load_dotenv
from repos_metadata_importer import reposFetcher
from galaxy_metadata import dMetadataFetcher

@task
def fetch_tools_metadata():
    logging.info('Fetching metadata from the Galaxy Toolshed...')
    RF = reposFetcher()
    RF.fetch_tools()
    return RF.all_metadatas

@task
def process_tools_metadata(repositories_metadata):
    logging.info('Processing Galaxy Toolshed Repositories Metadata...')
    dMFetcher = dMetadataFetcher(tools_galaxy_metadata=repositories_metadata)
    dMFetcher.process_metadata()

with Flow("Data Import Flow") as flow:
    # Define flow parameters
    log_level = Parameter("log_level", default="INFO")
    log_dir = Parameter("log_dir", default="./logs/summary.log")

    # Environment variables
    load_dotenv()
    
    # Task execution
    repositories_metadata = fetch_tools_metadata()
    process_tools_metadata(repositories_metadata)

# Execute the flow
if __name__ == "__main__":
    flow.run(parameters={"log_level": "DEBUG", "log_dir": "./logs/summary.log"})

import logging
import argparse
from dotenv import load_dotenv
import sys

from repos_metadata_importer import reposFetcher
from galaxy_metadata import dMetadataFetcher

def import_data():
    try:

        # ---------- Preparation ----------

        # 0.1 Set up logging
        parser = argparse.ArgumentParser(
            description="Importer of OpenEBench tools from OpenEBench Tool API"
        )
        parser.add_argument(
            "--loglevel", "-l",
            help=("Set the logging level"),
            default="INFO",
        )
        '''
        parser.add_argument(
            "--logdir", "-d",
            help=("Set the logging directory"),
            default="./logs/summary.log",
        )
        '''
        args = parser.parse_args()
        numeric_level = getattr(logging, args.loglevel.upper())
        #logs_dir = args.logdir
        print(f"Logging level: {numeric_level}")
        #print(f"Logging directory: {logs_dir}")

        logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - toolshed - %(message)s', stream=sys.stdout)        
        logging.getLogger('urllib3').setLevel(logging.INFO)


        # 0.2 Load .env
        load_dotenv()
        logging.info("state_importation - 1")

        # ---------- Importation --------------

        #1. Fetch galaxy metadata
        logging.debug('Initializing reposFetcher object to fetch metadata from the Galaxy Toolshed')
        RF = reposFetcher()

        #2. Fetch galaxy metadata
        logging.debug('Fetching raw metadata of all the repositories from the Galaxy Toolshed.')
        RF.fetch_tools()

        #3. Fetch and process configuration files in repos
        logging.info('Parsing and saving Galaxy Toolshed Repositories Metadata...')
        repositories_metadata = RF.all_metadatas
        dMFetcher = dMetadataFetcher(tools_galaxy_metadata=repositories_metadata) ## --- testing  here
        dMFetcher.process_metadata()

    except Exception as e:
        logging.error(f"error - {type(e).__name__} - {e}")
        logging.info("state_importation - 2")
        exit(1)
    
    else: 
        logging.info("state_importation - 0")

        exit(0)


if __name__ == '__main__':
    import_data() 


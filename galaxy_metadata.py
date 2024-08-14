import os
import logging
from utils import connect_db, update_entry, add_metadata_to_entry

class dMetadataFetcher():
    def __init__(self, tools_galaxy_metadata):
        self.repositories = tools_galaxy_metadata
        self.seen_tools = set()

        
    def get_dependencies(self, latest_revision):
        if latest_revision.get('tool_dependencies'):
            return(list(latest_revision['tool_dependencies'].keys()))
        else:
            return([])
    
    def retrieve_metadata(self, repo):
        entries = []
        if repo:
            latest_revision_id = max(iter(repo.keys()))
            latest_revision = repo[latest_revision_id]
            if latest_revision.get('repository', None):
                if 'tools' in latest_revision.keys():
                    dependencies = self.get_dependencies(latest_revision)
                    homepage = latest_revision['repository'].get('homepage_url')
                    repository = latest_revision['repository'].get('remote_repository_url')
                    for tool in latest_revision['tools']:
                        if tool.get('id') and tool.get('version'):
                            if tool['id']+tool['version'] not in self.seen_tools:
                                entry = {}
                                entry['id'] = tool['id']
                                if 'name' in tool.keys():
                                    entry['name'] = tool.get('name')
                                else:
                                    entry['name'] = tool['id']
                                entry['version'] = tool['version']
                                entry['dependencies'] = dependencies
                                entry['homepage'] = homepage
                                entry['repository'] = repository
                                entry['repository_id'] = latest_revision.get('repository_id')
                                entry['changeset_revision'] = latest_revision.get('changeset_revision')

                                self.seen_tools.add(tool['id']+tool['version'])

                                entries.append(entry)
        return(entries)

    def process_metadata(self):
        alambique = connect_db('alambique')
        for repo in self.repositories:
            entries = self.retrieve_metadata(repo)
            if entries:
                for entry in entries:
                    identifier = f"galaxy_metadata/{entry['id']}/cmd/{entry['version']}"
                    entry = {
                        'data': entry,
                        '@data_source': 'galaxy_metadata',
                    }
                    document_w_metadata = add_metadata_to_entry(identifier, entry, alambique)
                    update_entry(document_w_metadata, alambique)
                
            else:
                continue
        

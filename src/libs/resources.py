import src.libs.code_loader as code_loader
from src.libs.logger import create_logger


class Resources:
    """ Factory for creating commonly used resources.
    """

    def __init__(self):
        self.logger = create_logger()

    def __enter__(self):
        """ Context manager for resource management.
        Instances of this class can be used in a with statement.
        e.g. with code_loader.get_resource_factory() as resources:
                 ... do something ...
        This ensures all connections, etc. are closed when the with block ends.
        """
        return self

    def __exit__(self, exc_type, exc_val, trace):
        """ Release all resources acquired via this ResourceFactory
        """
        msg = None

    def get_module(self, module_name, dir_path):
        """ Returns the named module, using dynamic_import functionality
        in the code_loader module.
        """
        project_root = 'src'
        return code_loader.dynamic_import(module_name, project_root=project_root, dir_path=dir_path)

    def get_connector(self, config):
        return self.get_module('connector', 'libs').Connector(config, self.logger)

    def get_config(self, config_file, setting):
        return self.get_module('config', 'libs').Config(config_file, setting).config

    def get_source(self, source_package):
        return self.get_module('source', 'libs').Source(source_package)

import rpy2.robjects.packages as packages
import pandas as pd
import numpy as np


class Source:

    def __init__(self, source_package):
        self.package_name = source_package
        self.source_package = self.import_source_package(source_package)

    def import_source_package(self, package_name):
        """
        Import the source package. We check if it's already installed, then after import
        we check if it's the most up-to-date release version on Github.
        """
        if packages.isinstalled(package_name):
            self.source_package = packages.importr(package_name)
            if self.check_latest_release_version(package_name):
                return self.source_package
            else:
                self.install_package(package_name)

    def install_package(self, package_name):
        """
        Installs the source package using the R utils package.
        """
        utils = packages.importr('utils')
        utils.chooseCRANmirror(ind=1)
        utils.install_packages(package_name)
        self.source_package = packages.importr(package_name)
        return self.source_package

    def check_latest_release_version(self, package):
        """
        check if imported source package is latest available version.
        """
        utils = packages.importr('utils')
        installed_package = self.extract_version(utils.installed_packages())
        available_package = self.extract_version(utils.available_packages())
        is_latest_version = installed_package[package] == available_package[package]
        return is_latest_version

    def extract_version(self, package_data):
        """
        Get package and version column.
        """
        return dict(zip(package_data.rx(True, 'Package'), package_data.rx(True, 'Version')))

    def get_player_stats(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(v)
        results = self.source_package.fetch_player_stats(*args)
        player_stats = pd.DataFrame.from_dict({key: np.asarray(results.rx2(key)) for key in results.names},
                                              orient='index')
        player_stats = player_stats.T
        return player_stats

    def get_fixture(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(v)
        results = self.source_package.fetch_fixture(*args)
        fixture = pd.DataFrame.from_dict({key: np.asarray(results.rx2(key)) for key in results.names},
                                         orient='index')
        fixture = fixture.T
        return fixture

    def get_lineup(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(v)
        results = self.source_package.fetch_lineup(*args)
        lineup = pd.DataFrame.from_dict({key: np.asarray(results.rx2(key)) for key in results.names},
                                        orient='index')
        lineup = lineup.T
        return lineup

    def get_results(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(v)
        results = self.source_package.fetch_results(*args)
        season_results = pd.DataFrame.from_dict({key: np.asarray(results.rx2(key)) for key in results.names},
                                                orient='index')
        season_results = season_results.T
        return season_results

    def get_ladder(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(v)
        results = self.source_package.fetch_ladder(*args)
        ladder = pd.DataFrame.from_dict({key: np.asarray(results.rx2(key)) for key in results.names},
                                        orient='index')
        ladder = ladder.T
        return ladder

    #TODO This fetch function may be source dependent - need to investigate
    """
    def get_player_details(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(v)
        results = self.source_package.fetch_player_details(*args)
        player_details = pd.DataFrame.from_dict({key: np.asarray(results.rx2(key)) for key in results.names},
                                                orient='index')
        player_details = player_details.T
        return player_details
    """

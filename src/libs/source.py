import rpy2.robjects.packages as packages
import pandas as pd
import numpy as np
import requests


class Source:

    #TODO possibly remove hardcoding and put in config. We'll need to add config when creating an instance of
    # the Source class.
    REPOSITORY = 'https://api.github.com/repos/jimmyday12/fitzRoy/releases/latest'

    def __init__(self, source_package):
        self.source_package = self.import_source_package(source_package)

    def import_source_package(self, package_name):
        """
        Import the source package. We check if it's already installed, then after import
        we check if it's the most up-to-date release version on Github.
        """
        if packages.isinstalled(package_name):
            self.source_package = packages.importr(package_name)
            release_version = self.check_latest_release_version()
            if self.source_package.__version__ == release_version:
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

    def check_latest_release_version(self):
        """
        check if imported source package is latest release version on Github
        if it's not the latest release we'll re-install the package
        """
        response = requests.get(self.REPOSITORY)
        release_name = response.json()["name"]
        latest_release_version = release_name.split(' ')[1]
        return latest_release_version

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

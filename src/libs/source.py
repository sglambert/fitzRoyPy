import rpy2.robjects.packages as packages
import pandas as pd
import numpy as np


class Source:

    def __init__(self, source_package):
        self.source_package = self.get_source_package(source_package)

    def get_source_package(self, package_name):
        if packages.isinstalled(package_name):
            self.source_package = packages.importr(package_name)
            return self.source_package
        else:
            utils = packages.importr('utils')
            utils.chooseCRANmirror(ind=1)
            utils.install_packages(package_name)
            self.source_package = packages.importr(package_name)
            return self.source_package

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

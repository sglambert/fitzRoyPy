import time
import math
import traceback
import psycopg2
import numpy as np
import pandas as pd
from itertools import islice
from sqlalchemy import create_engine


class Connector:

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.conn = None
        self.cursor = None
        self.engine = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if self.cursor is not None:
            if exc_type is not None:
                self.rollback()
                traceback.print_exception(exc_type, exc_value, tb)
            else:
                self.commit()
        self.close()

    def connect(self):
        connection_string = f"postgresql+psycopg2://" \
                            f"{self.config['user']}:" \
                            f"{self.config['password']}@" \
                            f"{self.config['host']}:" \
                            f"{self.config['port']}"
        self.engine = create_engine(connection_string)
        self.conn = psycopg2.connect(f"dbname={self.config['dbname']} user={self.config['user']} "
                                     f"password={self.config['password']} host={self.config['host']}")
        self.cursor = self.conn.cursor()
        #TODO
        #if SET_FAST_EXECUTEMANY_SWITCH:
        #    @event.listens_for(self.engine, 'before_cursor_execute')
        #    def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
        #        if executemany:
        #            cursor.fast_executemany = True
        return self

    def query(self, sql):
        result = self.conn.execute(sql)
        self.logger.debug('Ran Query: %s' % sql)
        return result

    def commit(self):
        assert self.cursor is not None
        self.conn.commit()
        self.logger.debug("COMMIT")

    def rollback(self):
        assert self.cursor is not None
        self.conn.rollback()
        self.logger.debug("ROLLBACK")

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
            self.cursor = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.logger.info("Disconnected from %s database" % self.config['db'])

    def select_all(self, sql, parameters=None):
        self.execute(sql, parameters)
        return self.cursor.fetchall()

    def select_one(self, sql):
        self.execute(sql)
        assert self.cursor.rowcount <= 1
        return self.cursor.fetchone()

    def select_array(self, sql):
        rows = self.select_all(sql)
        return [r[0] for r in rows]

    def select_single_value(self, sql):
        row = self.select_one(sql)
        if row:
            assert len(row) == 1
        return row and row[0]

    def select_yield(self, sql):
        with self.conn.cursor(True) as dynamic_cursor:
            self.execute(sql, dynamic_cursor)
            while True:
                rows = dynamic_cursor.fetchmany(1000)
                if not rows:
                    break
                for row in rows:
                    yield row

    def execute(self, sql, parameters=None):
        self.cursor.execute(sql, parameters)

    def executemany(self, sql, parameters=None):
        assert self.cursor is not None
        self.cursor.executemany(sql, parameters)

    # Convience methods with Pandas

    def write_df(self, table_name, df, **kwargs):
        df.to_sql(table_name, con=self.engine, **kwargs)
        return True

    def write_split_df(self, table_name, dfs, **kwargs):
        self.write_df(table_name, dfs[0], **kwargs)
        kwargs.pop('if_exists')
        for df in dfs[1:]:
            self.write_df(table_name, df, if_exists='append', **kwargs)
        return True

    def split_df(self, df, chunksize):
        chunk_count = int(math.ceil(df.size / chunksize))
        return np.array_split(df, chunk_count)

    def set_df(self, table_name, df, if_exists='replace', chunksize=10 ** 6, **kwargs):
        s = time.time()
        status = False
        if chunksize is not None and df.size > chunksize:
            dfs = self.split_df(df, chunksize)
            status = self.write_split_df(table_name, dfs, if_exists=if_exists, **kwargs)
        else:
            status = self.write_df(table_name, df, if_exists='replace', **kwargs)
        self.logger.info("Wrote name: %s, dataframe shape: %s, %i" % (table_name, df.shape, round(time.time() - s, 4)))
        return status

    def get_df(self, table_name, chunk_count=None, **kwargs):
        s = time.time()
        if 'chunksize' not in kwargs.keys():
            kwargs['chunksize'] = 10 ** 6
        dfs = pd.read_sql_table(table_name, self.engine, **kwargs)

        try:
            df = pd.concat(islice(dfs, chunk_count), axis=0)
        except ValueError:
            self.logger.info(f"No objects to concatenate on table_name: {table_name}")
            return None

        self.logger.info('Fetched name: %s, dataframe shape: %s, within: %.4f' %
                         (table_name, df.shape, round(time.time() - s, 4)))
        return df

    def df_query(self, sql):
        result = pd.read_sql_query(sql, con=self.engine)
        return result

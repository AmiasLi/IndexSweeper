import pymysql
import sqlalchemy
import pandas as pd
from pydantic import BaseModel


class Instance(BaseModel):
    host: str
    port: int


class Instances(BaseModel):
    instances: list[Instance]


class MySQLInstance:
    def __init__(self, user: str, password: str, host: str, port: int):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect_to_db(self):
        """
        Connect to the database
        :return: connection object
        """
        connection = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/sys')

        return connection

    def get_replicas_info(self):
        sql = '''show replicas'''
        connection = self.connect_to_db()
        pd_replicas_info = pd.read_sql(sql, connection)

        return pd_replicas_info

    def get_group_replication_info(self):
        sql = '''select * from performance_schema.replication_group_members'''
        connection = self.connect_to_db()
        pd_group_replication_info = pd.read_sql(sql, connection)

        return pd_group_replication_info

    def get_source_info(self):
        sql = '''select * from mysql.slave_master_info'''
        connection = self.connect_to_db()
        pd_source_info = pd.read_sql(sql, connection)

        return pd_source_info

    def is_single_instance(self):
        pd_replicas_info = self.get_replicas_info()
        pd_group_replication_info = self.get_group_replication_info()
        pd_source_info = self.get_source_info()

        if pd_replicas_info.empty and pd_group_replication_info.empty and pd_source_info.empty:
            return True
        else:
            return False

    def get_unused_indexes(self):
        sql_unused_index = '''
                select *
                from sys.schema_unused_indexes
                where object_schema not in
                      ('sys', 'information_schema',
                       'mysql', 'performance_schema',
                       'mysql_innodb_cluster_metadata')
        '''

        connection = self.connect_to_db()
        pd_unused_indexes = pd.read_sql(sql_unused_index, connection)

        return pd_unused_indexes


class MySQLInstanceGroup:
    def __init__(self, instances: Instances, user, password):
        self.instances: Instances
        self.user = user
        self.password = password
        self.instances = instances

    def get_common_unused_indexes(self):
        try:
            pd_common_unused_indexes = pd.DataFrame()
            for instance in self.instances.instances:
                if pd_common_unused_indexes.empty:
                    pd_common_unused_indexes = MySQLInstance(host=instance.host, port=instance.port, user=self.user,
                                                             password=self.password).get_unused_indexes()
                    continue

                pd_unused_indexes = MySQLInstance(host=instance.host, port=instance.port, user=self.user,
                                                  password=self.password).get_unused_indexes()
                pd_common_unused_indexes = pd.merge(pd_common_unused_indexes, pd_unused_indexes)

            return pd_common_unused_indexes
        except Exception as e:
            print(e)
            return pd.DataFrame()

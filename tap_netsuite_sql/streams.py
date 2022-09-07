import time

from tap_netsuite_sql.client import Client
from singer_sdk import typing as th
from singer_sdk import Stream


class SqlStream(Stream):
    def __init__(self, tap=None, query=None):
        self._query = query
        self._query_template = self._load_query_template()
        super().__init__(tap=tap)

    @property
    def name(self):
        """Return primary key dynamically based on user inputs."""
        return self._query["stream"]

    @property
    def primary_keys(self):
        return ["system_id"]

    def _load_query_template(self):
        with open(self._query["query"]) as f:
            return f.read()

    # @property
    # def replication_key(self):
    #     """Return replication key dynamically based on user inputs."""
    #     result = self.config.get("replication_key")
    #     if not result:
    #         self.logger.warning("Danger: could not find replication key!")
    #     return result

    @property
    def schema(self) -> dict:
        """Dynamically detect the json schema for the stream.
        This is evaluated prior to any records being retrieved.
        """

        fields = self._query["fields"]

        properties = [
            th.Property(field, th.StringType) for field in ["system_id", *fields]
        ]

        return th.PropertiesList(*properties).to_dict()

    def get_records(self, context):
        data = Client(config=self.config).send(self._query_template)

        for row in data:
            # record = [row.get(f, '') for f in self._query['fields']]
            record = row

            record["system_id"] = time.time_ns()
            yield record

"""NetsuiteSQL tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_netsuite_sql.streams import SqlStream


class TapNetsuiteSql(Tap):
    """NetsuiteSQL tap class."""

    name = "tap-netsuite-sql"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "account_id",
            th.StringType,
        ),
        th.Property(
            "consumer_key",
            th.StringType,
        ),
        th.Property(
            "consumer_secret",
            th.StringType,
        ),
        th.Property(
            "token_key",
            th.StringType,
        ),
        th.Property(
            "token_secret",
            th.StringType,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""

        return [
            SqlStream(tap=self, query=query) for query in self.config.get("queries")
        ]

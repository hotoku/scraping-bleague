# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import sqlite3
from datetime import date

from .items import BleagueItem


class Db:
    path: str = "db.sqlite"

    @classmethod
    def get(cls):
        con = sqlite3.connect(cls.path)
        con.row_factory = sqlite3.Row
        return con


_con = Db.get()
_con.cursor().executescript("""
drop table if exists matches;
create table if not exists matches
(
  id integer primary key,
  year integer not null,
  month integer not null,
  day integer not null,
  dow text not null,
  start_time text not null,
  home text not null,
  away text not null,
  arena text not null default ""
)
""")


class BleaguePipeline:
    dow = [
        "sun", "mon", "tue", "wed",
        "thu", "fri", "sat"
    ]

    def process_item(self, item, _):
        if not isinstance(item, BleagueItem):
            return item
        con = Db.get()
        d = date(int(item["year"]), int(item["month"]), int(item["day"]))

        con.cursor().execute("""
        insert into matches (
        year,       month, day,  dow,
        start_time, home,  away, arena
        ) values (
        ?, ?, ?, ?,
        ?, ?, ?, ?
        )
        """, [
            int(item["year"]), int(item["month"]), int(item["day"]),
            self.dow[d.weekday()],
            item["start_time"], item["home"], item["away"], item["arena"]
        ])
        con.commit()
        return item

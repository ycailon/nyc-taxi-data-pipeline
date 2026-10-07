# Engineering decisions

## Monthly partitions instead of one giant file

TLC publishes the source by month, so I keep that boundary in the raw layer. It makes retries and backfills easier and avoids rebuilding the entire dataset when only one month changes.

## A manifest controls idempotency

A successful month is written to `data/manifest.json`. A normal rerun skips it. `--force` is available when I intentionally want to replace a month.

## Schema normalization before loading

TLC has changed fields over time. The canonical model includes optional/newer fields and applies controlled defaults when an older source file legitimately does not have them.

## Keep rejected records

Bad records are exported with a reason instead of disappearing through a filter.

## SQLite for the runnable portfolio version

The project demonstrates warehouse tables, indexes, joins and marts without making the reviewer install a database server. The storage adapter can later be replaced with Postgres or a cloud warehouse.

# Parquet Storage Patterns

Use Parquet for analytical columnar storage when consumers benefit from column projection, predicate pruning, compression, and typed schemas.

## Schema

Define a stable logical schema before writing:

- field names and types
- nullability
- decimal precision and scale
- timestamp unit and timezone
- list, struct, and map semantics
- schema version

Do not rely on one DataFrame sample to choose permanent types.

## Partitioning

Partition on columns that are frequently filtered and have bounded cardinality, commonly date or coarse tenant groups.

Avoid:

- unique identifiers
- free-form strings
- overly deep year/month/day/hour trees for small datasets
- partitions so small that metadata dominates reads

Estimate files per partition and expected query pruning before choosing keys.

## File and Row Group Sizing

Target measured byte sizes rather than universal row counts. Consider:

- object-store request overhead
- worker memory
- compression ratio
- scan parallelism
- expected filter columns

Compact uncontrolled small files. Choose row groups large enough for efficient scans but small enough for useful statistics-based pruning.

## Projection and Filtering

Reading selected columns is column projection, not predicate pushdown. Row filtering can use row-group statistics and partition pruning when the reader and expression support them.

Verify pruning through the actual query engine. A filter argument in client code does not guarantee that every backend avoids reading all data.

## Compression

Select based on measured workload:

- Snappy for low CPU cost and broad compatibility
- Zstandard for stronger compression with good general performance
- Gzip when compatibility or compression ratio outweighs CPU cost

Benchmark representative data and consumers.

## Schema Evolution

Classify changes:

- additive nullable field
- removal
- rename
- type widening
- type narrowing
- nullability change
- semantic or unit change

File readers differ in schema unification behavior. Test mixed-version partitions. Avoid rewriting types automatically merely because a library can find a common physical type.

## Publication

Parquet files alone do not provide table transactions. For pipeline output:

- write immutable files under a run or version prefix
- validate files and schema
- publish a manifest or catalog version atomically
- keep previous versions for rollback
- prevent concurrent writers from owning the same partition

Use a transactional table format when concurrent updates, deletes, snapshots, or reliable schema evolution require it.

## Metadata and Provenance

Record outside or alongside files:

- pipeline and schema version
- source cursor or partition
- row count and control totals
- creation time
- writer library and version
- partition values
- validation status

Do not put secrets or unnecessary personal data in file metadata.

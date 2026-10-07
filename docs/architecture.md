# Architecture

```mermaid
flowchart LR
    A[NYC TLC monthly Parquet] --> B[Downloader]
    B --> C[Raw monthly partition]
    C --> D[Schema normalization]
    D --> E[Data quality rules]
    E -->|Valid| F[(SQLite warehouse)]
    E -->|Rejected| G[Rejected-row report]
    F --> H[SQL marts]
    H --> I[CSV analytics outputs]
    B --> J[Manifest]
    J --> B
```

The live path keeps each TLC month as a separate raw Parquet file. A manifest records successfully processed months so a normal rerun does not download and load the same month again.

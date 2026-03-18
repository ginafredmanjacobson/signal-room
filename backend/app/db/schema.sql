CREATE TABLE IF NOT EXISTS collections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    collection_id INTEGER,
    source TEXT,
    source_id TEXT,
    url TEXT,
    title TEXT,
    text TEXT,
    author TEXT,
    created_at TEXT,
    fetched_at TEXT,
    UNIQUE(source, source_id),
    FOREIGN KEY (collection_id) REFERENCES collections(id)
);

# `.flet/`

This directory is created by `flet run` to hold per-project development state. It is local to your machine, safe to delete (it will be recreated on the next run), and git-ignored via the `.gitignore` next to this file.

While `flet run` is active, your app's working directory is `storage/data` and the three storage locations are exposed to your Python code through the `FLET_APP_STORAGE_*` environment variables — matching how a packaged app behaves on a device.

## `storage/`

- **`data/`** (`FLET_APP_STORAGE_DATA`) — durable application data: databases, settings, user files. This is also the process current working directory, so relative paths (e.g. `sqlite3.connect("my.db")`) land here. Persists across runs; the equivalent of this dir is preserved across app updates on a device.
- **`cache/`** (`FLET_APP_STORAGE_CACHE`) — regenerable cache data. The OS may purge the equivalent dir on a device under storage pressure, so only store things you can rebuild.
- **`temp/`** (`FLET_APP_STORAGE_TEMP`) — throwaway scratch space. Python's `tempfile` is pointed here too. May be cleared at any time.

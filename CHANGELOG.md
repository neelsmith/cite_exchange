# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## 0.3.0 - 2026-03-02

### Changes

- removed all runtime dependencies on `pydantic` and `requests`
- refactored `CexBlock` to use standard-library `dataclass`
- replaced URL fetching implementation with `urllib.request` from the Python standard library


## 0.2.0 - 2026-02-03

### Changes

- no changes in functionality
- changed underlying dependencies so packge can be compiled to HTML-WASM in a marimo notebook


## 0.2.0 - 2026-01-14 

### Added

- Added `to_cex` method to `CexBlock` class for converting block data back to CEX format.


## 0.1.0 - 2026-01-14 

Initial release.

### Added

- Implemented `CexBlock` class for parsing CEX-format data from strings, files and URLs.
- Added methods to filter blocks by label.
- Included example usage in the README.


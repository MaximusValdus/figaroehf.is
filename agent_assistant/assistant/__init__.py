"""A personal agent assistant.

Modular building blocks:
    - connectors:  integrations with external systems (mock for the MVP)
    - tools:       a uniform, permission-aware interface over connectors
    - services:    higher-level features (daily brief, approval workflow)
    - db / models: SQLite-backed memory
    - api:         FastAPI HTTP surface
    - cli:         command-line entry points
"""

__version__ = "0.1.0"

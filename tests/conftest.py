# Patch pydantic for FastAPI/gradio compatibility when using Pydantic v2.
# Old FastAPI (pulled in by gradio 4.19.2) does "from pydantic import Schema",
# but Schema was removed in Pydantic v2; Field is the replacement.
# Run in pytest_configure so it happens before any test module is imported.


def pytest_configure(config):
    import pydantic

    if not hasattr(pydantic, "Schema"):
        pydantic.Schema = pydantic.Field

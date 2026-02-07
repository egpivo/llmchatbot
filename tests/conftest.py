# Patch pydantic for FastAPI/gradio compatibility when using Pydantic v2.
# Old FastAPI (pulled in by gradio 4.19.2) uses "class Param(Schema)" and
# Schema was removed in Pydantic v2. Use FieldInfo as the replacement so Param
# can inherit and Schema(...) calls work for parameter metadata.
# Run in pytest_configure so it happens before any test module is imported.


def pytest_configure(config):
    import pydantic

    if not hasattr(pydantic, "Schema"):
        from pydantic.fields import FieldInfo

        pydantic.Schema = FieldInfo

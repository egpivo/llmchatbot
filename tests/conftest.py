# Patch pydantic for FastAPI/gradio compatibility when using Pydantic v2.
# Old FastAPI (from gradio 4.19.2) uses Schema and pydantic.types.UrlStr,
# both removed in v2. Run in pytest_configure before any test module is imported.


def pytest_configure(config):
    import pydantic

    if not hasattr(pydantic, "Schema"):
        from pydantic.fields import FieldInfo

        pydantic.Schema = FieldInfo

    # Pydantic v2 removed UrlStr; FastAPI openapi/models.py does "from pydantic.types import UrlStr"
    import pydantic.types as ptypes

    if not hasattr(ptypes, "UrlStr"):
        try:
            ptypes.UrlStr = pydantic.AnyUrl
        except AttributeError:
            ptypes.UrlStr = str

# Root cause: gradio 4.19.2 brings in an old FastAPI built for Pydantic v1,
# while the stack uses Pydantic v2. bentoml 1.0.18 pins starlette <0.26 so we
# cannot upgrade FastAPI. Patching pydantic (Schema, UrlStr, EmailStr, …) is
# fragile. So viewer tests skip when gradio is not importable (see
# tests/view/test_viewer.py). No conftest patches needed.

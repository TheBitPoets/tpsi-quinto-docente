from app.main import create_app
from app.settings import RuntimeSettings

def test_openapi_keeps_product_paths_and_adds_operational_paths():
    app=create_app(RuntimeSettings("test","sqlite:///:memory:","openapi"))
    schema=app.openapi(); paths=schema["paths"]
    for path in ("/api/posts","/api/posts/{post_id}","/health","/ready"): assert path in paths
    schemas=schema["components"]["schemas"]
    for name in ("Post","PostCreate","PostLikePatch"): assert name in schemas
    app.state.engine.dispose()

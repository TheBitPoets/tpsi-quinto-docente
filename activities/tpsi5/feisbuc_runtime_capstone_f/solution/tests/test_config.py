import pytest
from app.settings import RuntimeConfigError, load_settings

def test_development_default_is_local_sqlite():
    s=load_settings({})
    assert s.environment=="development"
    assert s.database_url=="sqlite:///./feisbuc-mirror.db"
    assert s.build_sha=="dev"

def test_production_requires_database_url():
    with pytest.raises(RuntimeConfigError): load_settings({"FEISBUC_ENV":"production"})

def test_explicit_runtime_values_are_used():
    s=load_settings({"FEISBUC_ENV":"test","FEISBUC_DATABASE_URL":"sqlite:///x.db","FEISBUC_BUILD_SHA":"abc"})
    assert (s.environment,s.database_url,s.build_sha)==("test","sqlite:///x.db","abc")
    assert not hasattr(s,"port") and not hasattr(s,"workers") and not hasattr(s,"reload")

import os
import pytest
from unittest import mock
from airflow.models import Variable 


@pytest.fixture
def api_key():
    with mock.patch.dict("os.environ",AIRFLOW_VAR_API_KEY="MOCK_KEY1234"):
        yield Variable.get("API_KEY")

@pytest.fixture
def channel_handle():
    with mock.patch.dict("os.environ",AIRFLOW_VAR_CHANNEL_HANDLE="GBOLUWAGA"):
        yield Variable.get("CHANNEL_HANDLE")

@pytest.fixture
def elt_database_name():
    with mock.patch.dict("os.environ",AIRFLOW_VAR_ELT_DATABASE_NAME="elt"):
        yield Variable.get("ELT_DATABASE_NAME")
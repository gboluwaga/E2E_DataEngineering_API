def test_api_key(api_key):
    assert api_key == "MOCK_KEY1234"

def test_channel_handle(channel_handle):
    assert channel_handle == "GBOLUWAGA"

def test_elt_database_name(elt_database_name):
    assert elt_database_name == "elt"

def test_mock_postgres_conn_vars(mock_postgres_conn_vars):
    assert mock_postgres_conn_vars.login == "mock_username"
    assert mock_postgres_conn_vars.password == "mock_password"
    assert mock_postgres_conn_vars.host == "mock_host"
    assert mock_postgres_conn_vars.port == 1234
    assert mock_postgres_conn_vars.schema == "mock_db_name"

def test_dags_integrity(dagbag):
    # 1.
    assert dagbag.import_errors == {}, f"Import errors found: {dagbag.import_errors}"
    print("===========")
    print(dagbag.import_errors)

    # 2.
    expected_dag_ids = ["youtube_video_statistics_dag", "update_db", "data_quality_checks"]
    loaded_dag_ids = list(dagbag.dags.keys())
    print("===========")
    print(dagbag.dags.keys())

    for dag_id in expected_dag_ids:
        assert dag_id in loaded_dag_ids, f"DAG {dag_id} is missing."

    # 3.
    assert dagbag.size() == 3
    print("===========")
    print(dagbag.size())

    # 4.
    expected_task_counts = {
        "youtube_video_statistics_dag": 4,
        "update_db": 2,
        "data_quality_checks": 2,
    }
    print("===========")
    for dag_id, dag in dagbag.dags.items():
        expected_count = expected_task_counts[dag_id]
        actual_count = len(dag.tasks)
        assert (
            expected_count == actual_count
        ), f"DAG {dag_id} has {actual_count} tasks, expected {expected_count}."
        print(dag_id, len(dag.tasks))
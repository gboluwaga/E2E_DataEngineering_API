from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_statistics import get_playlistid, get_video_id, extract_video_data, save_as_json_to_file_path
from datawarehouse.dwh import staging_table, core_table
from dataquality.soda import yt_elt_data_quality
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

local_tz = pendulum.timezone("Africa/Lagos")

default_args = {
    'owner': 'gboluwaga',
    'depends_on_past': False,
    'email_on_failure': False,              
    'email_on_retry': False,
    #'retries': 1,
    #'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 1, tzinfo=local_tz),
    #'schedule_interval': '@daily',
    'dagrun_timeout': timedelta(hours=1),
    #'end_date': None,
    'max_active_runs': 1,
}

#variables
staging_schema ="staging"
core_schema = "core"

#1 dag produce youtube video statistics and save as json


with DAG(
    dag_id='youtube_video_statistics_dag',
    default_args=default_args,
    description='A DAG to extract YouTube video statistics and save as JSON',
    schedule_interval='0 * * * *',
    catchup=False,
) as dag_produce:

    #Define Task
    playlist_id = get_playlistid()
    video_ids = get_video_id(playlist_id)
    extracted_data = extract_video_data(video_ids)
    save_to_json = save_as_json_to_file_path(extracted_data)

    trigger_update_db = TriggerDagRunOperator(
        task_id="trigger_update_db",
        trigger_dag_id="update_db",
    )

    #define task dependencies
    playlist_id >> video_ids >> extracted_data >> save_to_json >> trigger_update_db



#2 dag update staging and core table
with DAG(
    dag_id='update_db',
    default_args=default_args,
    description='Insert and Update and staging and core table',
    schedule_interval='0 */2 * * *',
    catchup=False,
    schedule = None,
) as dag_update:

    #Define Task
    staging_tables = staging_table()
    core_tables = core_table()

    trigger_data_quality  = TriggerDagRunOperator(
        task_id="trigger_data_quality ",
        trigger_dag_id="data_quality_checks",
    )

    #define task dependencies
    staging_tables >> core_tables >> trigger_data_quality   

#3 dag data quality check using soda
with DAG(
    dag_id='data_quality_checks',
    default_args=default_args,
    description='Run data quality checks using Soda',
    schedule_interval='0 */4 * * *',
    catchup=False,
    schedule = None,
) as dag:

    #Define Task
    soda_staging_validation = yt_elt_data_quality(staging_schema)
    soda_core_validation = yt_elt_data_quality(core_schema)

    #define task dependencies
    soda_staging_validation >> soda_core_validation
from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_statistics import get_playlistid, get_video_id, extract_video_data, save_as_json_to_file_path
from datawarehouse.dwh import staging_table, core_table

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


with DAG(
    dag_id='youtube_video_statistics_dag',
    default_args=default_args,
    description='A DAG to extract YouTube video statistics and save as JSON',
    schedule_interval='0 * * * *',
    catchup=False,
) as dag:

    #Define Task
    playlist_id = get_playlistid()
    video_ids = get_video_id(playlist_id)
    extracted_data = extract_video_data(video_ids)
    save_to_json = save_as_json_to_file_path(extracted_data)

    #define task dependencies
    playlist_id >> video_ids >> extracted_data >> save_to_json


with DAG(
    dag_id='update_db',
    default_args=default_args,
    description='Insert and Update and staging and core table',
    schedule_interval='0 */2 * * *',
    catchup=False,
) as dag:

    #Define Task
    staging_tables = staging_table()
    core_tables = core_table()

    #define task dependencies
    staging_tables >> core_tables
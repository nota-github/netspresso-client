import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from netspresso_cli.onprem import monitoring_apis
from netspresso_cli.onprem import compression
from netspresso_cli.onprem import auth

# common apis(without login)
user_id = "user_etri"
user_pw = "RevsJ8y529BQxYLE"
user_info = auth.login(user_id, user_pw)
user_key = user_info["user_key"]
# print(monitoring_apis.is_alive())
# print(monitoring_apis.get_compression_status_index())
# print(monitoring_apis.get_compression_progress_index())
# print(monitoring_apis.get_worker_status_list()) # this endpoint should be included in CLI client?
# print(monitoring_apis.get_task_queue_status()) # this endpoint should be included in CLI client?

# compression related apis(with login)
# print(monitoring_apis.get_compression_list(user_key))
# compression_info = compression.create_compression(user_key)
# compression_id = compression_info["compression_id"]
# compression_id = "7f78f5a4-f6e7-4666-af50-d4c4c14dce54"
# print(monitoring_apis.get_compression_status(user_key, compression_id))
# print(compression.delete_compression(user_key, compression_id).json())
# print(monitoring_apis.get_compression_result_list(user_key))
# print(monitoring_apis.get_compression_result(user_key, compression_id))
# print(monitoring_apis.get_task_queue_list(user_key))
# print(compression.delete_task_queue(user_key, compression_id))
# print(monitoring_apis.get_compression_progress_details(user_key, compression_id))
# print(monitoring_apis.get_one_compression_in_progress(user_key))
# time.sleep(5); print(compression.kill_core_process(user_key, compression_id)) # if success, returns success message
# time.sleep(5); print(compression.restart_process(user_key, compression_id)) # if success, returns compression_id

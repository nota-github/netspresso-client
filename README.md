# netspresso-client
## Overview

- 입력된 yaml 형태의 config 경로를 읽고, config, data, model을 aws에 업로드 한다.
- Core쪽에 API request(compressions/create)를 보낸다.
- Core쪽에서 완료 progress(3)이 넘어올 때 까지 주기적으로 status를 print한다.
- Core쪽 process가 완료된 후에는 aws로부터 결과와 모델 파일등을 다운로드 받는다.

## Code Flow(main.py)

### 1. Upload config, data, model

```python
 # Upload config, data, model
comp_sess.upload_config(config_path=args.config, storage_config=configs["STORAGE"])
comp_sess.upload_data(data_path=configs["DATASET"]["path"], dataset_type=configs["DATASET"]["type"], storage_config=configs["STORAGE"])
comp_sess.upload_model(model_path=configs["INPUT"]["path"], model_type=configs["INPUT"]["type"], storage_config=configs["STORAGE"])
```

### 2. Run compression session

```python
compression_id = comp_sess.compress()
```

### 3. Monitor compression

```python
    while True:
        current_status = get_compression_status(compression_id, return_type=ReturnDataType.JSON)
        current_compression_id = current_status["compression_id"]
        print("==========current status==========")
        print(current_status)
        print("==================================")
        if current_compression_id == None: # 요청한 compression_id가 없는 경우, 프로그램 종료
            print(f"compression_id({current_compression_id}) does not exists")
            exit(0)
        elif current_status["status"] != 0: # 도중에 error가 발생한 경우(status!=0), 프로그램 종료
            print("error in progressing")
            exit(0)
        elif current_status["progress"] == 1: # compression task가 queue에서 대기하고 있음.
            print("[*] compression task in queue!")
            print("[*] currently stacked compression queue size : ", get_task_queue_size())
        elif current_status["progress"] == 2:
            print("[*] compression is in progress.")
        elif current_status["progress"] == 3: # 정상적으로 프로세스가 완료된 경우
            print("compression completed!")
            break
        print(f"[*] running time in current step: ", calculate_duration(time_from=current_status["updated_time"]))
        print(f"[*] total time: ", calculate_duration(time_from=current_status["created_time"]))
        print("\n\n")
        time.sleep(20)
```

### 4. Download result

```python
aws_auth_info = aws_connection.get_auth()
    result = get_result(compression_id, return_type=ReturnDataType.JSON)
    print(result)
    log_file = aws_connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=result["url_log"])
    print(f"[*] log file(filename: {log_file}) saved")
    input_type_compressed_model = aws_connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=result["url_input_type_compressed_model"])
    print(f"[*] input type compressed model(filename: {input_type_compressed_model}) saved")
    converted_type_compressed_model = aws_connection.download_result_from_s3_with_url(aws_auth_info, compression_id, s3_url=result["url_converted_type_compressed_model"])
    print(f"[*] converted type compressed model(filename: {converted_type_compressed_model}) saved")
```



## Modules

### 1. Compress Session(modules/compression_sessions.py)

#### Class purpose

1. config, data, model을 cloud(s3)로 업로드
2. compression session을 수행(core를 구동)

#### Class attribute

#### Class methods

- upload_config
  ```python
  """Upload config to s3.
  
  Args:
      config_path (str): config yaml file path 
      storage_config (Dict[str, Any]): storage config
  
  Return:
      bool: Whether its valid config
  """
  ```

-  upload_data
  ```python
  """Upload data to s3.
  
  Args:
      data_path (str):  
      storage_config (Dict[str, Any]): storage config
      dataset_type (str): type of dataset: ["imagefolder", "npy"]
  """
  ```

- upload_model
  ```python
  """Upload model.
  
  Args:
      model_path (str): path to model
      storage_config (Dict[str, Any]): storage config from user_config
      model_type (str): type of model [pb, h5]
  """
  ```

- compress
  ```python
  """Requests create to core.
  
  Return:
      str: compression id
  """
  ```
 

### 2. Monitoring(modules/monitoring_apis.py)

netspresso_server 쪽으로 monitoring 요청을 보내는 함수들의 모음

각 API requests들의 return은 [netspresso-server](https://github.com/nota-github/netspresso-server/blob/develop/netspresso_server/urls.py) 를 확인

## Run
requirements.txt가 설치된 환경에서 구동
AWS 로그인 정보가 필요
```python
export PYTHONPATH=. && python netspresso_cli/main.py --login
```
```python
export PYTHONPATH=. && python netspresso_cli/main.py --config config_files/example1.yaml
```

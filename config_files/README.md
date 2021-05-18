# Tutorial config 설명

## Overview

- tutorial0_quickstart.yaml: 모델 경량화 과정 없이 전체 과정의 동작 및 반환 데이터를 확인하기 위한 quickstart
- tutorial1_imagefolder.yaml: 이미지폴더형태 데이터셋을 활용한 compression
- tutorial2_npy.yaml: npy파일 데이터셋을 활용한 compression
- tutorial3_local.yaml: local에서 입력해주는 모델, 데이터셋에 대한 compression
- tutorial4_tf22.yaml: tf 2.2 버전에서의 compression(tf 2.3에 대해서는 동작하지 않음)

## Note

1. `tutorial2_npy.yaml` 의 경우 `yaml` 내의 `acceptable_drop_percent_point`, 즉 허용 하락 성능의 마진이 5%로 상대적으로 작아서, compression이 다른 tutorial 대비 긴 시간동안 수행됩니다.
2. `tutorial3_local.yaml` 의 경우 테스트 시 경로를 로컬에 저장되어있는 모델, 데이터셋 경로로 변경해주세요.
3. `tutorial4_tf22.yaml` 의 경우 tf 2.2 버전 이미지에서 동작을 테스트하기 위한 `yaml`로, tf 2.3 이미지에서는 동작하지 않습니다.

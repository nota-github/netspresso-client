# netspresso-client
## Overview

- 입력된 yaml 형태의 config 경로를 읽고, config, data, model을 aws에 업로드 한다.
- Core쪽에 API request(compressions/create)를 보낸다.
- Core쪽에서 완료 progress(3)이 넘어올 때 까지 주기적으로 status를 print한다.
- Core쪽 process가 완료된 후에는 aws로부터 결과와 모델 파일등을 다운로드 받는다.

## Acknowledgement
This work was supported by Institute of Information & communications
Technology Planning & Evaluation (IITP) grant funded by the Korea
government (MSIT) (No. 2021-0-00907, Development of Adaptive and
Lightweight   Edge-Collaborative   Analysis   Technology   for   Enabling
Proactively Immediate Response and Rapid Learning)

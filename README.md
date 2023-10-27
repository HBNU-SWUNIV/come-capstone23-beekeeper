# 한밭대학교 컴퓨터공학과 BeeKeeper팀

**팀 구성**
- 20172597 고무서 
- 20172604 노호성
- 20172607 안종현

## <u>Teamate</u> Project Background
 적 드론 추적 알고리즘의 필요성
  - 드론 산업의 성장에 따라서 일반 시민들도 쉽게 드론을 구매하여 사용 가능 → 드론 수요 증가에 따라 드론을 이용한 범죄율 증가
  - 적 드론 검출, 드론 위치 예측, 대응 드론의 출격 및 트래킹을 통하여 적 드론의 전략적 운용 가능 

## 적 드론 대응 시나리오
![image](https://github.com/HBNU-SWUNIV/come-capstone23-beekeeper/assets/127067204/94d1110a-f198-4abb-9994-fc6588ff0f01)
1. 지상 관제 메인 컴퓨터(MC)에 설치된 캠을 통해 식별된 상공의 적 드론의 위치정보 수신
2. 추적용 드론에 적 드론의 정보를 전송, 해당 정보들을 이용하여 추적용 드론이 적 드론을 식별
3. 적 드론의 움직임에 따라 추적용 드론의 화면 중앙에 적 드론이 위치하도록 추적용 드론의 방향 조정 후 트래킹 진행 

## System Design
  - ### System Requirements
    - Python 3.10
    - OpenCV 4.8.1
    - Tello
    - YOLOv4
    - CUDA 11.8
      
  - ### System Architecture
![image](https://github.com/HBNU-SWUNIV/come-capstone23-beekeeper/assets/127067204/fed5f702-a33c-46c6-973b-e24aceafdfbb)
  
  - 위치에 따른 x, d값을 이용하여 𝜙 값을 알아낸 후 추적용 드론에 값을 전송, 최종적으로 계산된 yaw 값을 이용하여 적 드론과 유사한 위치로 추적용 드론을 출동
    
![image](https://github.com/HBNU-SWUNIV/come-capstone23-beekeeper/assets/127067204/bfcf55e4-cc8f-46a0-afcc-5fd6d49afff5)


  - 객체 인식 시 화면에 나오는 바운딩 박스(Bounding Box)를 통해 물체와 카메라 사이의 거리 예측
  - 카메라의 초점 거리(Focal length)와 드론의 실제 너비(Known width), 바운딩 박스의 넓이를 이용한 (Known_width * focal_length ) / bbox_width 공식을 활용


## Case Study
  - ### 동적 카메라 환경에서의 소형 드론 추적 방법
 ![image](https://github.com/HBNU-SWUNIV/come-capstone23-beekeeper/assets/127067204/6b306e21-8529-4424-8b36-0931701bbc52)

   - 연속되는 두 프레임 사이의 이미지 밝기 변화에서 각 픽셀의 움직임을 복구하기 위해 옵티컬 플로우 수행 
   - 칼만 필터와 혼합하여 PTZ 카메라에서 소형 드론 추적
    
  - ### 군집 비행을 이용한 불법 드론 추적 기법
    - 소형 드론의 무리로 구성된 군집 드론을 통해 불법 드론을 추적하는 시스템을 연구하였다. 기존 방식 대비 이동 횟수를 63%로 개선하였지만, 군집 드론 수신기의 이격 거리로 인하여 큰 폭의 오차가 발생하기도 하였다. 
## Conclusion
  -  본 프로젝트에서는 적 드론 검출, 드론 위치 예측, 대응 드론 출격의 3단계로 구성되는 알고리즘을 제안하였음. 
  -  적 드론의 속도에 따라 영상의 프레임 한계로 인해 트래킹에 실패하는 경우가 발생했으며, 이는 사용하는 캠의 성능과 메인 컴퓨터(MC)의 그래픽 가속 등으로 개선할 수 있음.
  
## Project Outcome
- ### 2023 년 한국통신학회 하계종합학발표회
[적 드론 대응을 위한 드론 추적 알고리즘 구현]

[단안 카메라 기반의 드론 검출 및 측위에 관한 연구]

[YOLOv7 기반 드론 경로 예측에 관한 연구]

- ### Reference
[1] Davidovich Barak." Towards the Detection of GPS Spoofing Attacks against Drones by Analyzing Camera's Video Stream.
[2] 최민우, 조남석 "Simulation Study on Search Strategies for the Reconnaissance Drone," 한국시뮬레이션학회 논문지, Vol. 28, No. 1, pp. 
23-39, 2019.
[4] Chang, Yunseok, "An enhanced rerouting cost estimation algorithm towards internet of drone." Journal of Supercomputing. Vol. 76, 
Issue 12, p10036-10049, 2020.
[5] https://www.droneportal.or.kr/subList/22000000118, 드론정보포털 드론 산업체 현황
[6] 손소희, 전진우, 이인재, 차지훈, 최해철. (2019). 동적 카메라 환경에서의 소형 드론 추적 방법. 방송공학회논문지, 24(5), 802-812.


# 한밭대학교 컴퓨터공학학과 BeeKeeper팀

**팀 구성**
- 20172597 고무서 
- 20172604 노호성
- 20172607 안종현

## <u>Teamate</u> Project Background
 적 드론 추적 알고리즘의 필요성
  - 드론 산업의 성장에 따라서 일반 시민들도 쉽게 드론을 구매하여 사용 가능 → 드론 수요 증가에 따라 드론을 이용한 범죄율 증가
  - 적 드론 검출, 드론 위치 예측, 대응 드론의 출격 및 트래킹을 통하여 적 드론의 전략적 운용 가능 
- ### 기존 해결책의 문제점
  - OOO
  - OOO
  
## System Design
  - ### System Requirements
  - ### System Architecture
![image](https://github.com/HBNU-SWUNIV/come-capstone23-beekeeper/assets/127067204/fed5f702-a33c-46c6-973b-e24aceafdfbb)
  
  - 위치에 따른 x, d값을 이용하여 𝜙 값을 알아낸 후 추적용 드론에 값을 전송, 최종적으로 계산된 yaw 값을 이용하여 적 드론과 유사한 위치로 추적용 드론을 출동
    
![image](https://github.com/HBNU-SWUNIV/come-capstone23-beekeeper/assets/127067204/bfcf55e4-cc8f-46a0-afcc-5fd6d49afff5)


  - 객체 인식 시 화면에 나오는 바운딩 박스(Bounding Box)를 통해 물체와 카메라 사이의 거리 예측
  - 카메라의 초점 거리(Focal length)와 드론의 실제 너비(Known width), 바운딩 박스의 넓이를 이용한 (Known_width * focal_length ) / bbox_width 공식을 활용

    - OOO
    
## Case Study
  - ### 동적 카메라 환경에서의 소형 드론 추적 방법
 ![image](https://github.com/HBNU-SWUNIV/come-capstone23-beekeeper/assets/127067204/6b306e21-8529-4424-8b36-0931701bbc52)

  - 연속되는 두 프레임 사이의 이미지 밝기 변화에서 각 픽셀의 움직임을 복구하기 위해 옵티컬 플로우 수행 
  - 칼만 필터와 혼합하여 PTZ 카메라에서 소형 드론 추적
    
## Conclusion
  - ### OOO
  - ### OOO
  
## Project Outcome
- ### 2023 년 한국통신학회 하계종합학발표회 [ 적 드론 대응을 위한 드론 추적 알고리즘 구현]

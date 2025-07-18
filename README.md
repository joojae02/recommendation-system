# Recommendation System with AWS Personalize

## 데이터 디렉토리 구조

```
recommendation-system/
├── infra/
│   ├── data/
│   │   ├── data_download.ipynb    # MovieLens 데이터 다운로드 및 전처리
│   │   ├── export_data.py         # 데이터를 CSV로 변환하는 스크립트
│   │   └── csv/                  # 변환된 CSV 파일들
│   └── schemas/
│       ├── user-schema.json      # 사용자 스키마 정의
│       ├── item-schema.json      # 아이템 스키마 정의
│       └── interaction-schema.json # 인터랙션 스키마 정의
```

## infra


### AWS Personalize 인프라 생성 순서 (Terraform, Scripts)

1. **Terraform 초기화**
   ```bash
   cd infra
   terraform init
   ```

2. **Terraform 실행 계획 확인**
   ```bash
   terraform plan
   ```

3. **인프라 생성**
   ```bash
   terraform apply
   ```

4. **초기 데이터 import**
    ```bash
    sh scripts/import_data.sh
    ```

### 생성되는 리소스
- 데이터셋 그룹
- 사용자/아이템/상호작용 스키마
- 데이터셋
- 데이터 임포트 작업 (스크립트 사용)
  - `sh infra/scripts/import_data.sh`
- 솔루션 (주석 처리)

### 주의사항
- Terraform 실행 전 AWS 자격 증명이 올바르게 설정되어 있어야 합니다.
  - profile: terraform을 사용합니다.
- 데이터 임포트 작업이 완료될 때까지 기다린 후 다음 단계로 진행해야 합니다.
  - `sh infra/scripts/import_data.sh` 를 사용하여 초기 데이터를 등록합니다.



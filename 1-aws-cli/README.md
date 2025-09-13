## AWS CLI 기본 사용법

### 1. 설치 여부 확인
```
aws --version
```
만약 `command not found` 에러가 뜨면 AWS CLI 설치 필요!

Mac:
```
brew install awscli
```

Linux:
```
sudo apt-get update
sudo apt-get install awscli -y
```

Powershell:
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html 사이트에서 설치

### 2. 자격 증명 설정
```
aws configure list
```
출력 예시
```
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                  <not set>             None
access_key     ****************ABCD              env
secret_key     ****************XYZ1              env
    region                ap-northeast-2      config
```

초기 설정 방법!
```
aws configure
```
순서대로 입력:
```
AWS Access Key ID [None]: (IAM 콘솔에서 발급받은 Access Key)
AWS Secret Access Key [None]: (IAM 콘솔에서 발급받은 Secret Key)
Default region name [None]: ap-northeast-2   # 서울 리전
Default output format [None]: json
```

#### Access Key 발급받기!
**주의**: 되도록이면 루트 계정이 아닌 IAM 사용자 계정을 만들어서 진행해봅시다.

1. IAM 사용자 계정 생성
![alt text](1-create-user.png)
사용자 생성 클릭

![alt text](2-user-info.png)
그림과 같이 체크박스를 눌러주세요!

![alt text](3-permission-settings.png)
(실습이니까...) Admin 권한으로 하나 만들어줍시다~

이렇게 IAM 사용자를 만들어주고, 로그인 해줍시다!

2. Access Key 발급받기
콘솔 -> IAM -> 사용자(Users) -> 만든 IAM 계정 클릭
![alt text](4-security-credentials.png)
![alt text](5-access-key1.png)
Access 키 만들기 클릭
![alt text](6-access-key2.png)
![alt text](7-access-key3.png)

### 3. 연결 성공 여부 확인
```
aws sts get-caller-identity
```
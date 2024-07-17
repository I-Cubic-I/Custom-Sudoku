# Custom-Sudoku

Sudoku Variants 특수 모드들에 대한 세부 규칙을 자동으로 판정해주는 UI를 제공합니다.

이 게임에서 사용된 모든 스도쿠 변형 규칙은 pillowprism에게 권한이 있으며,\
변형 규칙의 자세한 정보는 [Pillow's Sudoku Variants](https://discord.com/invite/aJPwNY7g6g) 서버에서 확인하실 수 있습니다.

## 변형 규칙
[최신 버전](https://github.com/I-Cubic-I/Custom-Sudoku/releases/latest)에서 오답 판별을 지원하는 변형 규칙들은 다음과 같습니다.
- 지원: DT, TP, CR, RO, SD, FX, QT, LI, RM, QD, CT
- 미지원: AS

## 사용 방법
### 메인
1. 설명이 표시되는 텍스트 박스입니다. 3번의 각 모드에 마우스를 올리면 해당 모드에 대한 설명이 표기됩니다.
2. 스도쿠 틀을 입력하는 입력 필드입니다. 텍스트는 기본으로 제공되는 형식과 유사한 형태로 주어져야 합니다.
3. 스도쿠의 특수 모드를 선택할 수 있는 리스트입니다.
4. 올바른 스도쿠와 모드가 입력되면 게임을 시작할 수 있는 버튼입니다.
   
![image](https://github.com/I-Cubic-I/Custom-Sudoku/assets/58257896/69a616c2-293c-4996-9630-47795037586d)

### 게임
마우스 커서로 셀을 선택하거나 WASD, 화살표 키로 이동할 수 있습니다.

Ctrl 또는 Shift 키를 누른 채로 조작하면 다중 셀을 선택할 수 있습니다.

선택한 셀에는 숫자 키로 입력이 가능하고, BackSpace 또는 Delete 키로 지울 수 있습니다.

ESC로 게임을 일시정지 하며, 메인으로 돌아갈 수 있는 버튼을 제공합니다.

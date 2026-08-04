
# 🛠️ Multi-Utility Project: Calculator & Book Management System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Language](https://img.shields.io/badge/language-Python-green.svg) <!-- 사용한 언어로 변경하세요 -->

계산기 기능과 도서 관리 기능을 하나로 통합한 유틸리티 프로그램입니다. 직관적인 인터페이스와 효율적인 데이터 처리를 목표로 개발되었습니다.

---

## 📌 주요 기능 (Features)

### 🔢 1. 계산기 (Calculator)
* **기본 연산:** 사칙연산(덧셈, 뺄셈, 곱셈, 나눗셈) 및 괄호 우선순위 계산
* **예외 처리:** 0으로 나누기 오류 처리 및 잘못된 수식 입력 검증
* **기록 조회:** 최근 계산 내역 저장 및 재사용 기능 *(선택사항)*

### 📚 2. 도서 관리 프로그램 (Book Management System)
* **도서 등록/수정/삭제 (CRUD):** ISBN, 제목, 저자, 출판사 정보를 관리
* **도서 검색:** 제목 또는 저자 키워드 기반 빠른 검색
* **대여 및 반납 관리:** 도서 대여 상태 업데이트 및 대여 이력 관리
* **데이터 지속성:** 파일(CSV/JSON) 또는 DB를 통한 데이터 자동 저장

---

## 🛠 기술 스택 (Tech Stack)

* **Language:** Python 3.10+ *(또는 Java, C++ 등)*
* **GUI / Framework:** PyQt5 / Tkinter *(CLI 프로젝트인 경우 'CLI Base'로 변경)*
* **Database / Storage:** SQLite3 / JSON / CSV

---

## 📁 프로젝트 구조 (Project Structure)

```text
├── src/
│   ├── calculator/          # 계산기 모듈
│   │   ├── main.py
│   │   └── utils.py
│   └── book_manager/        # 도서 관리 모듈
│       ├── manager.py
│       └── models.py
├── data/                    # 도서 데이터 저장 폴더
├── tests/                   # 단위 테스트
├── README.md
└── requirements.txt

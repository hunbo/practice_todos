# 데이터베이스와의 연결을 설정하고, 세션을 관리하는 part.
# 세션은 데이터베이스와의 상호작용을 위한 연결 상태를 유지하며, 각 트랜잭션을 관리함.
# 세션의 역할: 세션은 데이터베이스와의 연결을 유지하고, 각 요청마다 독립적인 트랜잭션을 처리함.
# 예를 들어, 데이터를 조회하거나 삽입할 때 세션이 열리고, 트랜잭션이 완료되면 세션이 종료됨.


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker   #ORM 모델을 사용하여 테이블의 구조를 객체로 표현
from sqlalchemy.ext.declarative import declarative_base

#sqplite3 엔진을 정의, DB파일 todo.sqlite3
DB_URL = 'sqlite:///todo.sqlite3'

# 데이터베이스에 연결하는 엔진을 생성하는 함수.
engine = create_engine(DB_URL,connect_args={'check_same_thread': False})

# 데이터베이스와 상호 작용하는 세션을 생성하는 클래스
# 애플리케이션에서 데이터베이스와 상호작용할 때 세션을 사용하여 데이터베이스 트랜잭션(transaction)을 관리함.
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 선언적 모델링을 위한 기본 클래스
Base = declarative_base()  # 이 클래스는 다른 ORM모델을 생성하는 기반이 됨.
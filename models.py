# 애플리케이션에서 사용할 데이터베이스 테이블을 정의하는 part.
# 각 테이블은 하나의 파이썬 클래스로 표현되며, SQLAlchemy ORM을 통해 테이블과 매핑됨.
# 덕분에 sql쿼리를 작성하지 않고도 객체 지향적인 방식으로 데이터베이스에 접근할 수 있게 해줌.


from sqlalchemy import Column, Integer, Boolean, Text
from database import Base


#todos 테이블
class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    task = Column(Text)
    completed = Column(Boolean, default=False)
"""
Подключение к базе данных и создание сессии для работы с ней
"""
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    """
    Принимает на вход адрес базы данных
    """
    global __factory

    if __factory:
        # Проверяет, не создали ли мы уже фабрику подключений
        # (то есть не вызываем ли мы функцию не первый раз).
        # Если уже создали, то завершаем работу, так как начальную
        # инициализацию надо проводить только единожды.
        raise Exception('Типа создали')
        # return

    if not db_file or not db_file.strip():
        # Проверяем, что нам указали не пустой адрес базы данных
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    # Создаём строку подключения conn_str
    # (она состоит из типа базы данных, адреса до базы данных
    # и параметров подключения)
    print(f'Подключение к базе данных по адресу {conn_str}')

    engine = sa.create_engine(conn_str, echo=False)
    # Передаём строку подключения Sqlalchemy для того,
    # чтобы она выбрала правильный движок работы с базой данных
    # (переменная engine)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models
    # Импортируем все созданные модели

    SqlAlchemyBase.metadata.create_all(engine)
    # Создаём все объекты, которых нет в базе данных.
    # Все таблицы, которые были уже созданы в базе данных,
    # останутся без изменений


def create_session() -> Session:
    """Получение сессии подключения к базе данных"""
    global __factory
    return __factory()

from fake_db.database import db

def test_get_user_by_email():
    """Проверка получения пользователя по email"""
    user = db.get_user_by_email('i.i.ivanov@mail.com')
    assert user is not None
    assert user['name'] == 'Ivan Ivanov'

    user = db.get_user_by_email('nonexistent@mail.com')
    assert user is None

def test_create_user():
    """Проверка создания нового пользователя"""
    initial_count = len(db._users)
    db.create_user('Alexey Alexandrov', 'a.a.alexandrov@mail.com')
    assert len(db._users) == initial_count + 1
    new_user = db.get_user_by_email('a.a.alexandrov@mail.com')
    assert new_user is not None
    assert new_user['name'] == 'Alexey Alexandrov'

def test_delete_user_by_email():
    """Проверка удаления пользователя по email"""
    db.delete_user_by_email('i.i.ivanov@mail.com')
    user = db.get_user_by_email('i.i.ivanov@mail.com')
    assert user is None

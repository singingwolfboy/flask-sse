import pytest
from flask_sse import Message


def test_empty_message():
    with pytest.raises(TypeError):
        m = Message()


def test_simple_data():
    m = Message("foo")
    assert m.data == "foo"
    assert m.type == None
    assert m.id == None
    assert m.retry == None

    assert m.to_dict() == {"data": "foo"}
    assert repr(m) == "Message('foo')"
    assert str(m) == 'data:foo\n\n'


def test_data_dict():
    m = Message({"message": "Hello!"})
    assert m.data == {"message": "Hello!"}
    assert m.type == None
    assert m.id == None
    assert m.retry == None

    assert m.to_dict() == {"data": {"message": "Hello!"}}
    assert repr(m) == "Message({'message': 'Hello!'})"
    assert str(m) == 'data:{"message": "Hello!"}\n\n'


def test_multiline_data():
    m = Message("foo\nbar")
    assert m.data == "foo\nbar"
    assert m.type == None
    assert m.id == None
    assert m.retry == None

    assert m.to_dict() == {"data": "foo\nbar"}
    assert repr(m) == "Message('foo\\nbar')"
    assert str(m) == 'data:foo\ndata:bar\n\n'


def test_all_args():
    m = Message("foo", type="example", id=5, retry=500)
    assert m.data == "foo"
    assert m.type == "example"
    assert m.id == 5
    assert m.retry == 500

    assert m.to_dict() == {
        "data": "foo",
        "type": "example",
        "id": 5,
        "retry": 500,
    }
    assert repr(m) == "Message('foo', type='example', id=5, retry=500)"
    assert str(m) == 'event:example\ndata:foo\nid:5\nretry:500\n\n'


def test_equality():
    m1 = Message("abc")
    m2 = Message("abc")
    assert m1 == m2
    m3 = Message("abc", type="example")
    assert m1 != m3
    m4 = Message("def")
    assert m1 != m4

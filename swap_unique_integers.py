import argparse

import sqlalchemy as sa
import sqlalchemy.orm

from sqlalchemy.ext.associationproxy import association_proxy

class Base(sa.orm.DeclarativeBase):
    pass


class Todo(Base):
    "TODO item"
    __tablename__ = 'todo'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    text = sa.Column(sa.Text)
    todolist_objects = sa.orm.relationship(
        'TodoList',
        back_populates = 'todo',
        order_by = 'TodoList.order_key',
    )

    def __str__(self):
        return self.text


class List(Base):
    __tablename__ = 'list'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, unique=True)
    todolist_objects = sa.orm.relationship(
        'TodoList',
        back_populates = 'list',
        order_by = 'TodoList.order_key',
    )

    todos = association_proxy('todolist_objects', 'todo')
    order_keys = association_proxy('todolist_objects', 'order_key')


class TodoList(Base):
    "List of TODO items"
    __tablename__ = 'todo_list'

    list_id = sa.Column(sa.ForeignKey('list.id'), primary_key=True)
    list = sa.orm.relationship(
        'List',
        back_populates = 'todolist_objects',
    )

    todo_id = sa.Column(sa.ForeignKey('todo.id'), primary_key=True)
    todo = sa.orm.relationship(
        'Todo',
        back_populates = 'todolist_objects',
    )

    order_key = sa.Column(sa.Integer)

    __table_args__ = (
        sa.UniqueConstraint(
            'list_id',
            'order_key',
            deferrable = True,
            initially = 'DEFERRED',
        ),
    )

    def __str__(self):
        return f'{self.order_key+1}. {self.todo.text}'


def swap(session, list_name, todo_a_name, todo_b_name):
    todo_a = session.scalars(
        sa.select(TodoList)
        .join(Todo)
        .join(List)
        .where(
            List.name == list_name,
            Todo.name == todo_a_name,
        )
    ).one()
    todo_b = session.scalars(
        sa.select(TodoList)
        .join(Todo)
        .join(List)
        .where(
            List.name == list_name,
            Todo.name == todo_b_name,
        )
    ).one()
    todo_a.order_key, todo_b.order_key = todo_b.order_key, todo_a.order_key

def format_todos(list_, start=1):
    items = zip(list_.todos, list_.order_keys)
    todos = [f'{order_key+start}. {todo.text}' for todo, order_key in items]
    return todos

def format_list(list_):
    return [f'List: {list_.name}'] + format_todos(list_)

def run():
    uri = sa.engine.URL.create(
        database = 'swap_unique_integers',
        drivername = 'postgresql+psycopg',
    )
    engine = sa.create_engine(uri)
    Base.metadata.create_all(engine)
    with sa.orm.Session(engine) as session:
        todos = {
            'mow': Todo(name='mow', text='Mow lawn'),
            'roof': Todo(name='roof', text='Fix roof'),
            'laundry': Todo(name='laundry', text='Wash laundry'),
            'sweep': Todo(name='sweep', text='Sweep floor'),
            'vacuum': Todo(name='vacuum', text='Vacuum carpet'),
            'glass': Todo(name='glass', text='Clean glass'),
            'trees': Todo(name='trees', text='Plant trees'),
            'dig': Todo(name='dig', text='Dig hole'),
        }

        lists = [
            List(
                name = 'outdoor',
                todolist_objects = [
                    TodoList(todo=todos['mow'], order_key=3),
                    TodoList(todo=todos['roof'], order_key=1),
                    TodoList(todo=todos['glass'], order_key=0),
                    TodoList(todo=todos['trees'], order_key=2),
                    TodoList(todo=todos['dig'], order_key=4),
                ],
            ),
            List(
                name = 'indoor',
                todolist_objects = [
                    TodoList(todo=todos['laundry'], order_key=3),
                    TodoList(todo=todos['sweep'], order_key=1),
                    TodoList(todo=todos['vacuum'], order_key=0),
                    TodoList(todo=todos['glass'], order_key=2),
                ],
            ),
        ]

        session.add_all(todos.values())
        session.add_all(lists)

        session.commit()

        lists = session.scalars(sa.select(List))
        print('\n\n'.join(map('\n'.join, map(format_list, lists))))

        print('\n== swap mow and dig ==')
        print('== swap laundry and glass ==\n')
        swap(session, 'indoor', 'laundry', 'glass')

        session.commit()
        lists = session.scalars(sa.select(List))
        print('\n\n'.join(map('\n'.join, map(format_list, lists))))

def main(argv=None):
    """
    Use deferrable constraints to allow swapping the ordered position of
    objects with an association object.
    """
    # - sql deferred deferrable
    # - https://emmer.dev/blog/deferrable-constraints-in-postgresql/
    # - sqlite does not support this:
    #   https://stackoverflow.com/a/43274469/2680592
    parser = argparse.ArgumentParser(
        description = main.__doc__,
    )
    args = parser.parse_args(argv)
    run()

if __name__ == '__main__':
    main()

import argparse

from enum import Enum
from enum import auto
from operator import attrgetter

class Behavior(Enum):
    UNSPECIFIED = auto()
    NULLS_DISTINCT = auto()
    NOT_DISTINCT = auto()


Behavior.UNSPECIFIED.sql = ''
Behavior.NULLS_DISTINCT.sql = 'NULLS DISTINCT'
Behavior.NOT_DISTINCT.sql = 'NULLS NOT DISTINCT'


def create_table(behavior):
    sql = 'CREATE TABLE t1 (a int, b int, c int,'
    constraint = ['UNIQUE', behavior.sql, '(a, b, c)']
    sql += ' '.join(constraint)
    sql += ');'
    return sql

def insert(n=2):
    return n * 'INSERT INTO t1 VALUES (1, NULL, NULL);'

def main(argv=None):
    """
    Generate SQL to stdout to produce the SQL for investigating unique distinct nulls.
    """
    parser = argparse.ArgumentParser(
        description = main.__doc__,
    )
    behavior_choices = list(map(str, map(attrgetter('value'), Behavior)))
    behavior_help = ', '.join((
        f'{member.value}: Default nothing' if not member.sql else
        f'{member.value} {member.sql}'
        for member in Behavior
    ))
    parser.add_argument(
        '--behavior',
        choices = behavior_choices,
        default = '1',
        help = behavior_help,
    )
    args = parser.parse_args(argv)
    behavior = Behavior(int(args.behavior))
    sql = create_table(behavior) + insert()
    print(sql, end='')
    return

    # NOTES
    # https://peter.eisentraut.org/blog/2023/04/04/sql-2023-is-finished-here-is-whats-new#unique-null-treatment-f292
    # psql 15.3
    # - just UNIQUE allows inserting multiple nulls--nulls are distinct per row.
    # - NULLS DISTINCT means no violation
    # - NULLS NOT DISTINCT throws violation

if __name__ == '__main__':
    main()

from contextlib import closing

from click import command, option
from cymysql import connect
from cymysql.cursors import DictCursor
from terminaltables import AsciiTable


@command()
@option('--host', default='127.0.0.1', help='Host')
@option('--port', default='3306', help='Port')
@option('--user', default='root', help='User')
@option('--password', default='root', help='Password')
@option('--database', default='', help='Database')
@option('--table', default='', help='Table')
def process(host, port, user, password, database, table):
    connection = connect(host=host, user=user, passwd=password, db=database, charset='utf8', cursorclass=DictCursor)
    with closing(connection) as connection:
        rows = []
        cursor = connection.cursor()
        with closing(cursor) as cursor:
            cursor.execute('SHOW TABLES')
            rows = cursor.fetchall()

        tables = []
        for row in rows:
            values = row.values()
            values = list(values)
            value = values[0]
            if not table or table == value:
                tables.append(value)

        tables = sorted(tables)

        tables_and_counts = []
        for table in tables:
            count = 0
            cursor = connection.cursor()
            with closing(cursor) as cursor:
                query = 'SELECT COUNT(*) AS count FROM {table:s}'.format(table=table)
                cursor.execute(query)
                row = cursor.fetchone()
                count = row['count']
            if not count:
                continue
            tables_and_counts.append([table, count])

        ascii_table = AsciiTable([['Table', 'COUNT(*)']] + tables_and_counts)
        ascii_table.justify_columns[1] = 'right'
        print(ascii_table.table)

        tables = []
        for table, _ in tables_and_counts:
            description = []
            rows = []
            cursor = connection.cursor()
            with closing(cursor) as cursor:
                query = 'SELECT * FROM {table:s}'.format(table=table)
                cursor.execute(query)
                description = cursor.description
                rows = cursor.fetchall()
            ascii_table = []
            if description:
                description = [d[0] for d in description]
                ascii_table.append(description)
            for row in rows:
                values = list(row.values())
                for index, _ in enumerate(values):
                    if isinstance(values[index], bytes):
                        try:
                            values[index] = values[index].decode('utf-8')
                        except UnicodeDecodeError:
                            values[index] = 'UnicodeDecodeError'
                ascii_table.append(values)
            tables.append((table, ascii_table))

        for name, ascii_table in tables:
            print('')
            print(name)
            print('')
            ascii_table = AsciiTable(ascii_table)
            print(ascii_table.table)


if __name__ == '__main__':
    process()

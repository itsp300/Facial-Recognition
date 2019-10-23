import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    print("Creating a connection to database")
    conn = None
    try:
        print("Connection Created!")
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "faceStudent.db"

    sql_create_attendance_table = """ CREATE TABLE IF NOT EXISTS attendance (
                                        attendance_id text PRIMARY KEY,
                                        report_id text NOT NULL,
                                        student_number text NOT NULL,
                                        confidence text NOT NULL,
                                        date_attended text NOT NULL
                                    ); """

    sql_create_report_table = """ CREATE TABLE IF NOT EXISTS report (
                                            report_id text PRIMARY KEY,
                                            identified blob NOT NULL,
                                            date_attended text NOT NULL 
                                        ); """

    sql_create_student_table = """ CREATE TABLE IF NOT EXISTS students (
                                            student_number text PRIMARY KEY,
                                            encoded_image text NOT NULL
                                        ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create attendance table
        create_table(conn, sql_create_attendance_table)

        # create report table
        create_table(conn, sql_create_report_table)

        # create student table
        create_table(conn, sql_create_student_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
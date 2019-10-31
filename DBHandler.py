import Database


def main():
    database = "faceStudent.db"

    sql_create_attendance_table = """ CREATE TABLE IF NOT EXISTS attendance (
                                        attendance_id text PRIMARY KEY,
                                        report_id text NOT NULL,
                                        student_number text NOT NULL,
                                        confidence text NOT NULL,
                                        date_attended text NOT NULL
                                    ); """

    sql_create_student_table = """ CREATE TABLE IF NOT EXISTS students (
                                            student_number text PRIMARY KEY,
                                            first_name text NOT NULL,
                                            surname text NOT NULL,
                                            file_name text NOT NULL
                                        ); """

    # create a database connection
    conn = Database.create_connection(database)

    # create tables
    if conn is not None:
        # create attendance table
        Database.create_table(conn, sql_create_attendance_table)

        # create student table
        Database.create_table(conn, sql_create_student_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()

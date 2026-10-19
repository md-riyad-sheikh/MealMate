from django.core.management.base import BaseCommand

from django.db import connection


MYSQL_SQL = [

    """
    CREATE TABLE IF NOT EXISTS users (

        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

        full_name VARCHAR(150) NOT NULL,

        email VARCHAR(255) NOT NULL UNIQUE,

        password_hash VARCHAR(255) NOT NULL,

        role VARCHAR(30) NOT NULL DEFAULT 'user',

        phone VARCHAR(30) DEFAULT NULL,

        is_active TINYINT(1) NOT NULL DEFAULT 1,

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        INDEX idx_users_role (role)

    ) ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci
    """,


    """
    CREATE TABLE IF NOT EXISTS food_posts (

        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

        business_id INT UNSIGNED NOT NULL,

        food_name VARCHAR(150) NOT NULL,

        description TEXT DEFAULT NULL,

        quantity INT UNSIGNED NOT NULL DEFAULT 1,

        pickup_address VARCHAR(255) NOT NULL,

        pickup_start DATETIME NOT NULL,

        pickup_end DATETIME NOT NULL,

        status VARCHAR(30) NOT NULL DEFAULT 'available',

        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        INDEX idx_food_business (business_id),

        INDEX idx_food_status_pickup (
            status,
            pickup_end
        ),

        CONSTRAINT fk_food_business
            FOREIGN KEY (business_id)
            REFERENCES users(id)
            ON DELETE CASCADE

    ) ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci
    """,


    """
    CREATE TABLE IF NOT EXISTS reservations (

        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

        user_id INT UNSIGNED NOT NULL,

        food_post_id INT UNSIGNED NOT NULL,

        status VARCHAR(30) NOT NULL DEFAULT 'reserved',

        pickup_code VARCHAR(20) DEFAULT NULL,

        reserved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        updated_at TIMESTAMP NOT NULL
            DEFAULT CURRENT_TIMESTAMP
            ON UPDATE CURRENT_TIMESTAMP,

        collected_at DATETIME DEFAULT NULL,

        UNIQUE KEY uq_reservation_pickup_code (
            pickup_code
        ),

        INDEX idx_reservation_user (
            user_id
        ),

        INDEX idx_reservation_food (
            food_post_id
        ),

        INDEX idx_reservation_status (
            status
        ),

        CONSTRAINT fk_reservation_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,

        CONSTRAINT fk_reservation_food
            FOREIGN KEY (food_post_id)
            REFERENCES food_posts(id)
            ON DELETE CASCADE

    ) ENGINE=InnoDB
    DEFAULT CHARSET=utf8mb4
    COLLATE=utf8mb4_unicode_ci
    """,
]


SQLITE_SQL = [

    """
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name VARCHAR(150) NOT NULL,

        email VARCHAR(255) NOT NULL UNIQUE,

        password_hash VARCHAR(255) NOT NULL,

        role VARCHAR(30) NOT NULL DEFAULT 'user',

        phone VARCHAR(30),

        is_active INTEGER NOT NULL DEFAULT 1,

        created_at DATETIME NOT NULL
            DEFAULT CURRENT_TIMESTAMP

    )
    """,


    """
    CREATE TABLE IF NOT EXISTS food_posts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        business_id INTEGER NOT NULL,

        food_name VARCHAR(150) NOT NULL,

        description TEXT,

        quantity INTEGER NOT NULL DEFAULT 1,

        pickup_address VARCHAR(255) NOT NULL,

        pickup_start DATETIME NOT NULL,

        pickup_end DATETIME NOT NULL,

        status VARCHAR(30) NOT NULL DEFAULT 'available',

        created_at DATETIME NOT NULL
            DEFAULT CURRENT_TIMESTAMP

    )
    """,


    """
    CREATE TABLE IF NOT EXISTS reservations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        food_post_id INTEGER NOT NULL,

        status VARCHAR(30) NOT NULL DEFAULT 'reserved',

        pickup_code VARCHAR(20) UNIQUE,

        reserved_at DATETIME NOT NULL
            DEFAULT CURRENT_TIMESTAMP,

        updated_at DATETIME NOT NULL
            DEFAULT CURRENT_TIMESTAMP,

        collected_at DATETIME

    )
    """,
]


class Command(BaseCommand):

    help = (
        "Creates and updates the MealMate "
        "application database tables."
    )


    def mysql_column_exists(
        self,
        cursor,
        table,
        column
    ):

        cursor.execute(
            f"""
            SHOW COLUMNS
            FROM `{table}`
            LIKE %s
            """,
            [column]
        )

        return cursor.fetchone() is not None


    def mysql_index_exists(
        self,
        cursor,
        table,
        index_name
    ):

        cursor.execute(
            f"""
            SHOW INDEX
            FROM `{table}`
            WHERE Key_name = %s
            """,
            [index_name]
        )

        return cursor.fetchone() is not None


    def sqlite_column_exists(
        self,
        cursor,
        table,
        column
    ):

        cursor.execute(
            f"PRAGMA table_info({table})"
        )

        columns = {
            row[1]
            for row in cursor.fetchall()
        }

        return column in columns


    def update_mysql_reservations(
        self,
        cursor
    ):

        if not self.mysql_column_exists(
            cursor,
            "reservations",
            "pickup_code"
        ):

            cursor.execute(
                """
                ALTER TABLE reservations

                ADD COLUMN pickup_code
                VARCHAR(20)
                NULL
                AFTER status
                """
            )

            self.stdout.write(
                "Added reservations.pickup_code"
            )


        if not self.mysql_column_exists(
            cursor,
            "reservations",
            "collected_at"
        ):

            cursor.execute(
                """
                ALTER TABLE reservations

                ADD COLUMN collected_at
                DATETIME
                NULL
                AFTER updated_at
                """
            )

            self.stdout.write(
                "Added reservations.collected_at"
            )


        if not self.mysql_index_exists(
            cursor,
            "reservations",
            "uq_reservation_pickup_code"
        ):

            cursor.execute(
                """
                ALTER TABLE reservations

                ADD UNIQUE INDEX
                uq_reservation_pickup_code
                (pickup_code)
                """
            )

            self.stdout.write(
                "Added unique pickup code index"
            )


    def update_sqlite_reservations(
        self,
        cursor
    ):

        if not self.sqlite_column_exists(
            cursor,
            "reservations",
            "pickup_code"
        ):

            cursor.execute(
                """
                ALTER TABLE reservations

                ADD COLUMN pickup_code
                VARCHAR(20)
                NULL
                """
            )


        if not self.sqlite_column_exists(
            cursor,
            "reservations",
            "collected_at"
        ):

            cursor.execute(
                """
                ALTER TABLE reservations

                ADD COLUMN collected_at
                DATETIME
                NULL
                """
            )


        cursor.execute(
            """
            CREATE UNIQUE INDEX
            IF NOT EXISTS
            uq_reservation_pickup_code

            ON reservations (
                pickup_code
            )
            """
        )


    def handle(
        self,
        *args,
        **options
    ):

        statements = (

            SQLITE_SQL

            if connection.vendor == "sqlite"

            else MYSQL_SQL
        )


        with connection.cursor() as cursor:


            for statement in statements:

                cursor.execute(
                    statement
                )


            if connection.vendor == "mysql":

                self.update_mysql_reservations(
                    cursor
                )


            elif connection.vendor == "sqlite":

                self.update_sqlite_reservations(
                    cursor
                )


        self.stdout.write(

            self.style.SUCCESS(
                "MealMate application tables are ready."
            )
        )
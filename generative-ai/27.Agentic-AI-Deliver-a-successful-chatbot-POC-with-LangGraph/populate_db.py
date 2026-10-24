import sqlite3


def populate_spending_events():
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS spending_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            plan_name TEXT NOT NULL,
            billing_start DATE NOT NULL,
            billing_end DATE NOT NULL,
            amount_due REAL
        )
        """
    )

    spending_events = [
        (1, "Standard Plan", "2024-01-01", "2024-01-31", 50.00),
        (1, "Standard Plan", "2024-02-01", "2024-02-29", 55.00),
        (1, "Standard Plan", "2024-03-01", "2024-03-31", 53.00),
        (1, "Standard Plan", "2024-04-01", "2024-04-30", 52.00),
        (1, "Standard Plan", "2024-05-01", "2024-05-31", 54.00),
        (1, "Standard Plan", "2024-06-01", "2024-06-30", 56.00),
        (1, "Eco Plan", "2024-07-01", "2024-07-31", 58.00),
        (1, "Eco Plan", "2024-08-01", "2024-08-31", 57.00),
        (1, "Eco Plan", "2024-09-01", "2024-09-30", 59.00),
        (1, "Standard Plan", "2024-10-01", "2024-10-31", 60.00),
        (1, "Standard Plan", "2024-11-01", "2024-11-30", 62.00),
        (1, "Standard Plan", "2024-12-01", "2024-12-31", 63.00),
    ]

    cursor.executemany(
        """
        INSERT INTO spending_events (
            customer_id,
            plan_name,
            billing_start,
            billing_end,
            amount_due
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        spending_events,
    )

    conn.commit()
    conn.close()


def populate_electricity_plans():
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS electricity_plans (
            plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_name TEXT NOT NULL,
            plan_description TEXT NOT NULL,
            selling_points TEXT NOT NULL
        )
        """
    )

    electricity_plans = [
        (
            1,
            "Standard Plan",
            "A well-rounded electricity plan designed for typical households, offering stable pricing and reliable service without any peak-hour surcharges.",
            "Affordable rates, predictable billing, ideal for families",
        ),
        (
            2,
            "Eco Plan",
            "A renewable energy plan that prioritizes sustainability by sourcing electricity from solar, wind, and hydroelectric power. Perfect for environmentally conscious consumers.",
            "100% green energy, reduces carbon footprint, government incentives may apply",
        ),
        (
            3,
            "Night Plan",
            "An electricity plan that provides significant cost savings for customers who consume most of their energy during off-peak nighttime hours. Ideal for night-shift workers and EV owners.",
            "Lower rates at night, great for electric vehicle charging, smart meter integration",
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO electricity_plans (
            plan_id,
            plan_name,
            plan_description,
            selling_points
        )
        VALUES (?, ?, ?, ?)
        """,
        electricity_plans,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    populate_spending_events()
    populate_electricity_plans()
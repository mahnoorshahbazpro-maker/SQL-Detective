
import sqlite3
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SQL Detective",
    page_icon="🕵️",
    layout="wide"
)

# -----------------------------
# DEMO DATABASE
# -----------------------------
def create_demo_database():
    conn = sqlite3.connect(":memory:")

    conn.executescript("""
    CREATE TABLE Customers (
        CustomerID INTEGER PRIMARY KEY,
        CustomerName TEXT,
        City TEXT,
        Age INTEGER,
        Gender TEXT
    );

    CREATE TABLE Products (
        ProductID INTEGER PRIMARY KEY,
        ProductName TEXT,
        Category TEXT,
        UnitPrice REAL
    );

    CREATE TABLE Orders (
        OrderID INTEGER PRIMARY KEY,
        CustomerID INTEGER,
        ProductID INTEGER,
        Quantity INTEGER
    );
    """)

    customers = [
        (1, "Ali Khan", "Lahore", 25, "Male"),
        (2, "Sara Ahmed", "Karachi", 24, "Female"),
        (3, "Ahmed Raza", "Islamabad", 29, "Male"),
        (4, "Ayesha Noor", "Lahore", 22, "Female"),
        (5, "Bilal Hussain", "Faisalabad", 27, "Male")
    ]

    products = [
        (1, "Laptop", "Electronics", 100000),
        (2, "Phone", "Electronics", 50000),
        (3, "Chair", "Furniture", 15000),
        (4, "Bottle", "Accessories", 500),
        (5, "Mouse", "Accessories", 1000),
        (6, "Desk", "Furniture", 20000)
    ]

    orders = [
        (1, 1, 1, 3),
        (2, 1, 2, 2),
        (3, 1, 5, 2),
        (4, 1, 3, 1),
        (5, 2, 1, 1),
        (6, 2, 2, 2),
        (7, 2, 4, 2),
        (8, 3, 2, 1),
        (9, 3, 6, 2),
        (10, 4, 1, 2),
        (11, 4, 3, 3),
        (12, 5, 6, 1),
        (13, 5, 4, 1),
        (14, 1, 1, 2)
    ]

    conn.executemany(
        "INSERT INTO Customers VALUES (?, ?, ?, ?, ?)",
        customers
    )
    conn.executemany(
        "INSERT INTO Products VALUES (?, ?, ?, ?)",
        products
    )
    conn.executemany(
        "INSERT INTO Orders VALUES (?, ?, ?, ?)",
        orders
    )
    conn.commit()
    return conn


# -----------------------------
# SESSION STATE
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "mission" not in st.session_state:
    st.session_state.mission = 1

if "solved" not in st.session_state:
    st.session_state.solved = False

# Demo database is recreated on each rerun.
# It contains sample data and needs no MySQL server.
conn = create_demo_database()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("🗄️ Detective Database")
st.sidebar.success("DEMO MODE: Connected")
st.sidebar.caption(
    "Explore the sample e-commerce database using SQL."
)

if st.sidebar.button("🔄 Restart Investigation"):
    st.session_state.score = 0
    st.session_state.mission = 1
    st.session_state.solved = False
    st.rerun()

# -----------------------------
# HEADER
# -----------------------------
st.title("🕵️ SQL DETECTIVE")
st.subheader("A Sales Mystery Has Occurred...")

st.write(
    "Investigate a fictional e-commerce company, "
    "write SQL queries, and uncover four hidden clues."
)

st.info(
    "This is a demo database with sample data. "
    "No external MySQL connection is required."
)

# -----------------------------
# SCOREBOARD
# -----------------------------
c1, c2, c3 = st.columns(3)

c1.metric("🏆 Detective Score", f"{st.session_state.score}/100")
c2.metric("🎯 Current Mission", f"{min(st.session_state.mission, 4)}/4")
c3.metric(
    "🔎 Status",
    "CASE CLOSED" if st.session_state.score == 100
    else "INVESTIGATING"
)

st.progress(st.session_state.score / 100)
st.divider()

# -----------------------------
# CASE FILE
# -----------------------------
st.markdown("## 🚨 CASE FILE #001")
st.write(
    "A fictional e-commerce company has reported unusual sales. "
    "Use SQL to examine the evidence and solve each mission."
)

st.markdown("## 🎯 Investigation Missions")

missions = [
    "🔎 Mission 1 — The Revenue King: Find the product with the highest revenue.",
    "🏙️ Mission 2 — The Winning City: Find the city with the highest revenue.",
    "📦 Mission 3 — The Weakest Category: Find the category with the lowest revenue.",
    "👤 Mission 4 — The Power Customer: Find the customer with the most orders."
]

for i, mission_text in enumerate(missions, start=1):
    if i < st.session_state.mission:
        st.success(f"✅ {mission_text}")
    elif i == st.session_state.mission and st.session_state.mission <= 4:
        st.warning(f"👉 CURRENT: {mission_text}")
    else:
        st.write(mission_text)

st.divider()

# -----------------------------
# DATABASE EVIDENCE
# -----------------------------
st.markdown("## 🗄️ DATABASE EVIDENCE")

with st.expander("View Customers table"):
    st.dataframe(
        pd.read_sql_query("SELECT * FROM Customers", conn),
        use_container_width=True
    )

with st.expander("View Products table"):
    st.dataframe(
        pd.read_sql_query("SELECT * FROM Products", conn),
        use_container_width=True
    )

with st.expander("View Orders table"):
    st.dataframe(
        pd.read_sql_query("SELECT * FROM Orders", conn),
        use_container_width=True
    )

st.caption(
    "Relationships: Orders.CustomerID → Customers.CustomerID | "
    "Orders.ProductID → Products.ProductID"
)

st.divider()

# -----------------------------
# SQL CONSOLE
# -----------------------------
st.markdown("## 🕵️ Current Investigation")

if st.session_state.mission <= 4:
    st.subheader(missions[st.session_state.mission - 1])
else:
    st.success("🏆 CASE CLOSED — All four missions solved!")

examples = {
    1: """SELECT p.ProductName,
       SUM(o.Quantity * p.UnitPrice) AS TotalRevenue
FROM Orders o
JOIN Products p ON o.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY TotalRevenue DESC
LIMIT 1;""",
    2: """SELECT c.City,
       SUM(o.Quantity * p.UnitPrice) AS TotalRevenue
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN Products p ON o.ProductID = p.ProductID
GROUP BY c.City
ORDER BY TotalRevenue DESC
LIMIT 1;""",
    3: """SELECT p.Category,
       SUM(o.Quantity * p.UnitPrice) AS TotalRevenue
FROM Products p
JOIN Orders o ON p.ProductID = o.ProductID
GROUP BY p.Category
ORDER BY TotalRevenue ASC
LIMIT 1;""",
    4: """SELECT c.CustomerName,
       COUNT(o.OrderID) AS OrderCount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
GROUP BY c.CustomerID, c.CustomerName
ORDER BY OrderCount DESC
LIMIT 1;"""
}

if st.session_state.mission <= 4:
    if "sql_input" not in st.session_state:
        st.session_state.sql_input = ""

    if st.button("📋 Load Example Query"):
        st.session_state.sql_input = examples[st.session_state.mission]
        st.rerun()

    query = st.text_area(
        "Write your SQL investigation:",
        key="sql_input",
        height=190,
        placeholder="SELECT ... FROM ... JOIN ..."
    )

    if st.button("▶ RUN INVESTIGATION", type="primary"):
        if not query.strip():
            st.warning("Write a SQL query first.")
        else:
            try:
                result = pd.read_sql_query(query, conn)
                st.success("🔍 Investigation complete!")
                st.markdown("### 📋 Evidence Found")
                st.dataframe(result, use_container_width=True)

                if result.empty or len(result.columns) == 0:
                    st.info("No evidence returned. Try another query.")
                else:
                    answer = str(result.iloc[0, 0]).strip().lower()

                    expected = {
                        1: "laptop",
                        2: "lahore",
                        3: "accessories",
                        4: "ali khan"
                    }

                    if answer == expected[st.session_state.mission]:
                        st.session_state.score += 25
                        solved_mission = st.session_state.mission
                        st.session_state.mission += 1
                        st.session_state.solved = True

                        st.success(
                            f"🎉 Mission {solved_mission} solved! +25 points!"
                        )

                        if st.session_state.mission == 5:
                            st.balloons()
                            st.markdown("## 🏆 CASE CLOSED")
                            st.write(
                                "You solved all four missions! "
                                "Final Detective Score: 100/100"
                            )

                        st.rerun()
                    else:
                        st.session_state.solved = False
                        st.info(
                            "🧐 Interesting evidence, Detective. "
                            "Check your result and keep investigating."
                        )

            except Exception as e:
                st.error("❌ SQL Error")
                st.code(str(e))

    st.markdown("### 💡 Detective Hint")
    hints = {
        1: "Join Orders with Products and calculate Quantity × UnitPrice.",
        2: "Join Customers, Orders and Products. Group revenue by City.",
        3: "Group revenue by Category and sort from lowest to highest.",
        4: "Group orders by customer and count OrderID."
    }
    st.caption(hints[st.session_state.mission])

st.divider()
st.caption("SQL Detective | Python • SQL • Pandas • Streamlit | Demo Mode")

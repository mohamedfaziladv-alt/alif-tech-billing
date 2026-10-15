# -*- coding: utf-8 -*-
"""
ALIF TECH - Online Enterprise Billing & Financial Management System
Streamlit Cloud Edition (With Member Role, Daily Status & User Management)
"""

import streamlit as st
import sqlite3
import datetime
import hashlib
import html
import streamlit.components.v1 as components
import pandas as pd

DB_FILE = "alif_tech_data.db"

# Page Configuration
st.set_page_config(
    page_title="ALIF TECH — Billing & Financial Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 100% Pre-loaded Embedded Data (Exactly 12 Unique Capital Rows)
DEFAULT_CAPITAL = [
    (1, "KYOCERA", "1", 87000.0),
    (2, "HP SMART TANK", "1", 17000.0),
    (3, "TABLE", "2", 9000.0),
    (4, "ADVANCE", "1", 15000.0),
    (5, "TRAVEL", "-", 8400.0),
    (6, "INTERNET", "1 YEAR", 5000.0),
    (7, "CCTV", "1", 2150.0),
    (8, "ELECTRICIAN", "-", 3202.0),
    (9, "MONITOR, CPU,SPIRAL,LAMINATOR,CARD CUTTER", "-", 29000.0),
    (10, "BANNER", "-", 6490.0),
    (11, "REGINET LICENSE", "-", 2000.0),
    (12, "PURCHASED", "DYNAMIC STOCK", 8047.0)
]

DEFAULT_PURCHASES = [
    (1, "65*95 x 250b gold", "06.10.2026", 140.0, 1.0, 140.0),
    (2, "65*95 x 175 JMD", "06.10.2026", 120.0, 1.0, 120.0),
    (3, "100*230 FOP FUL AAD", "06.10.2026", 180.0, 1.0, 180.0),
    (4, "BINDINGTAPE 15 MTR", "06.10.2026", 60.0, 1.0, 60.0),
    (5, "180 GSM PHOTO SHEET", "06.10.2026", 140.0, 1.0, 140.0),
    (6, "STUL FOTO 20 SHEET", "06.10.2026", 150.0, 1.0, 150.0),
    (7, "SPIRAL SHEET", "06.10.2026", 160.0, 3.0, 480.0),
    (8, "KANGARO DS-23S24L", "06.10.2026", 1750.0, 1.0, 1750.0),
    (9, "TNPL FS 70 GSM", "06.10.2026", 270.0, 1.0, 270.0),
    (10, "A4 LAMI  SHEET BLACK", "06.10.2026", 420.0, 1.0, 420.0),
    (11, "TNPL A4 70GSM", "06.10.2026", 2050.0, 1.0, 2050.0),
    (12, "A4 90 GSM GREEN", "06.10.2026", 330.0, 1.0, 330.0),
    (13, "SPIRAL RING FFP/FIP", "06.10.2026", 140.0, 2.0, 280.0),
    (14, "NOVA PLUS FOTO SHIT", "06.10.2026", 150.0, 2.0, 300.0),
    (15, "STYLISH X3 BLUE 7/-", "06.10.2026", 20.0, 2.0, 40.0),
    (16, "FEVISTICK MRP 40/-", "06.10.2026", 34.0, 1.0, 34.0),
    (17, "YELLOW HI LIGHATER", "06.10.2026", 15.0, 1.0, 15.0),
    (18, "CT-512BK (ON/OFF)", "06.10.2026", 110.0, 1.0, 110.0),
    (19, "MASTER 30 CM", "06.10.2026", 30.0, 1.0, 30.0),
    (20, "PREMIER SHEET 10/-", "06.10.2026", 8.0, 1.0, 8.0),
    (21, "009 STHUL:", "06.10.2026", 50.0, 1.0, 50.0),
    (22, "1Q FS AC NOT (NP)", "06.10.2026", 70.0, 1.0, 70.0),
    (23, "BINDING TAPE 30 MTR", "15.10.2026", 140.0, 2.0, 280.0),
    (24, "180 GSM PHOTO SHEET", "15.10.2026", 140.0, 2.0, 280.0),
    (25, "SPIRAL RING FFP/FIP", "15.10.2026", 140.0, 1.0, 140.0),
    (26, "COURIER CHARGE + PACKING", "15.10.2026", 220.0, 1.0, 220.0),
    (27, "180 gsM PHOTO SHEET", "15.10.2026", 100.0, 1.0, 100.0)
]

DEFAULT_SALES = [
    (1, "PRINTOUT", "09.10.2026", 0.0, 10.0, 10.0, "INV-001"),
    (2, "PRINT", "09.10.2026", 150.0, 0.0, 150.0, "INV-002"),
    (3, "VOTER PRINT  + LAMINATION", "11.10.2026", 60.0, 0.0, 60.0, "INV-003"),
    (4, "PASSPORTSIZE PHOTO 8+4", "11.10.2026", 110.0, 0.0, 110.0, "INV-004"),
    (5, "XEROX", "11.10.2026", 30.0, 60.0, 90.0, "INV-005"),
    (6, "SPIRAL", "11.10.2026", 360.0, 220.0, 580.0, "INV-006"),
    (7, "PRINT", "11.10.2026", 0.0, 50.0, 50.0, "INV-007"),
    (8, "PRINT", "12.10.2026", 80.0, 5.0, 85.0, "INV-008"),
    (9, "XEROX", "12.10.2026", 20.0, 0.0, 20.0, "INV-009"),
    (10, "PASSPORTSIZE PHOTO", "12.10.2026", 40.0, 0.0, 40.0, "INV-010"),
    (11, "SPIRAL", "13.10.2026", 270.0, 270.0, 540.0, "INV-011"),
    (12, "RATION CARD NAME CHANGE", "13.10.2026", 100.0, 0.0, 100.0, "INV-012"),
    (13, "PRINTOUT", "13.10.2026", 0.0, 80.0, 80.0, "INV-013"),
    (14, "MONEY TRANSFER (650)", "13.10.2026", 20.0, 0.0, 20.0, "INV-014"),
    (15, "SPIRAL", "14.10.2026", 210.0, 890.0, 1100.0, "INV-015"),
    (16, "XEROX", "14.10.2026", 4.0, 0.0, 4.0, "INV-016"),
    (17, "SPIRAL", "15.10.2026", 820.0, 385.0, 1205.0, "INV-017")
]

def hash_pw(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_database():
    conn = get_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")

    # Migrate any existing 'Staff' roles to 'Member'
    c.execute("UPDATE users SET role = 'Member' WHERE role = 'Staff'")
    conn.commit()

    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        dt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        c.execute("INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
                  ("owner", hash_pw("owner123"), "Owner", dt))
        c.execute("INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
                  ("member", hash_pw("member123"), "Member", dt))

    c.execute("""CREATE TABLE IF NOT EXISTS capital_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, sno INTEGER, purpose TEXT, quantity TEXT, amount REAL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT, sno INTEGER, item TEXT, date TEXT, rate REAL, quantity REAL, amount REAL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT, sno INTEGER, item TEXT, date TEXT, cash REAL DEFAULT 0, gpay REAL DEFAULT 0, amount REAL, invoice_no TEXT)""")
    conn.commit()

    # Seed capital if empty
    c.execute("SELECT COUNT(*) FROM capital_expenses")
    if c.fetchone()[0] == 0:
        for r in DEFAULT_CAPITAL:
            c.execute("INSERT INTO capital_expenses (sno, purpose, quantity, amount) VALUES (?, ?, ?, ?)", r)
    else:
        # Automatic Deduplication: Remove any duplicate rows keeping only unique S.No
        c.execute("""
            DELETE FROM capital_expenses 
            WHERE id NOT IN (
                SELECT MIN(id) FROM capital_expenses GROUP BY sno
            )
        """)
        conn.commit()

    c.execute("SELECT COUNT(*) FROM purchases")
    if c.fetchone()[0] == 0:
        for r in DEFAULT_PURCHASES:
            c.execute("INSERT INTO purchases (sno, item, date, rate, quantity, amount) VALUES (?, ?, ?, ?, ?, ?)", r)

    c.execute("SELECT COUNT(*) FROM sales")
    if c.fetchone()[0] == 0:
        for r in DEFAULT_SALES:
            c.execute("INSERT INTO sales (sno, item, date, cash, gpay, amount, invoice_no) VALUES (?, ?, ?, ?, ?, ?, ?)", r)

    conn.commit()
    conn.close()

init_database()

# Session State for Authentication & POS
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if "pos_cart" not in st.session_state:
    st.session_state.pos_cart = []

# --- 1. CLEAN LOGIN GATEWAY (NO REGISTER BUTTON HERE) ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #0284C7;'>⚡ ALIF TECH — Online Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Enterprise Billing & Financial Management System</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("### 🔑 Sign In")
        username_inp = st.text_input("Username")
        password_inp = st.text_input("Password", type="password")

        if st.button("🚀 Sign In", use_container_width=True, type="primary"):
            if username_inp and password_inp:
                conn = get_db()
                cur = conn.cursor()
                cur.execute("SELECT username, role FROM users WHERE username = ? AND password_hash = ?",
                            (username_inp.strip(), hash_pw(password_inp.strip())))
                user = cur.fetchone()
                conn.close()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user[0]
                    st.session_state.role = user[1]
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                st.warning("Please enter your credentials.")

# --- 2. AUTHENTICATED SYSTEM DASHBOARD ---
else:
    today_date = datetime.date.today().strftime("%d.%m.%Y")
    now_time = datetime.datetime.now().strftime("%H:%M:%S")

    st.sidebar.markdown(f"### 👤 {st.session_state.username}")
    st.sidebar.markdown(f"**Role:** `{st.session_state.role}`")
    st.sidebar.markdown(f"**Date:** `{today_date}`")
    st.sidebar.markdown(f"**Time:** `{now_time}`")

    if st.sidebar.button("🚪 Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.pos_cart = []
        st.rerun()

    conn = get_db()

    # Ensure Deduplication in Capital Expenses
    conn.execute("""
        DELETE FROM capital_expenses 
        WHERE id NOT IN (
            SELECT MIN(id) FROM capital_expenses GROUP BY sno
        )
    """)
    conn.commit()

    sales_df = pd.read_sql("SELECT sno, item, date, cash, gpay, amount, invoice_no FROM sales ORDER BY sno ASC", conn)
    purch_df = pd.read_sql("SELECT sno, item, date, rate, quantity, amount FROM purchases ORDER BY sno ASC", conn)
    cap_df = pd.read_sql("SELECT sno, purpose, quantity, amount FROM capital_expenses ORDER BY sno ASC", conn)

    # Lifetime figures
    tot_sales = sales_df['amount'].sum() if not sales_df.empty else 0.0
    tot_cash = sales_df['cash'].sum() if not sales_df.empty else 0.0
    tot_gpay = sales_df['gpay'].sum() if not sales_df.empty else 0.0
    tot_purch = purch_df['amount'].sum() if not purch_df.empty else 0.0

    # TODAY'S CURRENT DATE FIGURES
    today_sales_df = sales_df[sales_df['date'] == today_date] if not sales_df.empty else pd.DataFrame()
    today_cash = today_sales_df['cash'].sum() if not today_sales_df.empty else 0.0
    today_gpay = today_sales_df['gpay'].sum() if not today_sales_df.empty else 0.0
    today_total_sales = today_sales_df['amount'].sum() if not today_sales_df.empty else 0.0

    today_purch_df = purch_df[purch_df['date'] == today_date] if not purch_df.empty else pd.DataFrame()
    today_total_purch = today_purch_df['amount'].sum() if not today_purch_df.empty else 0.0

    # Sync dynamic purchase in capital row 12
    conn.execute("UPDATE capital_expenses SET amount = ? WHERE UPPER(purpose) = 'PURCHASED'", (tot_purch,))
    conn.commit()

    cap_df = pd.read_sql("SELECT sno, purpose, quantity, amount FROM capital_expenses ORDER BY sno ASC", conn)
    tot_cap = cap_df['amount'].sum() if not cap_df.empty else 0.0

    trade_net = tot_sales - tot_purch
    cap_deficit = tot_cap - tot_sales
    recovery_rate = (tot_sales / tot_cap * 100) if tot_cap > 0 else 0.0

    # Tabs based on Role (Member vs Owner)
    if st.session_state.role == "Member":
        tabs = st.tabs(["🧾 New Bill (POS)", "💰 Sales Register", "📦 Stock Purchases"])
    else:
        tabs = st.tabs([
            "🧾 New Bill (POS)", 
            "💰 Sales Register", 
            "📦 Stock Purchases", 
            "🏢 Setup & Investments (Sheet 1)", 
            "📅 Daily P&L (Sheet 4)", 
            "📊 Financial Statement (Sheet 5&6)", 
            "🤝 Profit Share (Sheet 7)",
            "👥 User Management"
        ])

    # --- TAB 1: POS BILL COUNTER ---
    with tabs[0]:
        st.subheader("🧾 New POS Bill Generator")
        col_left, col_right = st.columns([1.2, 1])

        with col_left:
            st.markdown("##### Quick Service Shortcuts")
            btn_c1, btn_c2, btn_c3, btn_c4 = st.columns(4)
            if btn_c1.button("Printout (₹10)", use_container_width=True):
                st.session_state.pos_cart.append({"Item": "PRINTOUT", "Rate": 10.0, "Qty": 1, "Total": 10.0})
            if btn_c2.button("Xerox (₹5)", use_container_width=True):
                st.session_state.pos_cart.append({"Item": "XEROX", "Rate": 5.0, "Qty": 1, "Total": 5.0})
            if btn_c3.button("Spiral (₹50)", use_container_width=True):
                st.session_state.pos_cart.append({"Item": "SPIRAL", "Rate": 50.0, "Qty": 1, "Total": 50.0})
            if btn_c4.button("Photo 8+4 (₹110)", use_container_width=True):
                st.session_state.pos_cart.append({"Item": "PASSPORT PHOTO 8+4", "Rate": 110.0, "Qty": 1, "Total": 110.0})

            with st.form("custom_item_form", clear_on_submit=True):
                st.markdown("##### Custom Item / Service Entry")
                f1, f2, f3 = st.columns([2, 1, 1])
                c_item = f1.text_input("Item Name")
                c_rate = f2.number_input("Rate (₹)", min_value=1.0, value=10.0, step=5.0)
                c_qty = f3.number_input("Qty", min_value=1, value=1, step=1)
                if st.form_submit_button("➕ Add Item to Bill"):
                    if c_item:
                        st.session_state.pos_cart.append({"Item": c_item, "Rate": c_rate, "Qty": c_qty, "Total": c_rate * c_qty})
                        st.rerun()

            if st.session_state.pos_cart:
                cart_df = pd.DataFrame(st.session_state.pos_cart)
                st.dataframe(cart_df, use_container_width=True)
                if st.button("🗑️ Clear Cart"):
                    st.session_state.pos_cart = []
                    st.rerun()

        with col_right:
            bill_total = sum(i["Total"] for i in st.session_state.pos_cart)
            st.metric(label="Grand Total", value=f"₹{bill_total:,.2f}")

            pay_c1, pay_c2 = st.columns(2)
            cash_paid = pay_c1.number_input("Cash Amount (₹)", min_value=0.0, value=float(bill_total))
            gpay_paid = pay_c2.number_input("GPay / UPI (₹)", min_value=0.0, value=0.0)

            # Thermal receipt format
            receipt_text = f"""========================================
               ALIF TECH                
   Xerox, Print, Spiral & Online Hub    
========================================
Date   : {today_date}   Time: {now_time}
Served : {st.session_state.username} ({st.session_state.role})
----------------------------------------
Item                 Qty          Total
----------------------------------------\n"""
            for itm in st.session_state.pos_cart:
                receipt_text += f"{itm['Item'][:18]:<20} x{itm['Qty']:<3} ₹{itm['Total']:>10.2f}\n"
            receipt_text += f"""----------------------------------------
GRAND TOTAL:              ₹{bill_total:>10.2f}
Paid Cash  :              ₹{cash_paid:>10.2f}
Paid GPay  :              ₹{gpay_paid:>10.2f}
========================================
        THANK YOU! VISIT AGAIN          
========================================
"""
            st.text_area("Receipt Preview", receipt_text, height=200)

            action_col1, action_col2 = st.columns(2)
            with action_col1:
                save_clicked = st.button("✅ Save Sale", type="primary", use_container_width=True)
                if save_clicked:
                    if not st.session_state.pos_cart:
                        st.warning("Cart is empty!")
                    else:
                        cur = conn.cursor()
                        cur.execute("SELECT COALESCE(MAX(sno), 0) + 1 FROM sales")
                        next_sno = cur.fetchone()[0]
                        inv_no = f"AT-{datetime.datetime.now().strftime('%y%m%d%H%M')}"
                        desc = " + ".join([f"{i['Item']}(x{i['Qty']})" for i in st.session_state.pos_cart])[:60]
                        cur.execute("INSERT INTO sales (sno, item, date, cash, gpay, amount, invoice_no) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (next_sno, desc, today_date, cash_paid, gpay_paid, bill_total, inv_no))
                        conn.commit()
                        st.success(f"Invoice #{inv_no} saved successfully!")
                        st.session_state.pos_cart = []
                        st.rerun()

            with action_col2:
                # Direct Browser/Thermal Printer Print Button
                escaped_receipt = html.escape(receipt_text).replace("\n", "\\n")
                print_button_html = f"""
                <button onclick="printReceipt()" style="
                    width: 100%;
                    background-color: #0284C7;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                    font-size: 14px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 1px;
                ">🖨️ Print Receipt</button>

                <script>
                function printReceipt() {{
                    var content = "{escaped_receipt}";
                    var printWindow = window.open('', '', 'height=600,width=450');
                    printWindow.document.write('<html><head><title>Print Receipt</title>');
                    printWindow.document.write('<style>body{{font-family: monospace; font-size: 13px; white-space: pre; margin: 10px;}}</style>');
                    printWindow.document.write('</head><body>');
                    printWindow.document.write(content.replace(/\\n/g, '<br/>'));
                    printWindow.document.write('</body></html>');
                    printWindow.document.close();
                    printWindow.focus();
                    printWindow.print();
                    printWindow.close();
                }}
                </script>
                """
                components.html(print_button_html, height=45)

    # --- TAB 2: SALES REGISTER ---
    with tabs[1]:
        st.subheader("💰 Sales Register (SALED)")
        
        # If Owner: Show Lifetime Totals
        # If Member: Hide Lifetime Totals, show ONLY Today's Current Date Status!
        if st.session_state.role == "Owner":
            k1, k2, k3 = st.columns(3)
            k1.metric("Overall Cash Sales", f"₹{tot_cash:,.2f}")
            k2.metric("Overall GPay Sales", f"₹{tot_gpay:,.2f}")
            k3.metric("Overall Total Revenue", f"₹{tot_sales:,.2f}")
        else:
            st.markdown(f"##### 📅 Today's Live Counter Status ({today_date})")
            k1, k2, k3 = st.columns(3)
            k1.metric("Today's Cash Collection", f"₹{today_cash:,.2f}")
            k2.metric("Today's GPay Collection", f"₹{today_gpay:,.2f}")
            k3.metric("Today's Total Sales", f"₹{today_total_sales:,.2f}")

        st.dataframe(sales_df, use_container_width=True)

    # --- TAB 3: STOCK PURCHASES ---
    with tabs[2]:
        st.subheader("📦 Stock Purchases (PURCHASED)")
        
        # If Owner: Show Total Material Stock Cost
        # If Member: Show ONLY Today's Purchase Total!
        if st.session_state.role == "Owner":
            p1, p2 = st.columns(2)
            p1.metric("Total Stock Investment Cost", f"₹{tot_purch:,.2f}")
            p2.metric("Total Purchase Items Count", f"{len(purch_df)}")
        else:
            st.markdown(f"##### 📅 Today's Stock Purchases ({today_date})")
            p1, p2 = st.columns(2)
            p1.metric("Today's Total Stock Purchased", f"₹{today_total_purch:,.2f}")
            p2.metric("Today's Purchased Items", f"{len(today_purch_df)}")

        with st.expander("➕ Add Purchased Product / Stock"):
            with st.form("add_purch_form"):
                p_item = st.text_input("Product / Item Name")
                p_c1, p_c2, p_c3 = st.columns(3)
                
                # DATE CANNOT BE CHANGED - Automatically Locked to Today's Current Date
                p_date = p_c1.text_input("Date (Auto-Updated)", value=today_date, disabled=True)
                p_rate = p_c2.number_input("Rate (₹)", min_value=0.0, value=100.0)
                p_qty = p_c3.number_input("Quantity (PKT/Units)", min_value=1.0, value=1.0)
                p_amt = st.number_input("Total Amount (₹) [Leave 0 to auto-calculate]", min_value=0.0, value=0.0)

                if st.form_submit_button("Save Product"):
                    if p_item:
                        actual_amt = p_amt if p_amt > 0 else (p_rate * p_qty)
                        cur = conn.cursor()
                        cur.execute("SELECT COALESCE(MAX(sno), 0) + 1 FROM purchases")
                        next_sno = cur.fetchone()[0]
                        cur.execute("INSERT INTO purchases (sno, item, date, rate, quantity, amount) VALUES (?, ?, ?, ?, ?, ?)",
                                    (next_sno, p_item, today_date, p_rate, p_qty, actual_amt))
                        conn.commit()
                        st.success(f"Product '{p_item}' added with date {today_date}!")
                        st.rerun()

        st.dataframe(purch_df, use_container_width=True)

    # --- OWNER EXCLUSIVE TABS ---
    if st.session_state.role == "Owner":
        # TAB 4: SETUP & CAPITAL EXPENSES (EXACTLY 12 UNIQUE ITEMS)
        with tabs[3]:
            st.subheader("🏢 Setup & Capital Investments (Sheet 1)")
            st.metric("Total Setup Capital Invested", f"₹{tot_cap:,.2f}")
            st.dataframe(cap_df, use_container_width=True)

        # TAB 5: DAILY PROFIT AND LOSS
        with tabs[4]:
            st.subheader("📅 Date-wise Daily Profit & Loss Tracker (Sheet 4)")
            all_dates = sorted(list(set(sales_df['date'].dropna().tolist() + purch_df['date'].dropna().tolist())))
            pnl_records = []
            for d in all_dates:
                p_day = purch_df[purch_df['date'] == d]['amount'].sum() if not purch_df.empty else 0.0
                c_day = sales_df[sales_df['date'] == d]['cash'].sum() if not sales_df.empty else 0.0
                g_day = sales_df[sales_df['date'] == d]['gpay'].sum() if not sales_df.empty else 0.0
                tot_day = c_day + g_day
                net_day = tot_day - p_day
                st_day = "PROFIT" if net_day >= 0 else "LOSS"
                pnl_records.append({
                    "DATE": d, "PURCHASED (₹)": p_day, "CASH SALES (₹)": c_day,
                    "GPAY SALES (₹)": g_day, "TOTAL SALES (₹)": tot_day,
                    "DAILY NET P&L (₹)": net_day, "STATUS": st_day
                })
            st.dataframe(pd.DataFrame(pnl_records), use_container_width=True)

        # TAB 6: FINANCIAL STATEMENT & RECOVERY
        with tabs[5]:
            st.subheader("📊 Overall Financial Statement & Capital Recovery (Sheet 5&6)")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Capital Invested", f"₹{tot_cap:,.2f}")
            m2.metric("Total Revenue", f"₹{tot_sales:,.2f}")
            m3.metric("Trading Net Pool", f"₹{trade_net:,.2f}")
            m4.metric("Capital Deficit Remaining", f"₹{cap_deficit:,.2f}")
            st.progress(min(max(recovery_rate / 100, 0.0), 1.0), text=f"Breakeven Progress: {recovery_rate:.2f}%")

        # TAB 7: 3-WAY PROFIT SHARING
        with tabs[6]:
            st.subheader("🤝 3-Way Profit Sharing Dashboard (Sheet 7)")
            each_share = round(trade_net / 3.0, 2)
            sh_data = [
                {"ENTITY": "Shop Reserve (Alif Tech)", "RATIO": "33.33%", "ALLOCATION (₹)": each_share, "NOTES": "Shop Maintenance & Emergency Fund"},
                {"ENTITY": "Mohamed Fazil", "RATIO": "33.33%", "ALLOCATION (₹)": each_share, "NOTES": "Partner Profit Share"},
                {"ENTITY": "Aafif", "RATIO": "33.33%", "ALLOCATION (₹)": each_share, "NOTES": "Partner Profit Share"}
            ]
            st.dataframe(pd.DataFrame(sh_data), use_container_width=True)

        # TAB 8: USER MANAGEMENT (ADD & REMOVE REGISTERED USERS)
        with tabs[7]:
            st.subheader("👥 User Management Portal")
            
            u_col1, u_col2 = st.columns([1.2, 1])

            with u_col1:
                st.markdown("##### ➕ Manually Add User")
                with st.form("add_user_form", clear_on_submit=True):
                    new_u = st.text_input("New Username")
                    new_p = st.text_input("New Password", type="password")
                    new_r = st.selectbox("Role", ["Member", "Owner"])
                    
                    if st.form_submit_button("Register New User"):
                        if new_u and new_p:
                            cur = conn.cursor()
                            cur.execute("SELECT id FROM users WHERE username = ?", (new_u.strip(),))
                            if cur.fetchone():
                                st.error(f"Username '{new_u}' already exists!")
                            else:
                                dt = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                                cur.execute("INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
                                            (new_u.strip(), hash_pw(new_p.strip()), new_r, dt))
                                conn.commit()
                                st.success(f"User '{new_u}' added successfully as {new_r}!")
                                st.rerun()
                        else:
                            st.warning("Please provide username and password.")

            with u_col2:
                st.markdown("##### ❌ Remove User")
                users_list_raw = conn.execute("SELECT id, username, role FROM users ORDER BY id ASC").fetchall()
                removable_users = [u[1] for u in users_list_raw if u[1] != st.session_state.username]
                
                if removable_users:
                    user_to_del = st.selectbox("Select User to Remove", removable_users)
                    if st.button("🗑️ Delete Selected User", type="primary"):
                        cur = conn.cursor()
                        cur.execute("DELETE FROM users WHERE username = ?", (user_to_del,))
                        conn.commit()
                        st.success(f"User '{user_to_del}' deleted successfully!")
                        st.rerun()
                else:
                    st.info("No other users available to remove.")

            st.markdown("---")
            st.markdown("##### 📋 Registered Users List")
            users_df = pd.read_sql("SELECT id, username, role, created_at FROM users ORDER BY id ASC", conn)
            st.dataframe(users_df, use_container_width=True)

    conn.close()

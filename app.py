import streamlit as st
import collections
import uuid

st.set_page_config(page_title="TARGET MASTER PREDICTOR", page_icon="🎯", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background: #0c0f1d; }
    .stApp { background: #0c0f1d; color: #FFFFFF; }
    
    .app-header {
        text-align: center;
        background: linear-gradient(90deg, #38BDF8, #818CF8, #C084FC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px !important;
        font-weight: 900 !important;
        margin-bottom: 10px;
    }

    .game-panel {
        background: linear-gradient(135deg, #1e1b4b33, #0f172a);
        padding: 22px;
        border-radius: 20px;
        border: 2px solid #6366f1;
        margin: 15px 0;
        box-shadow: 0px 8px 25px rgba(99, 102, 241, 0.2);
    }

    .grand-success-box {
        background: linear-gradient(135deg, #78350f, #451a03);
        padding: 30px;
        border-radius: 25px;
        border: 3px solid #FBBF24;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0px 10px 35px rgba(251, 191, 36, 0.4);
    }

    .admin-panel-box {
        background: linear-gradient(135deg, #4c0519, #1f1218);
        padding: 24px;
        border-radius: 20px;
        border: 2px solid #fb7185;
        margin: 15px 0;
    }

    .wallet-stat-card {
        background: #111827;
        border: 2px solid #38BDF8;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
    }

    .stButton button {
        background: linear-gradient(135deg, #312e81, #1e1b4b) !important;
        color: #38BDF8 !important;
        border: 2px solid #6366f1 !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        height: 48px !important;
        font-size: 16px !important;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: #6366f1 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }

    input[type="text"], input[type="password"] {
        text-align: center !important;
        font-size: 18px !important;
        font-weight: bold !important;
        background-color: #111827 !important;
        color: #38BDF8 !important;
        border: 2px solid #38BDF8 !important;
        border-radius: 10px !important;
    }

    .history-item-row {
        background: #111827;
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 8px;
        border-left: 5px solid #6366f1;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-header'>🎯 TARGET MASTER PREDICTOR 🎯</div>", unsafe_allow_html=True)

# Session States
if 'allowed_keys' not in st.session_state:
    st.session_state.allowed_keys = ["target123", "bosco456", "rahul789"]
if 'blocked_keys' not in st.session_state:
    st.session_state.blocked_keys = []
if 'bound_devices' not in st.session_state:
    st.session_state.bound_devices = {}
if 'auth_type' not in st.session_state:
    st.session_state.auth_type = None
if 'logged_in_key' not in st.session_state:
    st.session_state.logged_in_key = None
if 'my_device_id' not in st.session_state:
    st.session_state.my_device_id = str(uuid.uuid4())

if 'history_details' not in st.session_state: st.session_state.history_details = []
if 'history' not in st.session_state: st.session_state.history = []
if 'num_history' not in st.session_state: st.session_state.num_history = []
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'last_prediction_bs' not in st.session_state: st.session_state.last_prediction_bs = None
if 'last_predicted_numbers' not in st.session_state: st.session_state.last_predicted_numbers = []
if 'initial_wallet' not in st.session_state: st.session_state.initial_wallet = 500
if 'wallet_balance' not in st.session_state: st.session_state.wallet_balance = 500
if 'current_level' not in st.session_state: st.session_state.current_level = 1
if 'is_skip' not in st.session_state: st.session_state.is_skip = False
if 'target_achieved' not in st.session_state: st.session_state.target_achieved = False

def handle_number_click(val):
    current_bs = "BIG" if val >= 5 else "SMALL"
    current_bs_short = "B" if val >= 5 else "S"
    
    base_unit = st.session_state.wallet_balance / 255
    multipliers = [1, 2, 4, 8, 16, 32, 64, 128]
    current_bet = max(1, round(base_unit * multipliers[st.session_state.current_level - 1]))

    status_str = "<span style='color:#38BDF8; font-weight:bold;'>➖ START</span>"

    # Big/Small basis calculations (Wallet updates only based on Big/Small win/loss)
    if st.session_state.last_prediction_bs is not None:
        if not st.session_state.is_skip:
            if current_bs_short == st.session_state.last_prediction_bs:
                st.session_state.wins += 1
                st.session_state.wallet_balance += current_bet  # WIN വരുമ്പോൾ വാലറ്റ് തുക കൂടും
                status_str = f"<span style='color:#00E676; font-weight:900;'>🟢 WIN (+₹{current_bet})</span>"
                st.session_state.current_level = 1  
            else:
                st.session_state.losses += 1
                st.session_state.wallet_balance = max(0, st.session_state.wallet_balance - current_bet)  # LOSS വരുമ്പോൾ വാലറ്റ് കുറയും
                status_str = f"<span style='color:#FF5252; font-weight:900;'>🔴 LOSS (-₹{current_bet})</span>"
                
                if st.session_state.current_level < 8:
                    st.session_state.current_level += 1  
                else:
                    st.session_state.current_level = 1  
        else:
            status_str = "<span style='color:#38BDF8; font-weight:bold;'>🔄 SKIPPED</span>"

    profit_target = (st.session_state.initial_wallet / 500) * 100
    target_goal_amount = st.session_state.initial_wallet + profit_target

    if st.session_state.wallet_balance >= target_goal_amount:
        st.session_state.target_achieved = True

    # Number prediction display in history ONLY (does not affect wallet balance at all)
    num_win_str = ""
    if st.session_state.last_predicted_numbers and val in st.session_state.last_predicted_numbers:
        num_win_str = " <span style='color:#00E676; font-size:12px; font-weight:900;'>[🎯 Number Win]</span>"

    st.session_state.history.append(current_bs_short)
    st.session_state.num_history.append(val)
    st.session_state.history_details.insert(0, {"num": val, "type": current_bs, "status": status_str, "num_win": num_win_str})

    hist = st.session_state.history
    num_hist = st.session_state.num_history

    if len(hist) < 3:
        st.session_state.last_prediction_bs = None
        st.session_state.last_predicted_numbers = []
        st.session_state.is_skip = False
    else:
        recent_four = hist[-4:] if len(hist) >= 4 else hist
        is_choppy = len(recent_four) == 4 and recent_four[0] != recent_four[1] and recent_four[1] != recent_four[2] and recent_four[2] != recent_four[3]
        
        recent_five = hist[-5:] if len(hist) >= 5 else hist
        is_long_streak = len(recent_five) >= 5 and all(x == recent_five[0] for x in recent_five)

        if is_choppy or is_long_streak:
            st.session_state.is_skip = True
        else:
            st.session_state.is_skip = False

        if st.session_state.current_level >= 4:
            next_pred = "S" if hist[-1] == "B" else "B"
        else:
            is_alternating = len(hist) >= 4 and hist[-1] != hist[-2] != hist[-3] != hist[-4]
            is_heavy_repeat = len(hist) >= 3 and hist[-1] == hist[-2] == hist[-3]

            if is_alternating:
                next_pred = "S" if hist[-1] == "B" else "B"
            elif is_heavy_repeat:
                next_pred = "S" if hist[-1] == "B" else "B"
            else:
                recent_window = hist[-4:] if len(hist) >= 4 else hist
                b_count = recent_window.count('B')
                s_count = recent_window.count('S')
                next_pred = "B" if b_count >= s_count else "S"

        st.session_state.last_prediction_bs = next_pred
        num_counts = collections.Counter(num_hist[-10:])
        st.session_state.last_predicted_numbers = [n for n, c in num_counts.most_common(2)]

# Login Screen
if st.session_state.auth_type is None:
    st.markdown("<div class='game-panel'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#38BDF8; text-align:center;'>🔐 ആക്സസ് ടൈപ്പ് തിരഞ്ഞെടുക്കുക</h3>", unsafe_allow_html=True)
    
    login_option = st.selectbox("ലോഗിൻ വിഭാഗം തിരഞ്ഞെടുക്കുക:", ["-- Select --", "User Login", "Admin Login"])
    
    if login_option == "User Login":
        user_input_key = st.text_input("User Access Key നൽകുക:", type="password")
        if st.button("Login as User", use_container_width=True):
            if user_input_key in st.session_state.blocked_keys:
                st.error("❌ ഈ കീ അഡ്മിൻ ബ്ലോക്ക് ചെയ്തിരിക്കുന്നു!")
            elif user_input_key in st.session_state.allowed_keys:
                if user_input_key in st.session_state.bound_devices:
                    if st.session_state.bound_devices[user_input_key] != st.session_state.my_device_id:
                        st.error("❌ ഈ കീ മറ്റൊരു ഡിവൈസിൽ രജിസ്റ്റർ ചെയ്തതാണ്!")
                        st.stop()
                else:
                    st.session_state.bound_devices[user_input_key] = st.session_state.my_device_id

                st.session_state.auth_type = "user"
                st.session_state.logged_in_key = user_input_key
                st.rerun()
            else:
                st.error("❌ തെറ്റായ User Key!")
                
    elif login_option == "Admin Login":
        admin_input_pass = st.text_input("Admin Password നൽകുക:", type="password")
        if st.button("Login as Admin", use_container_width=True):
            if admin_input_pass == "bosco123":
                st.session_state.auth_type = "admin"
                st.rerun()
            else:
                st.error("❌ തെറ്റായ Admin Password!")
                
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Admin Panel
if st.session_state.auth_type == "admin":
    st.markdown("<div class='admin-panel-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#fb7185; text-align: center;'>🛠️ ADMIN CONTROL PANEL</h2>", unsafe_allow_html=True)
    
    st.write("### 👤 Allowed User Keys & Control")
    
    for key in list(st.session_state.allowed_keys):
        col_k1, col_k2, col_k3 = st.columns([2, 1, 1])
        with col_k1:
            is_blocked = key in st.session_state.blocked_keys
            status_label = "🔴 (Blocked)" if is_blocked else ("🔒 (Bound)" if key in st.session_state.bound_devices else "🔓 (Active)")
            st.write(f"🔑 `{key}` {status_label}")
        with col_k2:
            is_blocked = key in st.session_state.blocked_keys
            if is_blocked:
                if st.button("🟢 Unblock", key=f"unblock_{key}"):
                    st.session_state.blocked_keys.remove(key)
                    st.success(f"'{key}' അൺബ്ലോക്ക് ചെയ്തു!")
                    st.rerun()
            else:
                if st.button("⛔ Block", key=f"block_{key}"):
                    st.session_state.blocked_keys.append(key)
                    st.warning(f"'{key}' ബ്ലോക്ക് ചെയ്തു!")
                    st.rerun()
        with col_k3:
            if st.button("🗑️ Remove", key=f"del_{key}"):
                st.session_state.allowed_keys.remove(key)
                if key in st.session_state.bound_devices:
                    del st.session_state.bound_devices[key]
                if key in st.session_state.blocked_keys:
                    st.session_state.blocked_keys.remove(key)
                st.success(f"'{key}' നീക്കം ചെയ്തു!")
                st.rerun()

    st.divider()
    new_u = st.text_input("New User Key:")
    if st.button("Add User Key", use_container_width=True) and new_u:
        if new_u not in st.session_state.allowed_keys:
            st.session_state.allowed_keys.append(new_u)
            st.success("Key successfully added!")
            st.rerun()
        else:
            st.warning("ഈ കീ ഇതിനകം നിലവിലുണ്ട്!")

    if st.button("🚪 Logout Admin", use_container_width=True):
        st.session_state.auth_type = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Logout button
if st.session_state.auth_type == "user":
    if st.button("🚪 Logout"):
        st.session_state.auth_type = None
        st.session_state.logged_in_key = None
        st.rerun()

st.divider()

if st.session_state.auth_type == "user":
    
    # 🌟 TARGET ACHIEVED SECTION
    if st.session_state.target_achieved:
        st.balloons()
        profit_earned = int((st.session_state.initial_wallet / 500) * 100)
        st.markdown(f"""
            <div class="grand-success-box">
                <h1 style="color: #FEE140; font-size: 32px; font-weight: 900; text-shadow: 2px 2px 8px rgba(0,0,0,0.6);">🌟 TARGET ACHIEVED SUCCESSFULLY! 🌟</h1>
                <h3 style="color: #FFFFFF; margin-top: 10px; font-size: 20px;">അഭിനന്ദനങ്ങൾ! നിങ്ങൾ ടാർഗറ്റ് ലക്ഷ്യം ഭേദിച്ചു!</h3>
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 14px; margin-top: 15px; border: 1px solid #FBBF24;">
                    <p style="color: #E2E8F0; font-size: 16px; margin: 4px 0;">Initial Wallet: <b>₹{st.session_state.initial_wallet}</b></p>
                    <p style="color: #00E676; font-size: 18px; margin: 4px 0;">Profit Earned: <b>+₹{profit_earned}</b></p>
                    <p style="color: #FBBF24; font-size: 22px; font-weight: 900; margin: 4px 0;">Final Wallet: ₹{st.session_state.wallet_balance}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start New Target Session", use_container_width=True):
            st.session_state.target_achieved = False
            st.session_state.history_details = []
            st.session_state.history = []
            st.session_state.num_history = []
            st.session_state.wins = 0
            st.session_state.losses = 0
            st.session_state.last_prediction_bs = None
            st.session_state.last_predicted_numbers = []
            st.session_state.current_level = 1
            st.session_state.is_skip = False
            st.rerun()
        st.stop()

    # Regular Live Wallet & Prediction Section
    st.markdown("<p style='text-align: center; font-weight: bold; color: #38BDF8; font-size: 17px;'>💰 നിങ്ങളുടെ വാലറ്റ് ബാലൻസ് നൽകുക / ലൈവ് ബാലൻസ് (₹):</p>", unsafe_allow_html=True)
    wallet_col1, wallet_col2, wallet_col3 = st.columns([1, 2, 1])
    with wallet_col2:
        wallet_input = st.text_input("Wallet Input", value=str(st.session_state.wallet_balance), label_visibility="collapsed", key="u_wallet_box")
        if wallet_input.isdigit() and int(wallet_input) >= 100:
            new_val = int(wallet_input)
            if new_val != st.session_state.wallet_balance:
                st.session_state.initial_wallet = new_val
                st.session_state.wallet_balance = new_val

    fixed_profit_target = int((st.session_state.initial_wallet / 500) * 100)
    target_goal_amount = st.session_state.initial_wallet + fixed_profit_target

    st.markdown(f"""
        <div style="display: flex; gap: 12px; margin: 15px 0;">
            <div class="wallet-stat-card" style="flex: 1;">
                <div style="font-size: 13px; font-weight: 800; color: #38BDF8;">WINS 🟢</div>
                <div style="font-size: 22px; font-weight: 900; color: #00E676;">{st.session_state.wins}</div>
            </div>
            <div class="wallet-stat-card" style="flex: 1; border-color: #FF5252;">
                <div style="font-size: 13px; font-weight: 800; color: #FF5252;">LOSSES 🔴</div>
                <div style="font-size: 22px; font-weight: 900; color: #FF5252;">{st.session_state.losses}</div>
            </div>
        </div>
        <div style="background: #111827; border: 2px solid #6366f1; border-radius: 12px; padding: 14px; text-align: center; margin-bottom: 15px;">
            <span style="color: #38BDF8; font-weight: bold; font-size: 15px;">🟢 Live Wallet: </span>
            <span style="color: #FBBF24; font-weight: 900; font-size: 21px;">₹{st.session_state.wallet_balance}</span> 
            <span style="color: #94A3B8; font-size: 13px;">(Goal: ₹{target_goal_amount})</span>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Reset Data", use_container_width=True, key="u_reset"):
        st.session_state.history_details = []
        st.session_state.history = []
        st.session_state.num_history = []
        st.session_state.wins = 0
        st.session_state.losses = 0
        st.session_state.last_prediction_bs = None
        st.session_state.last_predicted_numbers = []
        st.session_state.current_level = 1
        st.session_state.is_skip = False
        st.session_state.target_achieved = False
        st.rerun()

    st.markdown("<p style='text-align: center; font-weight: bold; color: #38BDF8; font-size: 17px;'>വന്ന നമ്പർ തിരഞ്ഞെടുക്കുക:</p>", unsafe_allow_html=True)
    cols_top = st.columns(5)
    nums_top = [(0, "0", "🟣 🔴"), (1, "1", "🟢"), (2, "2", "🔴"), (3, "3", "🟢"), (4, "4", "🔴")]
    for idx, (num_val, num_str, badge) in enumerate(nums_top):
        with cols_top[idx]:
            if st.button(f"{num_str}\n{badge}", key=f"u_btn_{num_val}", use_container_width=True):
                handle_number_click(num_val)
                st.rerun()

    cols_bottom = st.columns(5)
    nums_bottom = [(5, "5", "🟢 🟣"), (6, "6", "🔴"), (7, "7", "🟢"), (8, "8", "🔴"), (9, "9", "🟢")]
    for idx, (num_val, num_str, badge) in enumerate(nums_bottom):
        with cols_bottom[idx]:
            if st.button(f"{num_str}\n{badge}", key=f"u_btn_{num_val}", use_container_width=True):
                handle_number_click(num_val)
                st.rerun()

    if st.session_state.last_prediction_bs is not None:
        next_pred = st.session_state.last_prediction_bs
        likely_nums = st.session_state.last_predicted_numbers
        pred_text = "⚠️ SMART SKIP (ഈ റൗണ്ട് സുരക്ഷിതമായി വിടുക)" if st.session_state.is_skip else ("BIG 🟢" if next_pred == "B" else "SMALL 🔴")
        color_code = "#38BDF8" if st.session_state.is_skip else ("#00E676" if next_pred == "B" else "#FF5252")

        base_unit = st.session_state.wallet_balance / 255
        multipliers = [1, 2, 4, 8, 16, 32, 64, 128]
        suggested_bet = max(1, round(base_unit * multipliers[st.session_state.current_level - 1]))

        st.markdown(f"""
            <div class="game-panel">
                <div style="color: #94A3B8; font-size: 13px; font-weight: bold; letter-spacing: 1px;">NEXT TARGET PREDICTION</div>
                <div style="font-size: 28px; font-weight: 900; color: {color_code}; margin: 6px 0;">{pred_text}</div>
                <div style="color: #E2E8F0; font-size: 14px; margin-bottom: 5px;">📊 Likely Numbers: <b style="color:#FBBF24;">{likely_nums}</b></div>
                <hr style="border-color: #312e81; margin: 8px 0;">
                <div style="color: #38BDF8; font-size: 15px; font-weight: bold;">🛡️ Level {st.session_state.current_level} | Suggested Bet: ₹{suggested_bet}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style='color: #38BDF8; text-align: center; margin-top: 20px;'>📜 History & Performance</h3>", unsafe_allow_html=True)
    if not st.session_state.history_details:
        st.markdown("<p style='text-align: center; color: #94A3B8;'>ഇതുവരെ ഗെയിം ഹിസ്റ്ററി ഒന്നുമില്ല. മുകളിലെ നമ്പറുകളിൽ ക്ലിക്ക് ചെയ്യുക.</p>", unsafe_allow_html=True)
    else:
        for item in st.session_state.history_details[:10]:
            st.markdown(f"""
              <div class="history-item-row">
                    <div><b>Number:</b> {item['num']} ({item['type']}){item['num_win']}</div>
                    <div>{item['status']}</div>
                </div>
            """, unsafe_allow_html=True)

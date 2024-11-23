import streamlit as st
import json
import random
import asyncio
import aiohttp
from datetime import datetime
import time
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import os
from pathlib import Path


# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f'friend_spammer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
)

@dataclass
class Account:
    display_name: str
    account_id: str
    device_id: str
    secret: str

class FriendRequestManager:
    def __init__(self):
        self.base_url = "https://account-public-service-prod.ol.epicgames.com"
        self.friends_url = "https://friends-public-service-prod.ol.epicgames.com"
        self.auth_tokens = {
            "iOS": "Basic MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE=",
            "Android": "Basic M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="
        }

    def get_account_files():
        """Get all JSON files from the accounts folder"""
        accounts_dir = Path("accounts")
        if accounts_dir.exists():
            return [f for f in accounts_dir.glob("*.json")]
        return []

    async def get_auth_token(self, account: Account) -> Optional[str]:
        data = {
            "grant_type": "device_auth",
            "account_id": account.account_id,
            "device_id": account.device_id,
            "secret": account.secret
        }

        for platform, auth_token in self.auth_tokens.items():
            try:
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": auth_token
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/account/api/oauth/token",
                        headers=headers,
                        data=data
                    ) as response:
                        response_text = await response.text()
                        
                        if response.status == 200:
                            response_data = json.loads(response_text)
                            self.log(f"Successfully authenticated with {platform}", "success")
                            return response_data.get('access_token')
                        else:
                            self.log(f"Auth failed with {platform}: {response_text}", "warning")
            except Exception as e:
                self.log(f"Error with {platform}: {str(e)}", "error")
                continue
        return None

    async def get_user_id(self, display_name: str, auth_token: str) -> Optional[str]:
        headers = {
            "Authorization": f"bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/account/api/public/account/displayName/{display_name}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('id')
                    return None
        except Exception as e:
            self.log(f"Error getting user ID: {str(e)}", "error")
            return None

    # Add this to the FriendRequestManager class
    async def send_friend_request(self, friend_id: str, accounts: List[Account]):
        while st.session_state.running:
            try:
                # Check at the start of each loop if we should stop
                if not st.session_state.running:
                    break

                account = random.choice(accounts)
                auth_token = await self.get_auth_token(account)
                
                # Check again after authentication
                if not st.session_state.running:
                    break

                if not auth_token:
                    self.log(f"Failed to get auth token for {account.display_name}", "error")
                    st.rerun()
                    continue

                headers = {
                    "Authorization": f"bearer {auth_token}",
                    "Content-Type": "application/json"
                }
                
                # Check before making request
                if not st.session_state.running:
                    break

                async with aiohttp.ClientSession() as session:
                    # Send friend request
                    async with session.post(
                        f"{self.friends_url}/friends/api/v1/{account.account_id}/friends/{friend_id}",
                        headers=headers
                    ) as response:
                        # Check after request
                        if not st.session_state.running:
                            break

                        if response.status == 204:
                            # Delete friend request
                            async with session.delete(
                                f"{self.friends_url}/friends/api/v1/{account.account_id}/friends/{friend_id}",
                                headers=headers
                            ) as delete_response:
                                if delete_response.status == 204:
                                    st.session_state.request_count += 1
                                    self.log(f"Friend request cycle completed with {account.display_name} ({st.session_state.request_count} total)", "success")
                                    self.update_stats()
                                    st.rerun()
                        elif response.status == 429:
                            data = await response.json()
                            wait_time = data.get('messageVars', [30])[0]
                            self.log(f"Rate limited. Waiting {wait_time} seconds", "warning")
                            st.rerun()
                            
                            # Break up the sleep into smaller chunks to check for stop
                            for _ in range(int(wait_time)):
                                if not st.session_state.running:
                                    break
                                await asyncio.sleep(1)
                        else:
                            response_text = await response.text()
                            self.log(f"Request failed: {response_text}", "error")
                            st.rerun()

                # Check before delay
                if not st.session_state.running:
                    break

                # Break up the sleep into smaller chunks
                for _ in range(3):  # 3 seconds delay
                    if not st.session_state.running:
                        break
                    await asyncio.sleep(1)

            except Exception as e:
                self.log(f"Error in friend request cycle: {str(e)}", "error")
                st.rerun()
                
                # Check before error delay
                if not st.session_state.running:
                    break
                await asyncio.sleep(5)

        # Final cleanup when stopped
        self.log("Process stopped", "warning")
        st.rerun()

    def log(self, message: str, level: str = "info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        if 'log' not in st.session_state:
            st.session_state.log = []
        
        st.session_state.log.append(log_entry)
        
        # Keep only last 100 messages
        if len(st.session_state.log) > 100:
            st.session_state.log = st.session_state.log[-100:]

    def update_stats(self):
        if 'start_time' in st.session_state:
            elapsed = time.time() - st.session_state.start_time
            st.session_state.elapsed_time = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
        
        if 'request_count' in st.session_state:
            success_rate = (st.session_state.request_count / max(st.session_state.total_attempts, 1)) * 100
            st.session_state.success_rate = f"{success_rate:.1f}%"

def initialize_session_state():
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'request_count' not in st.session_state:
        st.session_state.request_count = 0
    if 'total_attempts' not in st.session_state:
        st.session_state.total_attempts = 0
    if 'success_rate' not in st.session_state:
        st.session_state.success_rate = "0%"
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = "0m 0s"

async def run_friend_requests(manager: FriendRequestManager, accounts: List[Account], friend_id: str):
    await manager.send_friend_request(friend_id, accounts)

def main():
    st.set_page_config(page_title="Friend Request Manager", page_icon="🤝", layout="wide")
    
    # Add this at the beginning of your friend_spammer.py

    # Custom CSS with modern design
    st.markdown("""
    <style>
        /* Modern color scheme */
        :root {
            --primary: #4f46e5;
            --secondary: #3b82f6;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --background: #0f172a;
            --card: #1e293b;
            --text: #f8fafc;
        }

        /* Main container and background */
        .stApp {
            background: linear-gradient(145deg, var(--background), #1e1b4b);
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: var(--card);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 2rem;
        }

        /* Headers */
        h1, h2, h3 {
            color: var(--text) !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px !important;
        }

        /* Metrics styling */
        [data-testid="stMetric"] {
            background: var(--card);
            padding: 1rem;
            border-radius: 0.75rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
                        0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
        }

        [data-testid="stMetricValue"] {
            color: var(--primary) !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricLabel"] {
            color: rgba(255, 255, 255, 0.6) !important;
        }

        /* Button styling */
        .stButton button {
            width: 100%;
            padding: 0.75rem 1.5rem;
            border-radius: 0.75rem;
            font-weight: 600;
            transition: all 0.2s ease;
            border: none;
        }

        .stButton button:first-child {
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            color: white;
        }

        .stButton button:first-child:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }

        .stButton button[kind="secondary"] {
            background: var(--error);
            color: white;
        }

        .stButton button[kind="secondary"]:hover {
            background: #dc2626;
            transform: translateY(-2px);
        }

        /* File uploader */
        [data-testid="stFileUploader"] {
            background: var(--card);
            padding: 1.5rem;
            border-radius: 0.75rem;
            border: 2px dashed rgba(255, 255, 255, 0.2);
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--primary);
        }

        /* Input fields */
        .stTextInput input {
            background: var(--card);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0.75rem;
            padding: 0.75rem 1rem;
            color: var(--text);
        }

        .stTextInput input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.2);
        }

        /* Log container */
        pre {
            background: var(--card) !important;
            border-radius: 0.75rem !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 1rem !important;
            max-height: 400px !important;
            overflow-y: auto !important;
        }

        code {
            color: var(--text) !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Success/Error messages */
        .success {
            padding: 0.75rem;
            border-radius: 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid var(--success);
            color: var(--success);
            margin: 0.5rem 0;
        }

        .error {
            padding: 0.75rem;
            border-radius: 0.5rem;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid var(--error);
            color: var(--error);
            margin: 0.5rem 0;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--card);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.3);
        }

        /* Loading animation */
        .stProgress > div > div > div {
            background: linear-gradient(45deg, var(--primary), var(--secondary));
        }

        /* Divider */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, 
                transparent, 
                rgba(255, 255, 255, 0.1), 
                transparent
            );
            margin: 2rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        /* File uploader styling */
        [data-testid="stFileUploader"] {
            background: var(--card);
            padding: 1.5rem;
            border-radius: 0.75rem;
            border: 2px dashed rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--primary);
            background: rgba(79, 70, 229, 0.1);
        }

        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
            color: var(--text);
            padding: 0.5rem 1rem;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }

        .stTabs [aria-selected="true"] {
            background-color: var(--primary) !important;
            border-color: var(--primary) !important;
        }

        /* Selectbox styling */
        [data-baseweb="select"] {
            background-color: var(--card);
            border-radius: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        [data-baseweb="select"]:hover {
            border-color: var(--primary);
        }

        [data-baseweb="popover"] {
            background-color: var(--card);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0.5rem;
        }

        [data-baseweb="option"] {
            background-color: transparent;
        }

        [data-baseweb="option"]:hover {
            background-color: rgba(255, 255, 255, 0.05);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    manager = FriendRequestManager()

    st.title("Friend Request Manager")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # Only show file upload and target input if not running
        if not st.session_state.get('running', False):
            # Create tabs for different upload methods
            tab1, tab2 = st.tabs(["Upload File", "Select File"])
            
            with tab1:
                uploaded_file = st.file_uploader(
                    "Drag and drop or click to upload",
                    type=['json'],
                    help="Upload your accounts JSON file"
                )
                
            with tab2:
                account_files = [f for f in Path("accounts").glob("*.json")] if Path("accounts").exists() else []
                if account_files:
                    selected_file = st.selectbox(
                        "Select an account file",
                        options=account_files,
                        format_func=lambda x: x.name
                    )
                else:
                    st.info("No JSON files found in the 'accounts' folder")
            
            target_name = st.text_input("Target Username")
            
            # Start button
            if (uploaded_file or ('selected_file' in locals() and selected_file)) and target_name:
                if st.button("Start Process", use_container_width=True):
                    try:
                        # Load accounts from either uploaded file or selected file
                        if uploaded_file:
                            file_content = uploaded_file.read().decode('utf-8')
                            accounts_data = json.loads(file_content)
                        else:
                            with open(selected_file, 'r') as f:
                                accounts_data = json.loads(f.read())
                        
                        # Handle both single account and list of accounts
                        if isinstance(accounts_data, dict):
                            accounts_data = [accounts_data]
                        
                        accounts = [
                            Account(
                                display_name=acc.get('display_name', ''),
                                account_id=acc.get('account_id', ''),
                                device_id=acc.get('device_id', ''),
                                secret=acc.get('secret', '')
                            ) for acc in accounts_data
                        ]
                        
                        # Reset all session state
                        st.session_state.running = True
                        st.session_state.start_time = time.time()
                        st.session_state.accounts = accounts
                        st.session_state.target_name = target_name
                        st.session_state.request_count = 0
                        st.session_state.total_attempts = 0
                        st.session_state.success_rate = "0%"
                        st.session_state.elapsed_time = "0m 0s"
                        st.session_state.log = []
                        
                        manager.log(f"Loaded {len(accounts)} accounts", "success")
                        st.experimental_rerun()
                        
                    except Exception as e:
                        st.error(f"Error starting process: {str(e)}")
        
        # Show stop button only if running
        if st.session_state.get('running', False):
            if st.button("Stop Process", type="secondary", use_container_width=True):
                st.session_state.running = False
                manager.log("Process stopped", "warning")
                time.sleep(0.1)  # Small delay to ensure final log message
                st.experimental_rerun()

        # Stats
        st.header("Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Requests", st.session_state.get('request_count', 0))
        with col2:
            st.metric("Success Rate", st.session_state.get('success_rate', '0%'))
        
        if st.session_state.get('running', False):
            elapsed = time.time() - st.session_state.get('start_time', time.time())
            st.session_state.elapsed_time = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
        st.metric("Active Time", st.session_state.get('elapsed_time', '0m 0s'))

    # Log container
    st.markdown("### Process Log")
    log_container = st.empty()
    
    # Display logs
    if 'log' in st.session_state:
        log_text = "\n".join(st.session_state.log)
        log_container.code(log_text)

    # Run the friend request process
    if st.session_state.get('running', False) and 'accounts' in st.session_state and 'target_name' in st.session_state:
        try:
            # Get target ID first
            first_account = st.session_state.accounts[0]
            auth_token = asyncio.run(manager.get_auth_token(first_account))
            
            if auth_token:
                target_id = asyncio.run(manager.get_user_id(st.session_state.target_name, auth_token))
                if target_id:
                    asyncio.run(run_friend_requests(manager, st.session_state.accounts, target_id))
                else:
                    st.error("Could not find target user")
                    st.session_state.running = False
                    manager.log("Could not find target user", "error")
                    st.experimental_rerun()
            else:
                st.error("Failed to authenticate")
                st.session_state.running = False
                manager.log("Failed to authenticate", "error")
                st.experimental_rerun()
                
        except Exception as e:
            st.error(f"Error in friend request process: {str(e)}")
            st.session_state.running = False
            manager.log(f"Error in friend request process: {str(e)}", "error")
            st.experimental_rerun()

if __name__ == "__main__":
    main()

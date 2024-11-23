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
        if 'should_stop' not in st.session_state:  # Add this
            st.session_state.should_stop = False

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
        while st.session_state.running and not st.session_state.should_stop:
            try:
                if st.session_state.should_stop:
                    break

                account = random.choice(accounts)
                auth_token = await self.get_auth_token(account)
                
                if not auth_token or st.session_state.should_stop:
                    continue

                headers = {
                    "Authorization": f"bearer {auth_token}",
                    "Content-Type": "application/json"
                }
                
                async with aiohttp.ClientSession() as session:
                    if st.session_state.should_stop:
                        break

                    async with session.post(
                        f"{self.friends_url}/friends/api/v1/{account.account_id}/friends/{friend_id}",
                        headers=headers
                    ) as response:
                        if st.session_state.should_stop:
                            break

                        if response.status == 204:
                            async with session.delete(
                                f"{self.friends_url}/friends/api/v1/{account.account_id}/friends/{friend_id}",
                                headers=headers
                            ) as delete_response:
                                if delete_response.status == 204:
                                    st.session_state.request_count += 1
                                    self.log(f"Friend request cycle completed with {account.display_name} ({st.session_state.request_count} total)", "success")
                                    self.update_stats()
                        elif response.status == 429:
                            data = await response.json()
                            wait_time = data.get('messageVars', [30])[0]
                            self.log(f"Rate limited. Waiting {wait_time} seconds", "warning")
                            
                            # Break up the wait time
                            for _ in range(int(wait_time)):
                                if st.session_state.should_stop:
                                    break
                                await asyncio.sleep(1)
                        else:
                            response_text = await response.text()
                            self.log(f"Request failed: {response_text}", "error")

                if st.session_state.should_stop:
                    break

                # Break up the delay
                for _ in range(3):
                    if st.session_state.should_stop:
                        break
                    await asyncio.sleep(1)

            except Exception as e:
                self.log(f"Error in friend request cycle: {str(e)}", "error")
                if st.session_state.should_stop:
                    break
                await asyncio.sleep(5)

        # Clean up when stopped
        if st.session_state.should_stop:
            self.log("Process stopped completely", "warning")
            st.session_state.running = False
            st.session_state.should_stop = False

    def log(self, message: str, level: str = "info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        if 'log' not in st.session_state:
            st.session_state.log = []
        
        st.session_state.log.append(log_entry)
        
        # Keep only last 100 messages
        if len(st.session_state.log) > 100:
            st.session_state.log = st.session_state.log[-100:]
        
        # Force immediate update of displays
        if hasattr(st.session_state, 'update_displays'):
            st.session_state.update_displays()

    def update_stats(self):
        if 'start_time' in st.session_state:
            elapsed = time.time() - st.session_state.start_time
            st.session_state.elapsed_time = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
        
        if 'request_count' in st.session_state:
            success_rate = (st.session_state.request_count / max(st.session_state.total_attempts, 1)) * 100
            st.session_state.success_rate = f"{success_rate:.1f}%"

def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'running': False,
        'request_count': 0,
        'total_attempts': 0,
        'success_rate': "0%",
        'elapsed_time': "0m 0s",
        'should_stop': False,
        'log': [],
        'accounts': None,
        'target_name': None,
        'start_time': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

async def run_friend_requests(manager: FriendRequestManager, accounts: List[Account], friend_id: str):
    await manager.send_friend_request(friend_id, accounts)

def main():
    st.set_page_config(page_title="Friend Request Manager", page_icon="🤝", layout="wide")
    
    # Initialize session state
    initialize_session_state()
    
    manager = FriendRequestManager()

    st.title("Friend Request Manager")

    # Create placeholders for live updates
    stats_container = st.empty()
    log_container = st.empty()

    # Function to update stats
    def update_stats():
        with stats_container.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Requests", st.session_state.get('request_count', 0))
            with col2:
                st.metric("Success Rate", st.session_state.get('success_rate', '0%'))
            with col3:
                if st.session_state.get('running', False):
                    elapsed = time.time() - st.session_state.get('start_time', time.time())
                    st.session_state.elapsed_time = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
                st.metric("Active Time", st.session_state.elapsed_time)

    # Function to update log
    def update_log():
        if 'log' in st.session_state:
            log_container.code("\n".join(st.session_state.log))

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
                        st.session_state.should_stop = False
                        st.session_state.start_time = time.time()
                        st.session_state.accounts = accounts
                        st.session_state.target_name = target_name
                        st.session_state.request_count = 0
                        st.session_state.total_attempts = 0
                        st.session_state.success_rate = "0%"
                        st.session_state.elapsed_time = "0m 0s"
                        st.session_state.log = []
                        
                        manager.log(f"Loaded {len(accounts)} accounts", "success")
                        
                    except Exception as e:
                        st.error(f"Error starting process: {str(e)}")
        
        # Show stop button only if running
        if st.session_state.running:
            if st.button("Stop Process", type="secondary", use_container_width=True):
                st.session_state.should_stop = True
                st.session_state.running = False
                manager.log("Stopping process...", "warning")

    # Initial stats and log display
    update_stats()
    update_log()

    # Run the friend request process
    if st.session_state.running and 'accounts' in st.session_state and 'target_name' in st.session_state:
        try:
            # Get target ID first
            first_account = st.session_state.accounts[0]
            auth_token = asyncio.run(manager.get_auth_token(first_account))
            
            if auth_token:
                target_id = asyncio.run(manager.get_user_id(st.session_state.target_name, auth_token))
                if target_id:
                    while st.session_state.running and not st.session_state.should_stop:
                        # Update displays
                        update_stats()
                        update_log()
                        
                        # Run friend requests
                        asyncio.run(run_friend_requests(manager, st.session_state.accounts, target_id))
                        
                        # Small delay to prevent excessive updates
                        time.sleep(0.1)
                else:
                    st.error("Could not find target user")
                    st.session_state.running = False
                    manager.log("Could not find target user", "error")
            else:
                st.error("Failed to authenticate")
                st.session_state.running = False
                manager.log("Failed to authenticate", "error")
                
        except Exception as e:
            st.error(f"Error in friend request process: {str(e)}")
            st.session_state.running = False
            manager.log(f"Error in friend request process: {str(e)}", "error")

    # Final update after stopping
    if not st.session_state.running:
        update_stats()
        update_log()

if __name__ == "__main__":
    main()

import os
import time
from instagrapi import Client

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
GROUP_NAME = os.getenv("IG_GROUP_NAME")
WELCOME_DELAY = int(os.getenv("WELCOME_DELAY", 5))

if not USERNAME or not PASSWORD or not GROUP_NAME:
    print("❌ Missing required environment variables.")
    exit(1)

cl = Client()
cl.login(USERNAME, PASSWORD)

def get_thread_id_by_title(title):
    threads = cl.direct_threads()
    for thread in threads:
        if thread.title == title:
            return thread.id
    return None

thread_id = get_thread_id_by_title(GROUP_NAME)
if not thread_id:
    print("❌ Group not found with title:", GROUP_NAME)
    exit(1)

print("✅ Login successful!")
print("🚀 Starting welcome bot for Thread ID:", thread_id)

user_ids = set()

while True:
    thread = cl.direct_thread(thread_id)
    for user in thread.users:
        if user.pk not in user_ids:
            user_ids.add(user.pk)
            try:
                cl.direct_send(text=f"👋 Welcome @{user.username}!", thread_ids=[thread_id])
                print(f"✅ Sent welcome message to {user.username}")
            except Exception as e:
                print("⚠️ Error sending welcome message:", e)
    time.sleep(WELCOME_DELAY)
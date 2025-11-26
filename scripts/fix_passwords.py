"""
Fix script to update all users with proper password hashes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import SessionLocal, User
from security.core import hash_password

db = SessionLocal()

# Map of email to default password
users_passwords = {
    'info@techcorp.com': 'TechCorp123',
    'careers@innovalabs.com': 'InnovaLabs456',
    'hello@webdesignpro.com': 'WebDesign789',
    'jobs@dataviz.com': 'DataViz123',
    'recruit@cloudnine.com': 'CloudNine456',
    'contact@mobilefirst.com': 'MobileFirst789',
    'security@cybersecure.com': 'CyberSecure123',
    'careers@greentech.com': 'GreenTech456',
    'lopezgordillocarlosdaniel1@gmail.com': 'Carlos123',
    'carlosgordillo3030@gmail.com': 'Carlos456'
}

# Update all users with proper hashes
all_users = db.query(User).all()
for user in all_users:
    if user.email in users_passwords:
        pwd = users_passwords[user.email]
    else:
        pwd = 'password123'  # Default for any others
    
    user.hashed_password = hash_password(pwd)
    print(f"✓ Updated {user.email} with password: {pwd}")

db.commit()
print(f"\n✅ Total {len(all_users)} users updated with proper password hashes!")

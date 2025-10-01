"""
Authentication Module
Handles user login, registration, and role-based access control
"""

import json
import os
from datetime import datetime
import hashlib
import uuid


class Authentication:
    """Handle user authentication and authorization"""
    
    def __init__(self, users_file='data/users.json'):
        self.users_file = users_file
        self.ensure_file_exists()
        
        # Define permissions for each role
        self.role_permissions = {
            'Administrator': ['view_all', 'edit_all', 'delete_all', 'manage_users', 'export_data'],
            'Investor': ['view_all', 'view_analytics', 'export_data'],
            'Researcher': ['view_all', 'view_analytics', 'download_reports']
        }
    
    def ensure_file_exists(self):
        """Create users.json with default users if it doesn't exist"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        
        if not os.path.exists(self.users_file):
            # Create default users
            default_users = [
                {
                    'id': str(uuid.uuid4()),
                    'username': 'admin',
                    'password': self.hash_password('admin123'),
                    'email': 'admin@chronominerals.com',
                    'role': 'Administrator',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'id': str(uuid.uuid4()),
                    'username': 'investor1',
                    'password': self.hash_password('investor123'),
                    'email': 'investor@example.com',
                    'role': 'Investor',
                    'created_at': datetime.now().isoformat()
                },
                {
                    'id': str(uuid.uuid4()),
                    'username': 'researcher1',
                    'password': self.hash_password('research123'),
                    'email': 'researcher@example.com',
                    'role': 'Researcher',
                    'created_at': datetime.now().isoformat()
                }
            ]
            
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f, indent=4)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        """Load users from file"""
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def save_users(self, users):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
    
    def register(self, username, password, email, role='Researcher'):
        """Register a new user"""
        if not username or not password or not email:
            return {'success': False, 'message': 'All fields are required'}
        
        users = self.load_users()
        
        # Check if username exists
        if any(user['username'].lower() == username.lower() for user in users):
            return {'success': False, 'message': 'Username already exists'}
        
        # Create new user
        new_user = {
            'id': str(uuid.uuid4()),
            'username': username,
            'password': self.hash_password(password),
            'email': email,
            'role': role,
            'created_at': datetime.now().isoformat()
        }
        
        users.append(new_user)
        self.save_users(users)
        
        return {'success': True, 'message': 'User registered successfully'}
    
    def login(self, username, password):
        """Authenticate user login"""
        if not username or not password:
            return {'success': False, 'message': 'Username and password required'}
        
        users = self.load_users()
        
        # Find user
        user = None
        for u in users:
            if u['username'].lower() == username.lower():
                user = u
                break
        
        if not user:
            return {'success': False, 'message': 'Invalid username or password'}
        
        # Verify password
        if self.hash_password(password) != user['password']:
            return {'success': False, 'message': 'Invalid username or password'}
        
        # Return user data (without password)
        return {
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role']
            }
        }
    
    def check_permission(self, role, permission):
        """Check if a role has a specific permission"""
        if role not in self.role_permissions:
            return False
        return permission in self.role_permissions[role]
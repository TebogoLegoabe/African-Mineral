from modules.auth import Authentication

# Test the module
auth = Authentication()

print("Testing Authentication Module...")
print("-" * 50)

# Test login
print("\n1. Testing login with admin...")
result = auth.login('admin', 'admin123')
print(f"Success: {result['success']}")
print(f"User: {result.get('user', {}).get('username')}")
print(f"Role: {result.get('user', {}).get('role')}")

print("\n2. Testing wrong password...")
result = auth.login('admin', 'wrongpass')
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")

print("\n3. Testing permission check...")
has_permission = auth.check_permission('Administrator', 'edit_all')
print(f"Admin can edit: {has_permission}")

has_permission = auth.check_permission('Researcher', 'delete_all')
print(f"Researcher can delete: {has_permission}")

print("\n✓ Tests complete!")
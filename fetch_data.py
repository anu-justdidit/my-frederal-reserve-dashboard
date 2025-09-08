import os
import sys
from pathlib import Path

def check_env_file():
    """Check for existence and contents of environment files"""
    print("🔍 Checking for environment files...")
    
    env_files = ['.env', '.env.local', '.env.development']
    found_files = []
    
    for env_file in env_files:
        if Path(env_file).exists():
            found_files.append(env_file)
            print(f"✅ Found: {env_file}")
            
            # Show first few lines (without sensitive values)
            with open(env_file, 'r') as f:
                lines = f.readlines()[:3]
                print(f"   Sample content: {[line.strip() for line in lines if line.strip() and not line.startswith('#')]}")
        else:
            print(f"❌ Not found: {env_file}")
    
    return found_files

def check_environment_variables():
    """Check if environment variables are loaded"""
    print("\n🔍 Checking environment variables...")
    
    # Common environment variables to check
    common_vars = ['DATABASE_URL', 'API_KEY', 'DEBUG', 'SECRET_KEY']
    
    for var in common_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} is set (value hidden for security)")
        else:
            print(f"❌ {var} is not set")

def check_python_dotenv():
    """Check if python-dotenv is installed and properly used"""
    print("\n🔍 Checking python-dotenv setup...")
    
    try:
        import dotenv
        print("✅ python-dotenv is installed")
        
        # Check if it's being used in the project
        project_files = ['app.py', 'main.py', 'manage.py', 'wsgi.py']
        for file in project_files:
            if Path(file).exists():
                with open(file, 'r') as f:
                    content = f.read()
                    if 'dotenv' in content or 'load_dotenv' in content:
                        print(f"✅ dotenv is referenced in {file}")
                        return
        
        print("⚠️  dotenv is installed but may not be used in project entry points")
        
    except ImportError:
        print("❌ python-dotenv is not installed")
        print("   Install it with: pip install python-dotenv")

def create_sample_env():
    """Create a sample environment file if none exists"""
    if not Path('.env').exists():
        print("\n📝 Creating a sample .env file...")
        with open('.env', 'w') as f:
            f.write("# Environment variables\n")
            f.write("DEBUG=True\n")
            f.write("SECRET_KEY=your-secret-key-here\n")
            f.write("DATABASE_URL=sqlite:///db.sqlite3\n")
            f.write("# API_KEY=your-api-key-here\n")
        print("✅ Created sample .env file")
    else:
        print("\n📝 .env file already exists")

def main():
    print("=" * 50)
    print("Environment Configuration Diagnostic Tool")
    print("=" * 50)
    
    # Check current working directory
    print(f"Current directory: {os.getcwd()}")
    
    # Run checks
    check_env_file()
    check_environment_variables()
    check_python_dotenv()
    
    # Offer to create sample env file
    response = input("\nWould you like to create a sample .env file? (y/n): ")
    if response.lower() == 'y':
        create_sample_env()
    
    print("\n" + "=" * 50)
    print("Next steps:")
    print("1. Make sure your .env file is in the root of your project")
    print("2. Install python-dotenv: pip install python-dotenv")
    print("3. Add this to your main Python file:")
    print("   from dotenv import load_dotenv")
    print("   load_dotenv()")
    print("4. Restart your application after making changes")
    print("=" * 50)

if __name__ == "__main__":
    main()
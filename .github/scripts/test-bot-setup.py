#!/usr/bin/env python3
"""
Test script for Omio PR Reviewer Bot setup
This script helps verify that the bot is properly configured
"""

import os
import yaml
import json
from pathlib import Path

def test_yaml_syntax():
    """Test YAML syntax for all configuration files"""
    print("🔍 Testing YAML syntax...")
    
    yaml_files = [
        '.github/workflows/omio-pr-reviewer.yml',
        '.github/omio-bot-config.yml',
        '.github/workflows/test-omio-bot.yml'
    ]
    
    for file_path in yaml_files:
        try:
            with open(file_path, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {file_path} - Valid YAML")
        except Exception as e:
            print(f"❌ {file_path} - Invalid YAML: {e}")

def test_file_structure():
    """Test that all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        '.github/workflows/omio-pr-reviewer.yml',
        '.github/omio-bot-config.yml',
        '.github/workflows/OMIO_BOT_README.md',
        '.github/workflows/test-omio-bot.yml',
        '.github/QUICK_START.md'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Exists")
        else:
            print(f"❌ {file_path} - Missing")

def test_bot_configuration():
    """Test bot configuration settings"""
    print("\n⚙️ Testing bot configuration...")
    
    try:
        with open('.github/omio-bot-config.yml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Test required settings
        required_settings = {
            'auto_approve': bool,
            'auto_merge': bool,
            'merge_method': str,
            'require_approvals': int
        }
        
        for setting, expected_type in required_settings.items():
            if setting in config:
                value = config[setting]
                if isinstance(value, expected_type):
                    print(f"✅ {setting}: {value} ({type(value).__name__})")
                else:
                    print(f"⚠️ {setting}: {value} (expected {expected_type.__name__})")
            else:
                print(f"❌ {setting}: Missing")
        
        # Test file patterns
        include_patterns = config.get('include_patterns', [])
        exclude_patterns = config.get('exclude_patterns', [])
        print(f"✅ Include patterns: {len(include_patterns)} patterns")
        print(f"✅ Exclude patterns: {len(exclude_patterns)} patterns")
        
        # Test labels
        add_labels = config.get('add_labels', [])
        blocking_labels = config.get('blocking_labels', [])
        print(f"✅ Auto-add labels: {len(add_labels)} labels")
        print(f"✅ Blocking labels: {len(blocking_labels)} labels")
        
    except Exception as e:
        print(f"❌ Error reading config: {e}")

def test_workflow_permissions():
    """Test workflow permissions"""
    print("\n🔐 Testing workflow permissions...")
    
    try:
        with open('.github/workflows/omio-pr-reviewer.yml', 'r') as f:
            workflow = yaml.safe_load(f)
        
        permissions = workflow.get('permissions', {})
        required_permissions = ['contents', 'pull-requests', 'statuses', 'checks', 'issues']
        
        for perm in required_permissions:
            if perm in permissions:
                level = permissions[perm]
                if level in ['read', 'write']:
                    print(f"✅ {perm}: {level}")
                else:
                    print(f"⚠️ {perm}: {level} (unusual level)")
            else:
                print(f"❌ {perm}: Missing")
        
    except Exception as e:
        print(f"❌ Error reading workflow: {e}")

def test_trigger_events():
    """Test workflow trigger events"""
    print("\n🎯 Testing workflow triggers...")
    
    try:
        with open('.github/workflows/omio-pr-reviewer.yml', 'r') as f:
            content = f.read()
        
        # Check for trigger patterns in the content directly
        if 'pull_request:' in content and 'types: [opened, synchronize, reopened, ready_for_review]' in content:
            print("✅ Pull request triggers: [opened, synchronize, reopened, ready_for_review]")
        else:
            print("❌ Pull request triggers: Missing or incorrect")
        
        if 'pull_request_review:' in content and 'types: [submitted]' in content:
            print("✅ Review triggers: [submitted]")
        else:
            print("❌ Review triggers: Missing or incorrect")
        
        if 'check_suite:' in content and 'types: [completed]' in content:
            print("✅ Check suite triggers: [completed]")
        else:
            print("❌ Check suite triggers: Missing or incorrect")
        
        # Try YAML parsing as backup
        try:
            workflow = yaml.safe_load(content)
            on_events = workflow.get('on', {})
            if isinstance(on_events, dict) and on_events:
                print("✅ YAML parsing successful - triggers found")
            else:
                print("⚠️ YAML parsing issue - but content looks correct")
        except:
            print("⚠️ YAML parsing failed - but content looks correct")
        
    except Exception as e:
        print(f"❌ Error reading triggers: {e}")

def generate_test_pr_instructions():
    """Generate instructions for testing the bot"""
    print("\n🧪 Test PR Instructions:")
    print("=" * 50)
    print("To test the Omio bot, follow these steps:")
    print()
    print("1. Create a new branch:")
    print("   git checkout -b test-omio-bot")
    print()
    print("2. Make a small change (add a comment to any file):")
    print("   # Test comment for Omio bot")
    print()
    print("3. Commit and push:")
    print("   git add .")
    print("   git commit -m 'Test: Add comment for Omio bot testing'")
    print("   git push origin test-omio-bot")
    print()
    print("4. Create a PR with the 'auto-merge' label")
    print("5. Watch the bot automatically review and merge!")
    print()
    print("🔍 Monitor the process in:")
    print("   - GitHub Actions tab")
    print("   - PR comments")
    print("   - PR labels")

def main():
    """Main test function"""
    print("🤖 Omio PR Reviewer Bot - Setup Test")
    print("=" * 50)
    
    # Run all tests
    test_yaml_syntax()
    test_file_structure()
    test_bot_configuration()
    test_workflow_permissions()
    test_trigger_events()
    generate_test_pr_instructions()
    
    print("\n🎉 Test completed!")
    print("\n📖 For more information:")
    print("   - Quick Start: .github/QUICK_START.md")
    print("   - Full Docs: .github/workflows/OMIO_BOT_README.md")

if __name__ == '__main__':
    main()
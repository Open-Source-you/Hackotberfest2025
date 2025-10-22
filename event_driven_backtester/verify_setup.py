"""
Setup verification script for the event-driven backtesting engine.
Run this to ensure everything is properly installed and configured.
"""

import sys
import os


def check_python_version():
    """Check if Python version is 3.7 or higher."""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("  ⚠️  Warning: Python 3.7+ recommended")
        return False
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required = ['pandas', 'numpy']
    optional = ['matplotlib']
    
    missing_required = []
    missing_optional = []
    
    print("\nChecking required dependencies:")
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package} installed")
        except ImportError:
            print(f"  ✗ {package} NOT installed")
            missing_required.append(package)
    
    print("\nChecking optional dependencies:")
    for package in optional:
        try:
            __import__(package)
            print(f"  ✓ {package} installed")
        except ImportError:
            print(f"  ⚠️  {package} NOT installed (visualization will not work)")
            missing_optional.append(package)
    
    if missing_required:
        print(f"\n⚠️  Missing required packages: {', '.join(missing_required)}")
        print(f"   Install with: pip install {' '.join(missing_required)}")
        return False
    
    return True


def check_file_structure():
    """Check if all required files are present."""
    required_files = [
        '__init__.py',
        'events.py',
        'data_handler.py',
        'strategy.py',
        'portfolio.py',
        'execution.py',
        'backtest.py',
        'config.py',
        'generate_sample_data.py',
        'run_backtest.py',
        'README.md',
    ]
    
    print("\nChecking file structure:")
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} NOT FOUND")
            all_present = False
    
    return all_present


def check_data_directory():
    """Check if data directory exists and contains sample data."""
    print("\nChecking data directory:")
    if not os.path.exists('data'):
        print("  ⚠️  'data' directory not found")
        print("     Run: python generate_sample_data.py")
        return False
    
    print("  ✓ 'data' directory exists")
    
    sample_files = ['AAPL.csv', 'MSFT.csv', 'GOOG.csv']
    missing = []
    for file in sample_files:
        path = os.path.join('data', file)
        if os.path.exists(path):
            print(f"  ✓ {file} found")
        else:
            print(f"  ⚠️  {file} not found")
            missing.append(file)
    
    if missing:
        print(f"\n  ⚠️  Sample data missing: {', '.join(missing)}")
        print("     Run: python generate_sample_data.py")
        return False
    
    return True


def check_import_modules():
    """Try importing the main modules."""
    print("\nTesting module imports:")
    modules = [
        'events',
        'data_handler',
        'strategy',
        'portfolio',
        'execution',
        'backtest'
    ]
    
    all_imported = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module} imports successfully")
        except Exception as e:
            print(f"  ✗ {module} import failed: {e}")
            all_imported = False
    
    return all_imported


def run_quick_test():
    """Run a quick functionality test."""
    print("\nRunning quick functionality test:")
    try:
        from events import MarketEvent, SignalEvent, OrderEvent, FillEvent
        import datetime
        import queue
        
        # Test event creation
        me = MarketEvent()
        se = SignalEvent('TEST', datetime.datetime.now(), 'LONG', 1.0)
        oe = OrderEvent('TEST', 'MKT', 100, 'BUY')
        fe = FillEvent(datetime.datetime.now(), 'TEST', 'SIM', 100, 'BUY', 10000.0)
        
        print("  ✓ Event objects created successfully")
        
        # Test event queue
        q = queue.Queue()
        q.put(me)
        q.put(se)
        event = q.get(False)
        
        print("  ✓ Event queue working")
        print("  ✓ All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("="*60)
    print("Event-Driven Backtesting Engine - Setup Verification")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Data Directory", check_data_directory),
        ("Module Imports", check_import_modules),
        ("Quick Test", run_quick_test),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("Verification Summary:")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:.<30} {status}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to run backtests!")
        print("\nNext steps:")
        print("  1. Review README.md for documentation")
        print("  2. Run: python run_backtest.py")
        print("  3. Check QUICKSTART.md for examples")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install pandas numpy")
        print("  - Generate sample data: python generate_sample_data.py")
        print("  - Check you're in the right directory")
    
    print("\n" + "="*60)
    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

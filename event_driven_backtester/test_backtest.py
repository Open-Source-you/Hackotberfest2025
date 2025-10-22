"""
Basic tests for the event-driven backtesting engine.
"""

import unittest
import datetime
import queue
from events import MarketEvent, SignalEvent, OrderEvent, FillEvent


class TestEvents(unittest.TestCase):
    """Test event creation and attributes."""
    
    def test_market_event(self):
        """Test MarketEvent creation."""
        event = MarketEvent()
        self.assertEqual(event.type, 'MARKET')
    
    def test_signal_event(self):
        """Test SignalEvent creation."""
        dt = datetime.datetime(2023, 1, 1)
        event = SignalEvent('AAPL', dt, 'LONG', 1.0)
        self.assertEqual(event.type, 'SIGNAL')
        self.assertEqual(event.symbol, 'AAPL')
        self.assertEqual(event.signal_type, 'LONG')
        self.assertEqual(event.strength, 1.0)
    
    def test_order_event(self):
        """Test OrderEvent creation."""
        event = OrderEvent('AAPL', 'MKT', 100, 'BUY')
        self.assertEqual(event.type, 'ORDER')
        self.assertEqual(event.symbol, 'AAPL')
        self.assertEqual(event.order_type, 'MKT')
        self.assertEqual(event.quantity, 100)
        self.assertEqual(event.direction, 'BUY')
    
    def test_fill_event(self):
        """Test FillEvent creation."""
        dt = datetime.datetime(2023, 1, 1)
        event = FillEvent(dt, 'AAPL', 'SIMULATED', 100, 'BUY', 10000.0)
        self.assertEqual(event.type, 'FILL')
        self.assertEqual(event.symbol, 'AAPL')
        self.assertEqual(event.quantity, 100)
        self.assertIsNotNone(event.commission)
    
    def test_fill_event_commission(self):
        """Test commission calculation."""
        dt = datetime.datetime(2023, 1, 1)
        event = FillEvent(dt, 'AAPL', 'SIMULATED', 100, 'BUY', 10000.0)
        # Commission should be max(1.0, 0.005 * 100) = 1.0
        self.assertEqual(event.commission, 1.0)
        
        event2 = FillEvent(dt, 'AAPL', 'SIMULATED', 1000, 'BUY', 100000.0)
        # Commission should be max(1.0, 0.005 * 1000) = 5.0
        self.assertEqual(event2.commission, 5.0)


class TestEventQueue(unittest.TestCase):
    """Test event queue functionality."""
    
    def test_event_queue(self):
        """Test adding and retrieving events from queue."""
        events = queue.Queue()
        
        # Add events
        events.put(MarketEvent())
        events.put(SignalEvent('AAPL', datetime.datetime.now(), 'LONG', 1.0))
        
        # Retrieve events
        event1 = events.get(False)
        self.assertEqual(event1.type, 'MARKET')
        
        event2 = events.get(False)
        self.assertEqual(event2.type, 'SIGNAL')
        
        # Queue should be empty
        self.assertTrue(events.empty())


if __name__ == '__main__':
    print("Running Event-Driven Backtester Tests...")
    print("="*60)
    unittest.main(verbosity=2)

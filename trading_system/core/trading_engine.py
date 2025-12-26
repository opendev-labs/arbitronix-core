import pandas as pd
import time
from datetime import datetime

def main():
    print("🚀 Starting Trading Engine...")
    
    # Import components
    from market.data_fetcher import DataFetcher
    from market.analytics import Analytics
    from strategies.mean_reversion import MeanReversionStrategy
    from risk.risk_manager import RiskManager
    from execution.paper_broker import PaperBroker
    
    # Initialize components
    print("Initializing components...")
    fetcher = DataFetcher()
    strategy = MeanReversionStrategy()
    risk = RiskManager()
    broker = PaperBroker(initial_balance=10000)
    
    # Main trading loop
    print("\nStarting trading loop...")
    print("-" * 50)
    
    symbols = ['BTCUSDT', 'ETHUSDT']
    
    for i in range(5):  # Run 5 iterations for demo
        print(f"\n📊 Iteration {i+1} - {datetime.now().strftime('%H:%M:%S')}")
        
        for symbol in symbols:
            # Get market data
            data = fetcher.get_mock_data(symbol, periods=100)
            latest_price = data['close'].iloc[-1]
            
            # Run strategy
            signal = strategy.analyze(symbol, data['close'])
            
            print(f"\n{symbol}:")
            print(f"  Price: ${latest_price:.2f}")
            print(f"  Z-score: {signal['zscore']:.2f}")
            print(f"  Regime: {signal['regime']}")
            print(f"  Action: {signal['action']}")
            print(f"  Reason: {signal['reason']}")
            
            if signal['action'] != 'hold':
                # Calculate position size
                balance = broker.get_balance()['total']
                position_size = strategy.calculate_position_size(signal, balance)
                
                # Risk check
                risk_check = risk.check_trade(signal, position_size, balance)
                
                if risk_check['approved']:
                    # Execute trade
                    amount = position_size / latest_price
                    result = broker.place_order(
                        symbol, signal['side'], amount, latest_price
                    )
                    
                    if result['success']:
                        print(f"  ✅ Executed: {signal['side']} {amount:.4f} {symbol}")
                        # Update risk manager
                        risk.update_position(symbol, {
                            'side': signal['side'],
                            'amount': amount,
                            'entry_price': latest_price
                        })
                    else:
                        print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
                else:
                    print(f"  ⚠️  Blocked by risk: {risk_check['reason']}")
        
        # Show portfolio status
        print(f"\n📈 Portfolio Status:")
        print(f"  Cash: ${broker.balance['USDT']:.2f}")
        print(f"  Positions: {len(broker.positions)}")
        
        if broker.positions:
            for sym, pos in broker.positions.items():
                print(f"    {sym}: {pos['amount']:.4f} @ ${pos['entry_price']:.2f}")
        
        print("-" * 50)
        time.sleep(2)  # Wait before next iteration
    
    print("\n✅ Trading session complete!")
    print(f"Final balance: ${broker.balance['USDT']:.2f}")
    print(f"Total trades: {len(broker.orders)}")

if __name__ == "__main__":
    main()

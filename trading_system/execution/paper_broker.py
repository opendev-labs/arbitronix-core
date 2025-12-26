import pandas as pd

class PaperBroker:
    def __init__(self, initial_balance=100000):
        self.balance = {'USDT': initial_balance}
        self.positions = {}
        self.orders = []
    
    def place_order(self, symbol, side, amount, price):
        cost = amount * price
        
        if side == 'buy':
            if self.balance['USDT'] < cost:
                return {'success': False, 'error': 'Insufficient balance'}
            
            self.balance['USDT'] -= cost
            if symbol in self.positions:
                self.positions[symbol]['amount'] += amount
            else:
                self.positions[symbol] = {'amount': amount, 'entry_price': price}
        
        elif side == 'sell':
            if symbol not in self.positions or self.positions[symbol]['amount'] < amount:
                return {'success': False, 'error': 'No position to sell'}
            
            self.balance['USDT'] += cost
            self.positions[symbol]['amount'] -= amount
            if self.positions[symbol]['amount'] <= 0:
                del self.positions[symbol]
        
        order = {
            'symbol': symbol,
            'side': side,
            'amount': amount,
            'price': price,
            'timestamp': pd.Timestamp.now()
        }
        self.orders.append(order)
        
        return {'success': True, 'order': order}
    
    def get_balance(self):
        total = self.balance['USDT']
        return {'USDT': self.balance['USDT'], 'total': total}

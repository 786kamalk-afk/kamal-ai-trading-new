from order_execution.paper_adapter import PaperBroker
from order_execution.broker_base import OrderRequest

def test_paper_place_order():
    b = PaperBroker()
    req = OrderRequest(client_order_id='c1', symbol='AAPL', qty=10, side='BUY', type='MARKET', price=100)
    resp = b.place_order(req)
    assert resp.status == 'FILLED'
    assert resp.filled_qty == 10

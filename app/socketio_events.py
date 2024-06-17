from flask_socketio import Namespace, emit
from app.models import Inventory
from app import socketio


class InventoryNamespace(Namespace):
    def on_connect(self):
        print('Client connected')

    def on_disconnect(self):
        print('Client disconnected')

    def on_update_inventory(self, data):
        # Assuming data contains {'product_id': 1, 'quantity': 5}
        product_id = data['product_id']
        quantity = data['quantity']
        inventory = Inventory.query.filter_by(product_id=product_id).first()
        if inventory:
            inventory.quantity = quantity
            db.session.commit()
            emit('inventory_update', {'product_id': product_id, 'quantity': quantity}, broadcast=True)

socketio.on_namespace(InventoryNamespace('/inventory'))
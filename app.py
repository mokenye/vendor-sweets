from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Vendor, Sweet, VendorSweet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/') 
def home(): 
    return 'VENDORS, SWEETS, VENDOR_SWEETS'

@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    response = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
    return jsonify(response)

@app.route('/vendors/<int:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    if vendor:
        vendor_data = {'id': vendor.id, 'name': vendor.name}
        vendor_sweets = [{'id': vs.id, 'price': vs.price, 'sweet': {'id': vs.sweet.id, 'name': vs.sweet.name},
                          'sweet_id': vs.sweet_id, 'vendor_id': vs.vendor_id} for vs in vendor.vendor_sweets]
        vendor_data['vendor_sweets'] = vendor_sweets
        return jsonify(vendor_data)
    else:
        return jsonify({'error': 'Vendor not found'}), 404

@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    response = [{'id': sweet.id, 'name': sweet.name} for sweet in sweets]
    return jsonify(response)

@app.route('/sweets/<int:sweet_id>', methods=['GET'])
def get_sweet(sweet_id):
    sweet = Sweet.query.get(sweet_id)
    if sweet:
        return jsonify({'id': sweet.id, 'name': sweet.name})
    else:
        return jsonify({'error': 'Sweet not found'}), 404

@app.route('/vendor_sweets', methods=['POST'])
def add_vendor_sweet():
    data = request.json
    price = data.get('price')
    vendor_id = data.get('vendor_id')
    sweet_id = data.get('sweet_id')

    if not all([price, vendor_id, sweet_id]):
        return jsonify({'error': 'Missing data'}), 400

    try:
        price = int(price)
        if price < 0:
            raise ValueError("Price can't be negative number")
    except ValueError:
        return jsonify({'error': 'Price must be a non-negative integer'}), 400

    vendor = Vendor.query.get(vendor_id)
    sweet = Sweet.query.get(sweet_id)

    if not vendor or not sweet:
        return jsonify({'error': 'Invalid vendor_id or sweet_id'}), 400

    vendor_sweet = VendorSweet(price=price, vendor_id=vendor_id, sweet_id=sweet_id)
    db.session.add(vendor_sweet)
    db.session.commit()

    response_data = {
        'id': vendor_sweet.id,
        'price': vendor_sweet.price,
        'sweet': {'id': sweet.id, 'name': sweet.name},
        'sweet_id': sweet_id,
        'vendor': {'id': vendor.id, 'name': vendor.name},
        'vendor_id': vendor_id
    }

    return jsonify(response_data), 201


@app.route('/vendor_sweets/<int:vendor_sweet_id>', methods=['DELETE'])
def delete_vendor_sweet(vendor_sweet_id):
    vendor_sweet = VendorSweet.query.get(vendor_sweet_id)
    if vendor_sweet:
        db.session.delete(vendor_sweet)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'VendorSweet not found'}), 404
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)

#testing git
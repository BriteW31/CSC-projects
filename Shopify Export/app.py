from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# This completely resolves the browser CORS error
# It allows your Angular app (localhost:4200) to talk to this Python app
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/remove-locations', methods=['POST'])
def remove_locations():
    data = request.get_json()
    
    if not data or 'items' not in data or 'credentials' not in data:
        return jsonify({"error": "Invalid payload. Missing items or credentials."}), 400

    # Extract dynamic credentials
    creds = data['credentials']
    store_url = creds.get('storeUrl')
    access_token = creds.get('accessToken')
    api_version = creds.get('apiVersion', '2024-01')

    if not store_url or not access_token:
        return jsonify({"error": "Missing store URL or Access Token in payload."}), 400

    items_to_process = data['items']
    success_count = 0
    errors = []

    # Use the dynamic access token for the headers
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    for item in items_to_process:
        inventory_item_id = item.get('inventoryItemId')
        location_id = item.get('locationId')

        if not inventory_item_id or not location_id:
            continue

        # Use the dynamic store URL and API version for the endpoint
        url = f"https://{store_url}/admin/api/{api_version}/locations/{location_id}/inventory_levels.json?inventory_item_id={inventory_item_id}"

        try:
            response = requests.delete(url, headers=headers)
            
            if response.status_code == 204 or response.status_code == 200:
                success_count += 1
            else:
                errors.append(f"Failed item {inventory_item_id}: {response.text}")
                
        except Exception as e:
            errors.append(f"Network error on item {inventory_item_id}: {str(e)}")

    return jsonify({
        "message": f"Successfully processed {success_count} items.",
        "success_count": success_count,
        "errors": errors
    }), 200

if __name__ == '__main__':
    # Runs the server on port 5000 by default
    app.run(debug=True, port=5000)

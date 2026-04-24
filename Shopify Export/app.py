from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)


# Allows your Angular app (localhost:4200) to reach this Python app
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def health_check():
    """
    A simple endpoint for UptimeRobot to ping to verify the server is alive.
    """
    return "Backend proxy is awake and running!", 200

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """
    Tests the Shopify credentials by making a safe, read-only 
    request to fetch the store's basic profile.
    """
    data = request.get_json()
    
    if not data or 'storeUrl' not in data or 'accessToken' not in data:
        return jsonify({"error": "Missing credentials in request."}), 400

    # Clean up the inputs just like we do for the main sync
    store_url = data['storeUrl'].replace('https://', '').strip()
    access_token = data['accessToken'].strip()
    api_version = data.get('apiVersion', '2024-01').strip()

    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }

    # The safest read-only endpoint in Shopify
    url = f"https://{store_url}/admin/api/{api_version}/shop.json"

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            shop_data = response.json().get('shop', {})
            store_name = shop_data.get('name', 'your store')
            return jsonify({"message": f"Success! Connected securely to {store_name}."}), 200
        else:
            return jsonify({"error": f"Auth Failed ({response.status_code}): Check your token and URL."}), 401
            
    except Exception as e:
        return jsonify({"error": f"Network error: Could not reach Shopify. {str(e)}"}), 500

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


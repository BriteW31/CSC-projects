from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)

# This completely resolves the browser CORS error
# It allows your Angular app (localhost:4200) to talk to this Python app
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- SECURITY WARNING ---
# In a production environment, NEVER hardcode these! 
# Load them from environment variables (e.g., using python-dotenv)
# Modify the variables below to be based on your Shopify link:
SHOPIFY_STORE_URL = ""
SHOPIFY_ACCESS_TOKEN = ""
API_VERSION = ""

@app.route('/api/remove-locations', methods=['POST'])
def remove_locations():
    """
    Receives the parsed CSV array from Angular and processes 
    the location deletions via the Shopify API.
    """
    data = request.get_json()
    
    if not data or 'items' not in data:
        return jsonify({"error": "Invalid payload. Expected an 'items' array."}), 400

    items_to_process = data['items']
    success_count = 0
    errors = []

    # Set up the secure headers for Shopify
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    # Loop through the exact items Angular extracted
    for item in items_to_process:
        inventory_item_id = item.get('inventoryItemId')
        location_id = item.get('locationId')

        if not inventory_item_id or not location_id:
            continue

        # The specific Shopify endpoint to sever the location tie
        url = f"https://{SHOPIFY_STORE_URL}/admin/api/{API_VERSION}/locations/{location_id}/inventory_levels.json?inventory_item_id={inventory_item_id}"

        try:
            response = requests.delete(url, headers=headers)
            
            # 204 No Content is Shopify's successful delete response
            if response.status_code == 204 or response.status_code == 200:
                success_count += 1
            else:
                errors.append(f"Failed item {inventory_item_id}: {response.text}")
                
        except Exception as e:
            errors.append(f"Network error on item {inventory_item_id}: {str(e)}")

    # Report back to Angular
    return jsonify({
        "message": f"Successfully processed {success_count} items.",
        "success_count": success_count,
        "errors": errors
    }), 200

if __name__ == '__main__':
    # Runs the server on port 5000 by default
    app.run(debug=True, port=5000)


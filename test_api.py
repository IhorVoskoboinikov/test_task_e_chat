from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/endpoint', methods=['POST'])
def receive_post_request():
    try:
        data = request.get_json()
        print(f"Received POST request with data: {data}")

        return jsonify({'status': 'success', 'message': 'Data received successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)


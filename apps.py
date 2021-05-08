from flask.app import Flask, request, jsonify
import concurrent.futures
from services import p_service, a_service, d_service

apps_app = Flask('apps_app')

def start_apps_app():
    print("starting apps_app")
    apps_app.run(port=8082, debug=True)

@apps_app.route('/api/apps', methods = ['POST', 'GET'])
def get_app():
    if request.method == 'POST':
        app_name = request.form.get('appName')
        p_name = request.form.get('platformName')
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            p_future = executor.submit(p_service.fetch, p_name)
            print(p_future.result())
            d_future = executor.submit(d_service.fetch, request.form.get('developerName'))
            d_bio = d_future.result()
    
        app_id = a_service.fetch(app_name, p_name, d_bio)
        data = {'appName' : app_name, 'appId' : app_id}
        return jsonify(data)
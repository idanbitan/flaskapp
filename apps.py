from flask.app import Flask, request, jsonify
from services import a_service, d_service
import concurrent.futures
import requests

apps_app = Flask('apps_app')


def start_apps_app():
    print("starting apps_app")
    apps_app.run(port=8081, debug=True)


def request_platform(plat_name):
    # We Will Use Our previous api to fetch the platform
    response = requests.post('http://127.0.0.1:8082/api/platforms', data={'platformName': plat_name})
    return response.json()['platformId']


@apps_app.route('/api/apps', methods=['POST', 'GET'])
def get_app():
    if request.method == 'POST':
        app_name = request.form.get('appName')
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            p_future = executor.submit(
                request_platform, request.form.get('platformName'))
            d_future = executor.submit(
                d_service.fetch, request.form.get('developerName'))
            p_id = p_future.result()
            d_bio = d_future.result()

        app_id = a_service.fetch(app_name, p_id, d_bio)
        data = {'appName': app_name, 'appId': app_id}
        return jsonify(data)
    if request.method == 'GET':
        data = {}
        count = 0
        for app_name, app_id in a_service.get_all:
            # Count Only To differ between apps
            count += 1
            data[count] = {'appName': app_name, 'appId': app_id}
        return jsonify(data)

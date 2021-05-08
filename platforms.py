from flask.app import Flask, request, jsonify
from flask import abort
from services import p_service

platforms_app = Flask('platforms_app')


def start_platforms_app():
    print("starting platforms_app")
    platforms_app.run(port=8081)


@platforms_app.route('/api/platforms/<platformName>', methods=['GET'])
def plat_name(platformName):
    p_id = p_service.get(platformName)
    if p_id == 0:
        abort(404)
    data = {'platformName': platformName, 'platformId': p_id}
    return jsonify(data)


@platforms_app.route('/api/platforms', methods=['POST'])
def add_plat():
    p_name = request.form.get('platformName')
    if p_name is None:
        abort(400)
    p_id = p_service.fetch(p_name)
    data = {'platformName': p_name, 'platformId': p_id}
    return jsonify(data)

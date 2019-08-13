from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from pprint import pprint
# from server import db
from . import api
from ..chat.events import bot
import json


@api.route('/weights/targets', methods=['GET'])
def get_weight_target():
    return jsonify(bot.get_weights_target())

@api.route('/transition_features',methods=['GET'])
def get_transition_features():
    return jsonify(bot.get_transition_features())
@api.route('/csv/attribute',methods=['GET'])
def create_csv_attribute():
    bot.create_csv_attribute()
    return 'GENERATE CSV ATTRIBUTE SUCCESS'
@api.route('/csv/state_features', methods=['GET'])
def create_state_features_csv():
    bot.create_state_features_csv()
    return 'GENERATE CSV STATE FEATURES SUCCESS'
@api.route('/csv/transition_features', methods=['GET'])
def create_transition_features_csv():
    bot.create_transition_features_csv()
    return 'GENERATE CSV TRANSITION FEATURES SUCCESS'

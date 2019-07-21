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

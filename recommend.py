# from django.shortcuts import render
from flask import Flask, render_template, request, Blueprint
import datetime, pymysql
import simRecommend_zsf
# from django.http import JsonResponse
import json
app = Blueprint("recommend", __name__)
@app.route("/recommend")
def recommend():
    scholarID = request.args.get('user')
    print(scholarID)
    recommend_list = simRecommend_zsf.scholar_Recommend(str(scholarID))
    print(recommend_list)
    text = json.dumps(recommend_list,ensure_ascii=False)
    return text

@app.route("/refresh")
def refresh():
    scholarID = request.args.get('user')
    type = request.args.get('type')
    print(int(type))
    recommend_list = simRecommend_zsf.scholar_Recommend(str(scholarID),int(type))
    print(recommend_list)
    text = json.dumps(recommend_list,ensure_ascii=False)
    return text

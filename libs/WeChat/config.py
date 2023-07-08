# coding: utf-8
from libs.utils import db

token = "YDDn6qd4LDImnn44PMl4dQzIPZQvDn00"
WC_CONFIG = {x.id: x for x in db.default.wx_app.filter(platform='dev')}

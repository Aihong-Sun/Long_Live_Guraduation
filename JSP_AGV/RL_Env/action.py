
from JSP_AGV.PDR import *

def action_translator(a,SF):
    JS_action=a%7
    VS_action=int(a/7)
    Ji=JS_set[JS_action](SF)
    agvi=VS_set[VS_action](SF,Ji)
    return Ji,agvi
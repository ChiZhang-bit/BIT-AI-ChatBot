# -*- coding:utf-8 -*-


from matcher.rulesMapper import get_rules


def add_rules():
    mybot = get_rules()
    return mybot

def match(inputs_seg, mybot):
    return mybot.respond(inputs_seg)

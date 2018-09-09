#!/usr/bin/python3
# _*_ coding: utf-8 _*_

import sys
from bfcm.logic import ConfigLogic
from bfcm.logic import ContentLogic
from bfcm.logic import DatabaseLogic
from bfcm.logic import TrainLogic

class Commander:

    def __init__(self, cm):
        self._cm = cm

    def execute(self, command, args):
        self._easy_check(command)
        if 'init' == command:
            self._setup()
        elif 'dump' == command:
            self._dump()
        elif 'train' == command:
            if len(args) < 1:
                sys.stderr.write('サブコマンドの引数が足りません:%s %s\n' % (command, 'mail_directory_name'))
                sys.exit(3)
            self._easy_check(args[0])
            self._imp(args[0])
            mpssid = self._cm.get_mail_profile_set_sid(args[0])
            self._train(mpssid)
        elif 'prob' == command:
            if len(args) < 3:
                sys.stderr.write('サブコマンドの引数が足りません:%s %s %s %s\n' % (command, 'mail_directory_name', 'message', 'category'))
                sys.exit(3)
            self._easy_check(args[0])
            self._easy_check(args[2])
            msid = self._cm.get_model_sid(args[0])
            self._prob(msid, args[1], args[2])
        elif 'dumpmeasurableset' == command:
            if len(args) < 2:
                sys.stderr.write('サブコマンドの引数が足りません:%s %s %s\n' % (command, 'mail_directory_name', 'message'))
                sys.exit(3)
            self._easy_check(args[0])
            msid = self._cm.get_model_sid(args[0])
            self._dump_measurable_set(msid, args[1])
        else:
            sys.stderr.write('未定義のサブコマンドです: %s\n' % command)
            sys.exit(3)

    def _easy_check(self, s):
        cc = self._cm.get_invalid_chars().split(' ')
        flag = False
        if ' ' in s:
            flag = True
        for c in cc:
            if c in s:
                flag = True
                break
        if flag:
            sys.stderr.write('不正な引数です: %s\n' % s)
            sys.exit(3)

    def _setup(self):
        dg = DatabaseLogic(self._cm)
        dg.create_tables()

    def _dump(self):
        dg = DatabaseLogic(self._cm)
        dg.dump()

    def _imp(self, name):
        cg = ContentLogic(self._cm)
        mps = cg.create_mail_profile_set(name)
        dg = DatabaseLogic(self._cm)
        dg.insert_mail_profile_set(mps)

    def _train(self, mpssid):
        dg = DatabaseLogic(self._cm)
        tg = TrainLogic(self._cm)
        mps = dg.create_mail_profile_set(mpssid)
        model = tg.create_model(mps)
        dg.insert_model(model)

    def _dump_measurable_set(self, msid, message):
        dg = DatabaseLogic(self._cm)
        tg = TrainLogic(self._cm)
        model = dg.create_model(msid)
        ms = tg.create_measurable_set(model, message)
        print(tg.dump_measurable_set(ms))

    def _prob(self, msid, message, category):
        dg = DatabaseLogic(self._cm)
        tg = TrainLogic(self._cm)
        model = dg.create_model(msid)
        ms = tg.create_measurable_set(model, message)
        print(tg.prob(model, ms, category))

#!/usr/bin/python3

import os
import codecs
import json
import csv
import sqlite3
from collections import defaultdict
import re
from bfcm.data import ConfigManager
from bfcm.data import ContentProfile
from bfcm.data import Event
from bfcm.data import MailProfile
from bfcm.data import MailProfileSet
from bfcm.data import MeasurableSet
from bfcm.data import Model
from bfcm.data import Probability
from bfcm.data import ProbabilitySpace
from bfcm.data import Sample
from bfcm.data import SampleSpace

class ConfigLogic:

    def create_config_manager(self, config_path):
        with codecs.open(config_path, 'r', 'utf-8') as fd:
            conf_dict = json.load(fd)
            return ConfigManager(conf_dict)

class ContentLogic:

    def __init__(self, cm):
        self._cm = cm

    def create_mail_profile_set(self, name):
        judge_path = self._cm.get_judge_path(name)
        with codecs.open(judge_path, 'r', 'utf-8') as fd:
            judge_reader = csv.reader(fd, delimiter='\t')
            i = 1
            col = []
            for row in judge_reader:
                mpsid = self._cm.get_mail_profile_sid(name, i)
                cpsid = self._cm.get_content_profile_sid(name, i)
                path = self._cm.get_content_path(name, row[0])
                cp = ContentProfile(cpsid, path)
                mp = MailProfile(mpsid, row[1], cp)
                col.append(mp)
                i = i + 1
        mpssid = self._cm.get_mail_profile_set_sid(name)
        return MailProfileSet(mpssid, col)

class DatabaseLogic:

    def __init__(self, cm):
        self._cm = cm

    def dump(self):
        conn = sqlite3.connect(self._cm.get_database_path())
        for row in conn.execute("select * from sqlite_master where type = 'table'"):
            print(row)
        for row in conn.execute("select * from attribute_relations"):
            print('attribute_relations %s' % str(row))
        for row in conn.execute("select * from content_profiles"):
            print('content_profiles %s' % str(row))
        for row in conn.execute("select * from mail_profiles"):
            print('mail_profiles %s' % str(row))
        for row in conn.execute("select * from mail_profile_sets"):
            print('mail_profiles_sets %s' % str(row))
        for row in conn.execute("select * from models"):
            print('models %s' % str(row))
        for row in conn.execute("select * from samples"):
            print('samples %s' % str(row))
        for row in conn.execute("select * from sample_spaces"):
            print('sample_spaces %s' % str(row))
        for row in conn.execute("select * from events"):
            print('events %s' % str(row))
        for row in conn.execute("select * from probability_spaces"):
            print('probability_spaces %s' % str(row))
        for row in conn.execute("select * from probabilities"):
            print('probabilities %s' % str(row))
        conn.close()

    def create_tables(self):
        conn = sqlite3.connect(self._cm.get_database_path())
        conn.executescript(self.read_sql('createtables.sql'))
        conn.close()

    def insert_mail_profile_set(self, mps):
        conn = sqlite3.connect(self._cm.get_database_path())
        conn.execute(self.read_sql('insert1.sql') % 'mail_profile_sets', (mps.get_sid(),))
        for mp in mps.get_mail_profile_list():
            conn.execute(self.read_sql('insert2.sql') % 'mail_profiles', (mp.get_sid(), mp.get_judge()))
            cp = mp.get_content_profile()
            conn.execute(self.read_sql('insert2.sql') % 'content_profiles', (cp.get_sid(), cp.get_path()))
            conn.execute(self.read_sql('insert2.sql') % 'attribute_relations', (mp.get_sid(), cp.get_sid()))
            conn.execute(self.read_sql('insert2.sql') % 'attribute_relations', (mps.get_sid(), mp.get_sid()))
        conn.commit()
        conn.close()
        return 0

    def insert_model(self, model):
        conn = sqlite3.connect(self._cm.get_database_path())
        conn.execute(self.read_sql('insert1.sql') % 'models', (model.get_sid(),))
        ss = model.get_sample_space()
        conn.execute(self.read_sql('insert1.sql') % 'sample_spaces', (ss.get_sid(),))
        conn.execute(self.read_sql('insert2.sql') % 'attribute_relations', (model.get_sid(), ss.get_sid()))
        sc = ss.get_sample_list()
        for s in sc:
            conn.execute(self.read_sql('insert2.sql') % 'samples', (s.get_sid(),s.get_word()))
            conn.execute(self.read_sql('insert2.sql') % 'attribute_relations', (ss.get_sid(), s.get_sid()))
        es = model.get_probability_space()
        conn.execute(self.read_sql('insert2.sql') % 'probability_spaces', (es.get_sid(), es.get_cardinality()))
        conn.execute(self.read_sql('insert2.sql') % 'attribute_relations', (model.get_sid(), es.get_sid()))
        p = model.get_probability()
        conn.execute(self.read_sql('insert1.sql') % 'probabilities', (p.get_sid(),))
        conn.execute(self.read_sql('insert2.sql') % 'attribute_relations', (model.get_sid(), p.get_sid()))
        ec = p.get_event_list()
        for e in ec:
            conn.execute(self.read_sql('insert2.sql') % 'events', (e.get_sid(), json.dumps(e.get_value_dict())))
            conn.execute(self.read_sql('insert2.sql') % 'attribute_relations', (p.get_sid(), e.get_sid()))
        conn.commit()
        conn.close()

    def create_mail_profile_set(self, mpssid):
        conn = sqlite3.connect(self._cm.get_database_path())
        results = conn.execute(self.read_sql('selectattributes.sql'), (mpssid,))
        col = []
        for result in results:
            results2 = conn.execute(self.read_sql('selectbysid.sql') % 'mail_profiles', (result[1],))
            for result2 in results2:
                results3 = conn.execute(self.read_sql('selectattributes.sql'), (result2[0],))
                for result3 in results3:
                    results4 = conn.execute(self.read_sql('selectbysid.sql') % 'content_profiles', (result3[1],))
                    for result4 in results4:
                        cp = ContentProfile(result4[0], result4[1])
                        mp = MailProfile(result2[0], result2[1], cp)
                        col.append(mp)
        return MailProfileSet(mpssid, col)

    def create_model(self, msid):
        s = self._create_sample_space(msid)
        e = self._create_probability_space(msid)
        p = self._create_probability(msid)
        return Model(msid, s, e, p)

    def _create_probability(self, msid):
        conn = sqlite3.connect(self._cm.get_database_path())
        results = conn.execute(self.read_sql('selectattributes.sql'), (msid,))
        for result in results:
            if 'PR' != result[1][:2]:
                continue
            prc = conn.execute(self.read_sql('selectbysid.sql') % 'probabilities', (result[1],))
            for pr in prc:
                vrc = conn.execute(self.read_sql('selectattributes.sql'), (pr[0],))
                col = []
                for vr in vrc:
                    wrc = conn.execute(self.read_sql('selectbysid.sql') % 'events', (vr[1],))
                    for wr in wrc:
                        col.append(Event(wr[0], json.loads(wr[1])))
                return Probability(pr[0], col)

    def _create_probability_space(self, msid):
        conn = sqlite3.connect(self._cm.get_database_path())
        results = conn.execute(self.read_sql('selectattributes.sql'), (msid,))
        for result in results:
            if 'EV' != result[1][:2]:
                continue
            erc = conn.execute(self.read_sql('selectbysid.sql') % 'probability_spaces', (result[1],))
            for er in erc:
                return ProbabilitySpace(er[0], int(er[1]))

    def _create_sample_space(self, msid):
        conn = sqlite3.connect(self._cm.get_database_path())
        results = conn.execute(self.read_sql('selectattributes.sql'), (msid,))
        for result in results:
            if 'SM' != result[1][:2]:
                continue
            src = conn.execute(self.read_sql('selectbysid.sql') % 'sample_spaces', (result[1],))
            for sr in src:
                trc = conn.execute(self.read_sql('selectattributes.sql'), (sr[0],))
                col = []
                for tr in trc:
                    urc = conn.execute(self.read_sql('selectbysid.sql') % 'samples', (tr[1],))
                    for ur in urc:
                        col.append(Sample(ur[0], ur[1]))
                return SampleSpace(sr[0], col)

    def read_sql(self, sql_name):
        sql_path = self._cm.get_sql_path(sql_name)
        with codecs.open(sql_path , 'r', 'utf-8') as fd:
            return fd.read()

class TrainLogic:

    def __init__(self, cm):
        self._cm = cm

    def create_model(self, mps):
        name = mps.get_sid()[3:]
        wc = self._create_word_list(mps)
        s = self._create_sample_space(name, wc)
        e = self._create_probability_space(name, wc)
        ec = self._create_event_list(name, mps, wc)
        p = self._create_probability(name, ec)
        sid = self._cm.get_model_sid(name)
        return Model(sid, s, e, p)

    def create_measurable_set(self, model, message):
        sc = model.get_sample_space().get_sample_list()
        jd = self._cm.get_judge_word()
        vd = defaultdict(int)
        for s in sc:
            w = s.get_word()
            if not (w in message):
                continue
            if w == jd:
                continue
            else:
                vd[w] = 1 if w in message else 0
        return MeasurableSet(vd)

    def prob(self, model, ms, judge):
        vd = ms.get_value_dict()
        ec = model.get_probability().get_event_list()
        sc = model.get_sample_space().get_sample_list()
        jd = self._cm.get_judge_word()
        sm = self._cm.get_smoothing()
        found = 0
        total = 0
        for e in ec:
            evd = e.get_value_dict()
            flag = True
            for k,v in vd.items():
                if evd[k] != v:
                    flag = False
                    break
            if flag:
                total = total + 1
                if evd[jd] == judge:
                    found = found + 1
        return float(found + sm)/float(total + sm*2)

    def dump_measurable_set(self, ms):
        return json.dumps(ms.get_value_dict())

    def _create_word_list(self, mps):
        mpc = mps.get_mail_profile_list()
        ret = [self._cm.get_judge_word()]
        for mp in mpc:
            cp = mp.get_content_profile()
            with codecs.open(cp.get_path(), 'r', 'utf-8') as fd:
                content = fd.read()
                sep = self._cm.get_separators()
                words = re.split('[%s]' % sep, content)
                for word in words:
                    w = word.strip().replace('\n', '').replace('\r', '')
                    if w:
                        ret.append(w)
        return list(set(ret))

    def _create_event_list(self, name, mps, wc):
        mpc = mps.get_mail_profile_list()
        ret = []
        i = 0
        for mp in mpc:
            vd = defaultdict(int)
            jd = self._cm.get_judge_word()
            vd[jd] = mp.get_judge()
            sid = self._cm.get_event_sid(name, i + 1)
            cp = mp.get_content_profile()
            with codecs.open(cp.get_path(), 'r', 'utf-8') as fd:
                content = fd.read()
                for w in wc:
                    if w == jd:
                        continue
                    else:
                        vd[w] = 1 if w in content else 0
                ret.append(Event(sid, vd))
            i = i + 1
        return ret

    def _create_sample_space(self, name, wc):
        col = self._create_sample_list(name, wc)
        sid = self._cm.get_sample_space_sid(name)
        return SampleSpace(sid, col)

    def _create_sample_list(self, name, wc):
        ret = []
        i = 0
        for w in wc:
            sid = self._cm.get_sample_sid(name, i + 1)
            ret.append(Sample(sid, w))
            i = i + 1
        return ret

    def _create_probability_space(self, name, wc):
        sid = self._cm.get_probability_space_sid(name)
        return ProbabilitySpace(sid, 2**len(wc))

    def _create_probability(self, name, ec):
        psid = self._cm.get_probability_sid(name)
        return Probability(psid, ec)

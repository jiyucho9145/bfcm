#!/usr/bin/python3
# _*_ coding: utf-8 _*_

class ConfigManager:

    def __init__(self, config_dict):
        self._config_dict = config_dict

    def get_mail_collection_path(self, name):
        return '%s/%s' % (self._config_dict['path_config']['mail_collection_path'], name)

    def get_judge_path(self, name):
        file_name = self._config_dict['path_config']['judge_file_name']
        return '%s/%s' % (self.get_mail_collection_path(name), file_name)

    def get_content_path(self, name, mn):
        return '%s/%s' % (self.get_mail_collection_path(name), mn)

    def get_dat_path(self):
        return self._config_dict['path_config']['dat_path']

    def get_database_name(self):
        return self._config_dict['database_config']['database_name']

    def get_database_path(self):
        return '%s/%s' % (self.get_dat_path(), self.get_database_name())

    def get_sql_directory_path(self):
        return self._config_dict['path_config']['sql_directory_path']

    def get_judge_word(self):
        return self._config_dict['train_config']['judge_word']

    def get_separators(self):
        return self._config_dict['train_config']['separators']

    def get_smoothing(self):
        return float(self._config_dict['train_config']['smoothing'])

    def get_invalid_chars(self):
        return self._config_dict['arg_config']['invalid_chars']

    def get_sql_path(self, name):
        return '%s/%s' % (self.get_sql_directory_path(), name)

    def get_mail_profile_sid(self, name, i):
        return  'MP%s-%04d' % (name, i)

    def get_content_profile_sid(self, name, i):
        return 'CP%s-%04d' % (name, i)

    def get_mail_profile_set_sid(self, name):
        return 'MPS%s' % name

    def get_event_sid(self, name, i):
        return 'EV%s-%04d' % (name, i)

    def get_sample_sid(self, name, i):
        return 'SM%s-%04d' % (name, i)

    def get_sample_space_sid(self, name):
        return 'SM%s' % name

    def get_probability_space_sid(self, name):
        return 'EV%s' % name

    def get_probability_sid(self, name):
        return 'PR%s' % name

    def get_model_sid(self, name):
        return 'MD%s' % name

class ContentProfile:

    def __init__(self, sid, path):
        self._sid = sid
        self._path = path

    def get_sid(self):
        return self._sid

    def get_path(self):
        return self._path

class MailProfile:

    def __init__(self, sid, judge, content_profile):
        self._sid = sid
        self._judge = judge
        self._content_profile = content_profile

    def get_sid(self):
        return self._sid

    def get_judge(self):
        return self._judge

    def get_content_profile(self):
        return self._content_profile

class MailProfileSet:

    def __init__(self, sid, mpc):
        self._sid = sid
        self._mpc = mpc

    def get_sid(self):
        return self._sid

    def get_mail_profile_list(self):
        return self._mpc

class Sample:

    def __init__(self, sid, word):
        self._sid = sid
        self._word = word

    def get_sid(self):
        return self._sid

    def get_word(self):
        return self._word

class SampleSpace:

    def __init__(self, sid, sample_list):
        self._sid = sid
        self._sample_list = sample_list

    def get_sid(self):
        return self._sid

    def get_sample_list(self):
        return self._sample_list

class Event:

    def __init__(self, sid, value_dict):
        self._sid = sid
        self._value_dict = value_dict

    def get_sid(self):
        return self._sid

    def get_value_dict(self):
        return self._value_dict

class ProbabilitySpace:

    def  __init__(self, sid, cardinality):
        self._sid = sid
        self._cardinality = cardinality

    def get_sid(self):
        return self._sid

    def get_cardinality(self):
        return self._cardinality

class MeasurableSet:

    def __init__(self, value_dict):
        self._value_dict = value_dict

    def get_value_dict(self):
        return self._value_dict

class Probability:

    def  __init__(self, sid, event_list):
        self._sid = sid
        self._event_list = event_list

    def get_sid(self):
        return self._sid

    def get_event_list(self):
        return self._event_list

class Model:

    def __init__(self, sid, sample_space, probability_space, probability):
        self._sid = sid
        self._sample_space = sample_space
        self._probability_space = probability_space
        self._probability = probability

    def get_sid(self):
        return self._sid

    def get_sample_space(self):
        return self._sample_space

    def get_probability_space(self):
        return self._probability_space

    def get_probability(self):
        return self._probability

__author__ = 'rochelle'
#!/usr/bin/env python

import optparse, sys, os, traceback, errno
import ast
import re
import json
import ExtParser
import logging
import arcpy

class VampireDefaults:

    def __init__(self):
        # set up logging
        self.logger = logging.getLogger('Vampire')
        logging.basicConfig(filename='vampire.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG, filemode='w')


        # load default values from .ini file
        self.config = ExtParser.ExtParser()
        cur_dir = os.path.join(os.getcwd(), 'vampire.ini')
        ini_files = ['vampire.ini',
                     os.path.join(os.getcwd(), 'vampire.ini'),
                     cur_dir]
        dataset = self.config.read(ini_files)
        if len(dataset) == 0:
            msg = "Failed to open/find vampire.ini in {0}, {1} and {2}".format(ini_files[0], ini_files[1], ini_files[2])
            raise ValueError, msg
        self.countries = dict(self.config.items('country'))
        self.countries = dict((k.title(), v) for k, v in self.countries.iteritems())
        self.country_codes_l = []
        self.country_codes = {}

        for c in self.countries:
            cc = ast.literal_eval(self.countries[c].replace("\n", ""))
            if 'chirps_boundary_file' in ast.literal_eval(self.countries[c].replace("\n", "")):
                _chirps_boundary_file = ast.literal_eval(self.countries[c].replace("\n", ""))['chirps_boundary_file']
                p = re.match(r'.*\$\{(?P<param>.*)\}.*', _chirps_boundary_file)
                if p:
                    # has a reference
                    _chirps_boundary_file = _chirps_boundary_file.replace('${'+p.group('param')+'}',
                                                            self.config.get('CHIRPS', p.group('param')))
                    cc['chirps_boundary_file'] = _chirps_boundary_file
            if 'modis_boundary_file' in ast.literal_eval(self.countries[c].replace("\n", "")):
                _modis_boundary_file = ast.literal_eval(self.countries[c].replace("\n", ""))['modis_boundary_file']
                p = re.match(r'.*\$\{(?P<param>.*)\}.*', _modis_boundary_file)
                if p:
                    # has a reference
                    _modis_boundary_file = _modis_boundary_file.replace('${'+p.group('param')+'}',
                                                            self.config.get('MODIS', p.group('param')))
                    cc['modis_boundary_file'] = _modis_boundary_file
            self.countries[c] = cc
            self.country_codes[cc['abbreviation']] = c
            self.country_codes_l.append(cc['abbreviation'])
        return

    def get(self, section, item):
        return self.config.get(section, item)

    def get_home_country(self):
        return self.config.get('vampire', 'home_country')

    def get_country(self, country=None):
        if not country:
            return self.countries
        return self.countries[country]

    def get_country_code(self, country=None):
        if country is None:
            return self.country_codes
        if country in self.countries:
            return self.countries[country]['abbreviation']
        return

    def get_country_name(self, country_code):
        for c in self.countries:
            if country_code.lower() == self.countries[c]['abbreviation'].lower():
                return c
        return None

    def print_defaults(self):
        print self.config._sections


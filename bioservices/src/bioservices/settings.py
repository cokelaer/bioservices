# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 15:31:34 2014

@author: cokelaer
"""
import os
import ConfigParser

__all__ = ["get_bioservices_env"]


class Settings(object):
    """Not yet used"""
    def __init__(self):
        self.bs = BioServicesConfig()
        self.HOME = self.bs.home
        self.CONFIG_FILE = self.bs.config_file


def get_bioservices_env(section, option):
    bs = BioServicesConfig()

    if os.path.isdir(bs.home) == False:
        os.mkdir(bs.home)

    # Create the configuration from scratch
    if os.path.isfile(bs.config_file) == False:
        bs.cf.add_section("chemspider")
        bs.cf.set("chemspider", "token", "")
        fh = open(bs.config_file, "w")
        bs.cf.write(fh)
        fh.close()
        raise ValueError("""No token found for chemspider. 
        Creating one on http//www.chemspider.com and provide it when creating instance of ChemSpider""")
    else:
        bs.cf.read(bs.config_file)
        value = bs.cf.get(section, option)
        if value=="":
            raise ValueError("""No token found for chemspider. 
            Creating one on http//www.chemspider.com and provide it when creating instance of ChemSpider""")
        return value


class BioServicesConfig(object):
    """Not yet used"""
    def __init__(self):
        self.homedir = os.getenv("HOME")
        self.home = homedir + os.sep + ".bioservices"
        self.config_file = self.home + os.sep + "bioservices.cfg"

        self.cf = ConfigParser.ConfigParser()

    def read_config(self):
        return self.cf.read(bs.config_file)
        





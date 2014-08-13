# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 15:31:34 2014

@author: cokelaer
"""

__all__ = ["get_bioservices_env"]



def get_bioservices_env(section, option):
    import os
    import ConfigParser
    cf = ConfigParser.ConfigParser()

    homedir = os.getenv("HOME")
    bioservices_home = homedir + os.sep + ".bioservices"
    config_file = bioservices_home + os.sep + "bioservices.cfg"

    if os.path.isdir(bioservices_home) == False:
        os.mkdir(bioservices_home)
    if os.path.isfile(config_file) == False:
        cf.add_section("chemspider")
        cf.set("chemspider", "token", "")
        fh = open(config_file, "w")
        cf.write(fh)
        fh.close()
        raise ValueError("No token found for chemspider. Create one on http//www.chemspider.com and provide it when creating instance of ChemSpider")
    else:
        cf.read(config_file)
        value = cf.get(section, option)
        if value=="":
            raise ValueError("No token found for chemspider. Create one on http//www.chemspider.com and provide it when creating instance of ChemSpider")
        return value

#!/usr/bin/python
# -*- coding: latin-1 -*-
#
#  This file is part of bioservices software
#
#  Copyright (c) 2013-2014 - EBI-EMBL
#
#  File author(s):
#      
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/cokelaer/bioservices
#  documentation: http://packages.python.org/bioservices
#
##############################################################################
#$Id$
"""ChEMBLdb has been renamed into ChEMBL (module chembl instead of chembldb)"""


class ChEMBLdb(object):
    def __init__(self):
        print("""This class is deprecated. To update your code, 
            1. replace the module chembldb by chembl
            2. replace the class ChEMBLdb by ChEMBL""")





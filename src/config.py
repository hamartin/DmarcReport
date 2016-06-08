# -*- coding: UTF-8 -*-
# File name: config.py

'''
Dmarc Report config module.

Copyright 2016, Hans Åge Martinsen <hamartin@moshwire.com>

    This file is part of Dmarc Report.

    Dmarc Report is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Dmarc Report is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Dmarc Report.  If not, see <http://www.gnu.org/licenses/>
'''

import os

KV_DIRECTORY = '../kv'
IMG_DIRECTORY = '../img'

IMAGENORMAL = os.path.join(os.path.dirname(__file__), IMG_DIRECTORY,
                           'openfile-gr.png')
IMAGEOVER = os.path.join(os.path.dirname(__file__), IMG_DIRECTORY,
                         'openfile-wh.png')

# 
# Copyright (c) 2003 Asko Soukka
# 
# This file is part of Navidoc.
# 
# Navidoc is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# Navidoc is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
# 
# You should have received a copy of the GNU General
# Public License along with Navidoc; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
# 

# $Id: fi.py,v 1.2 2003/04/10 15:33:25 humppake Exp $

#
# Written by Asko Soukka
#

"""
Finnish-language mappings for language-dependent features of Docutils.
"""

__docformat__ = 'reStructuredText'

from docutils import nodes

labels = {
      'author': 'Kirjoittaja',
      'authors': 'Kirjoittajat',
      'organization': 'Järjestö',
      'address': 'Osoite',
      'contact': 'Yhteystieto',
      'version': 'Versio',
      'revision': 'Versio',
      'status': 'Tila',
      'date': 'Päiväys',
      'copyright': 'Tekijänoikeus',
      'dedication': 'Omistuskirjoitus',
      'abstract': 'Tiivistelmä',
      'attention': 'Huomio!',
      'caution': 'Ole varovainen!',
      'danger': '!VAARA!',
      'error': 'Virhe',
      'hint': 'Vihje',
      'important': 'Tärkeää',
      'note': 'Muistiinpano',
      'tip': 'Neuvo',
      'warning': 'Varoitus',
      'contents': 'Sisällys',
      'scope': 'Laajuus',
      'type': 'Tyyppi',
      'last-modified': 'Muokattu',
      
      'viewdocumentsource': "Sivun reST-kuvaus",
      'generatedon': "Luotu",
      'generatedby': "Sivun on tuottanut",
      'from': "",
      'source':"kuvauksesta"}
"""Mapping of node class name to label text."""

bibliographic_fields = {
      'author': 'author',
      'authors': 'authors',
      'organization': 'organization',
      'address': 'address',
      'contact': 'contact',
      'version': 'version',
      'revision': 'revision',
      'status': 'status',
      'date': 'date',
      'copyright': 'copyright',
      'dedication': 'dedication',
      'abstract': 'abstract'}
"""Finnish (lowcased) to canonical name mapping for bibliographic fields."""

#bibliographic_fields = {
#      'kirjoittaja': 'author',
#      'kirjoittajat': 'authors',
#      'järjestö': 'organization',
#      'osoite': 'address',
#      'yhteystieto': 'contact',
#      'versio': 'version',
#      'tarkistus': 'revision',
#      'tila': 'status',
#      'päiväys': 'date',
#      'tekijänoikeus': 'copyright',
#      'omistuskirjoitus': 'dedication',
#      'tiivistelmä': 'abstract'}
#"""Finnish (lowcased) to canonical name mapping for bibliographic fields."""

author_separators = [';', ',']
"""List of separator strings for the 'Authors' bibliographic field. Tried in
order."""

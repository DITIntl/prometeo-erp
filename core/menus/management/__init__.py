#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.2'

from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

from prometeo.core.widgets.models import *
from prometeo.core.menus.models import *

def fixtures(sender, **kwargs):
    """Installs fixtures for this application.
    """
    sidebar_region = Region.objects.get(slug="sidebar")
    
    # Menus.
    main_menu = Menu.objects.create(
        slug="main",
        description=_("Main menu")
    )
    
    # Widgets.
    main_menu_widget = Widget.objects.create(
        title=_("Main Menu"),
        slug="main-menu",
        description=_("The main menu"),
        source="prometeo.core.widgets.base.dummy",
        template="menus/widgets/menu.html",
        context="{\"name\": \"main\"}",
        show_title=False,
        sort_order=1,
        region=sidebar_region
    )
    
    post_syncdb.disconnect(fixtures)

post_syncdb.connect(fixtures)

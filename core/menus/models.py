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
__version__ = '0.0.5'

from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Permission
from django.db.models import permalink 
        
class Menu(models.Model):
    """Menu model.
    """
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('menu')
        verbose_name_plural = _('menus')

    def __unicode__(self):
        return self.slug

class Link(models.Model):
    """A generic menu entry.
    """
    menu = models.ForeignKey(Menu, db_column='menu_id', related_name='links', verbose_name=_('menu'))
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    url = models.CharField(_('url'), max_length=200)
    sort_order = models.PositiveIntegerField(_('sort order'), default=0)
    submenu = models.ForeignKey(Menu, db_column='submenu_id', related_name='parent_links', blank=True, null=True, verbose_name=_('sub-menu'))
    only_authenticated = models.BooleanField(_('Only for authenticated users'), default=True)
    only_staff = models.BooleanField(_('Only for staff users'), default=False)
    only_with_perms = models.ManyToManyField(Permission, blank=True, null=True, verbose_name=_('Only with following permissions'))

    class Meta:
        ordering = ('menu', 'sort_order', 'id',)
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __unicode__(self):
        return '%s | %s' % (self.menu, self.title)

    def get_absolute_url(self):
        return self.url

    @models.permalink
    def get_edit_url(self):
        user = get_object_or_404(User, pk=self.slug.split('_')[1])
        return ('bookmark_edit', (), {"username": user.username, "slug": self.slug})

    @models.permalink
    def get_delete_url(self):
        user = get_object_or_404(User, pk=self.slug.split('_')[1])
        return ('bookmark_delete', (), {"username": user.username, "slug": self.slug})
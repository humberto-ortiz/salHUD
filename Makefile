# Makefile - download statistics and prepare datafiles for salHUD
# Copyright 2013 - Humberto Ortiz-Zuazaga <humberto.ortiz@upr.edu>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

all-causes.json: basic-death.py basic-death-2008.txt
	python basic-death.py basic-death-2008.txt > all-causes.json

basic-death-2008.txt:
	wget -O $@ 'http://www.estadisticas.gobierno.pr/iepr/LinkClick.aspx?fileticket=jqa80LaEXmY%3d&tabid=201'

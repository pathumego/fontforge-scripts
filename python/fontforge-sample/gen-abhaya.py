#!/usr/bin/python
# -*- coding: utf-8 -*-
# gen.py is copyright (C) 2008-2012, Dave Crossland (dave@understandingfonts.com)
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#   The name of the author may not be used to endorse or promote products
#   derived from this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED
#   WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#   MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
#   EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""WIP..A FontForge plug-in to create a test doc easily. Based on Anthoza.py by Dave Crossland.
   Copy to ~/.FontForge/python/ and then find "Generate Sample" in the Tools menu.
"""

# XXX
# font.randomText(script[,language])
# where script and language are OpenType tags expressed as strings
# font.randomText("latn","ENG ")

import fontforge, sys, os, time, shutil, tempfile, subprocess, fileinput

myDate = time.strftime("%Y-%m-%d-%H%M", time.localtime()) # 2009-12-30-1559

lowercaseNonsense = """abcdefghijklmnopqrstuvwxyz ohnideascutlmbrpqfjvywzxkg lijhnumodbpqvywzxkftrceasg nhumwyvzxklijftraecopqbdgs ABCDEFGHIJKLMNOPQRSTUVWXYZ EFHILTMWRBPGCDOQNVAZXYKJSU Metepimeral film stuggy uplimber signalised demasculinisation a flamier flue amphi by guars maps pollucite a belat cat animalish unvying uncarded yourn lion a just nada celandines knockdowns paraesthesia coda uh vesseled ye hoc bleeps pyins be tribarred pee a said mel bony kolmogorov set pent am armaria dui bostonian gabblers serenify ingrately ugh if nix gin snary be want ewer spninx pions maze tv wags debutantes sophic inn hematospectrophotometer tesla ape friesian a slubby dud ragas a spermatozoa relaxes galax spars tad gif jaseyed tank do loaches up scup shipbuild we malacologic apicultural sering bedumb eel so piotty chalkotheke conflab manjack commercially bag hit pachuco rotted rectos clot repremising elk botanise viscidities fop claimless burstwort ash em he tom me punt mode skiing ballon becoiffed bay sty file hi watch crandallite iris eyrie muruxi situ cancerated tile a a hooches gynics gauge hid hemoptoe smidgeon ovidian catso up pales dry swonk chowk roentgenologically ganch big pull care openhandedness our outjinxing cauch repkie rad a a maidhead an apodictive a cabuja gyps zit in a newcomer micraner fainaigue as weft emir ow em latherers tv or ceiling sarcasticalness fireflower eth gybes push cronian jumblingly footworks bilayer land cows nonreformational mixen teat podolite em latchmen dowsed ahem phlogisticate tutly sans proseneschal up spindliest spry azine a sadware whigged peacock save ryas unsely load habituates arienzo sagest coistrels ajiva homelessly air dike with as as dinghies ax a canescent ext arrah purvoe deplumate rack mehari asp avascular herb tele a a my cig nub reconcentration ravine sporades lay rut lofters rex booed a jewelfish hankt uh tv ten lipogrammatic hapax unfurnitured astrophotometrical ink cud alloplastic flax him oct a boos of just slovens dishcloth exiguities hi chauk lug ye em aruspex kids trims sternway nonosmotically judith has whift nude leucemia dentinasal skart phanic"""

# abcdefghijklmnopqrstuvwxyz - alphabetical
# ohnideascutlmbrpqfjvywzxkg - drawing order
# lijhnumodbpqvywzxkftrceasg - groups
# nhumwyvzxklijftraecopqbdgs - groups

testString = "lijhnumodbpqvywzxkftrceasg"




def genAbhayasamp(thisFont):
  """Generate a OTF of this font with points rounded to integers"""
  systemFontsDir = '/Users/Pathum/src/github.com/mooniak/abhaya-libre-font/tests/fonts/'
  thisOTF = thisFont.fontname + ".otf"
  thisSystemFont = systemFontsDir + thisOTF
  thisFont.generate(thisOTF,flags=("round", "dummy-dsig", "PfEd-comments", "PfEd-colors", "PfEd-lookups", "PfEd-guidelines", "PfEd-background"))
  fontforge.logWarning("  Generated " + thisOTF)
  if os.path.exists(systemFontsDir):
    shutil.copy(thisOTF, thisSystemFont)
  if os.path.isfile(thisSystemFont):
    fontforge.logWarning("  Installed " + thisOTF)

def writeDoc(document,fileName):
  outfile = open(fileName, "w")
  outfile.write(document)
  outfile.close()



def genAbhaya(junk,glyph):
  """Roll a font forward"""
  myFont = fontforge.activeFont()
  genAbhayasamp(myFont)
  fontforge.logWarning("All done!")



if fontforge.hasUserInterface():
  keyShortcut="Ctl+Shft+n"
  fontforge.registerMenuItem(genAbhaya,None,None,("Font","Glyph"),keyShortcut,"Generate Abahay");

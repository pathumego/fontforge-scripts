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

def snapShot(myFont):
  fontforge.logWarning("Making a snapshot of " + myFont.fontname + " at " + myDate + "!")
  myFont.save()
  fontforge.logWarning("Saved master file")
  fontName =  myFont.fontname
  myFont.fontname = fontName
  myFont.familyname = fontName
  myFont.fullname = fontName
  myFont.appendSFNTName('English (US)', 'SubFamily', 'Medium')
  fontforge.logWarning("  Applied new name")
  mySFD = fontName + ".sfd"
  myFont.save(mySFD)
  fontforge.logWarning("  Saved as " + mySFD)
  # TODO: make sure spiros are all turned off
#  for glyph in myFont.glyphs():
#    glyph.round()
#    glyph.removeOverlap()
#    glyph.addExtrema()
#    glyph.simplify()
#    glyph.correctDirection()
  genFont(myFont)
  fontforge.logWarning("  Generated OTF ")
  genHTMLlowercase(myFont)
  fontforge.logWarning("  Generated HTML testdoc")
#TODO: new test documents ideally are made by work out what glyphs are in the font, make an adhesion t from those glyphs, and then make inkscape, shoebot or context documents with that dummytext and compile the PDFs and give the option to hit p to print or any other key to finish
  myFont.revert()
  fontforge.logWarning("  Reverted to master file")


def genFont(thisFont):
  """Generate a OTF of this font with points rounded to integers"""
  systemFontsDir = "/Users/Pathum/fonts/"
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


def genSVGlowercase(aFont,testString):
  fontName = aFont.fontname
  document = r"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<svg width="1488.189" height="1052.3622" version="1.0">\n\n<g id="layer1">\n<flowRoot\n       id="flowRoot2800"\n       style="font-size:12px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-family:%(fontName)s;-inkscape-font-specification:%(fontName)s"\n       transform="matrix(5.5742295,0,0,5.5742295,-782.49813,-1766.1304)">\n\n<flowRegion\n	id="flowRegion2802">\n<rect\n           id="rect2804"\n           width="248.03557"\n           height="165.44458"\n           x="151.42857"\n           y="320.93362"\n           style="font-size:12px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-family:%(fontName)s;-inkscape-font-specification:%(fontName)s"\n           ry="0"\n/>\n</flowRegion>\n\n<flowPara\n	id="flowPara2806"\n	style="font-size:44.84924698px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-family:%(fontName)s;-inkscape-font-specification:%(fontName)s"\n>\n%(testString)s\n</flowPara>\n\n</flowRoot>\n</g>\n</svg>""" % locals()
  fileName = "%(fontName)s.svg" % locals()
  writeDoc(document,fileName)
  subprocess.call("/usr/local/bin/inkscape %(fileName)s --export-pdf=%(fileName)s.pdf" % locals(), shell=True)

def makeStyles(sizesOfTypeAndLeading,unit):
  sizes = sorted(sizesOfTypeAndLeading.keys())
  document = ""
  for size in sizes:
    lead = sizesOfTypeAndLeading[size]
    document += ".a%(size)s%(unit)s {font-size: %(size)s%(unit)s; line-height:%(lead)s%(unit)s}\n" % locals()
  return document

def makeParas(sizesOfTypeAndLeading,unit,testString):
  sizes = sorted(sizesOfTypeAndLeading.keys())
  document = ""
  for size in sizes:
    document += """<p class="a%(size)s%(unit)s">%(size)s%(unit)s\n%(testString)s</p>\n""" % locals()
  #TODO add <wbr /> tags every 10 words?
  return document

def genHTMLlowercase(aFont):
  fontName = aFont.fontname
  sizesOfTypeAndLeading = { 8:10, 9:11, 10:12, 11:14, 12:16, 14:18, 16:20, 18:24, 24:32, 36:42 }
  fontDate = fontName[9:]
  document = r"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>%(fontName)s</title>
<style type="text/css">
@font-face { font-family: '%(fontName)s'; src: url('%(fontName)s.otf'); }
body { font-family:'%(fontName)s', serif; width:450px}
p { font-family: '%(fontName)s', serif; font-size: 14px; line-height:16px}
""" % locals()
  document += makeStyles(sizesOfTypeAndLeading,"pt")
  document += makeStyles(sizesOfTypeAndLeading,"px")
  document += "</style>\n</head>\n<body>"
#  keys = sizesOfTypeAndLeading.keys()
#  for item in keys:
#    document += makeParas(sizesOfTypeAndLeading,"px",lowercaseNonsense)
#    document += makeParas(sizesOfTypeAndLeading,"pt",lowercaseNonsense)
#  for line in fileinput.input(["/home/crossland/Desktop/MATD/term_6/2009-06-05a anthozoa/eliot.txt"]):
#    document += "<p>%(line)s</p>" % locals()
#  document += "</body></html>"
  document += """
<p>¿?!"#%&'()*+÷±-=×¬.,:;·<>«» @ 0123456789¶
{}~|¦[]\/¢$£€¤¥§©¼½¾AÀÁÂÃÄÅÆBßCÇŒDÐEÈÉÊËŒFGH
IÌÍÎÏJKLMNÑOÒÓÔÕÖØPþQRSTUÙÚÛÜVWXYÝZ
aàáâãäåæbcçdeèéêëœfﬀﬁﬃﬂﬄghiìíîïjkl
mnñoœòóôõöøpþqrstuùúµûüvwxyýÿzð¡
¨^®°ªº¹²³`´¯_¸ı</p>
<p>Benito Mussolini is reported to have said that “Fascism should more properly be called corporatism, since it is the merger of state and corporate power.” This goes to the heart of the map and shows why what follows is only the beginning. Of course, with the reality of Peak Oil, financial disasters are easy to predict; fish in a barrel. Yet within that global reality there lingers in the hearts and minds of many Americans a belief that somehow the Emperor will see to it that they are protected, that they remain comfortable and continue to have more resources than anyone else as the world suffers. Nonsense! Few will be prepared for how far that destruction has already progressed and fewer still will even think of preparing before the disaster becomes apparent.</p>
<p>This article © John Taylor Gatto, 2009. Trademark® TRADEMARN® at 9°
and spx is rox Ãlexander Älexander Ålexander Ælexander Çantarell Èducation Éducation Êducation Ëducation Ìllinois  Íllinois Îllinois Ïllinois Ðarth Ñovember Òland Óland Ôland Õland Öland Ølind Ùnger Únger Ûnger Ünger Ýanone þain glaß ànanánanânanãnanänanåna anananænançnanènanénanêna ananënanìnanínanînan anïnanðnanñnanana nònanónanônana nõnanönanønanana nùnanúnanûnanana nünanýnanþnanÿnanﬂnannanœ.</p>
<p>I taught for #30 years in some¹ of the worst schools in "New York City," and in² some of the³ best, and during that time I became an expert in boredom! Boredom was everywhere in my world, and if you asked the kids, as I often did, [why] they felt so^ bored, they\always \ gave the same answers: The work was stupid, it made no sense - they *already* knew it. Âlexander Œnglis They wanted to be doing something real, not just sitting around. Teachers_didn't seem to know <much aboun> their` subjects and weren’t interested in learning more. (And the kids were right: The teachers were every bit as bored as they were.) THIN³ AN² MOTION¹ can be 35µ ¶</p>
<p>(Boredom is the common condition of schoolteachers, and) anyone who has spent time in a teachers’ lounge can vouch for the low energy, the = whining, the <dispiriteb> attitudes found there. When asked why they’re bored, teachers tend to blame the ¼ kids; Who wouldn’t get ½ bored teaching students who are rude/interested only in grades? 5/10? If even that.¶</p>
<p>¡Of course, teachers are themselves products of the same ~12-year school programs that so thoroughly bore their students, & as school personnel, they’re trapped* inside structures even more rigid than those imposed on the kids¡ Who, then, is to blame? We all are. My ¾ grandfather taught me that. One afternoon when I was 7% I complained to him of boredom, + he batted me hard on the head. He told me I was never to use that term in his presence again, that if I was bored it was my fluﬄe fault and no one else’s. The obligation to amuse and instruct myself was entirely ﬁnish my own, he said, and those who didn’t know that were childish people, to be avoided if possible¿</p>
<p>That episode cured me of boredom forever, and here and there over the years I was able to pass on the lesson to some remarkable students. For the most part I found it «over futile to» challenge the oﬃcial notion that boredom and childishness were the natural state of aﬀairs in the classroom. Often I had to defy custom, and «NON» even bend the law, to help kids break out of this trap. By the time I retired in 1991, I’d had more than enough reason to think of our schools—with their long-term, cell-block-style forced confinement of both students and teachers—as virtual factories of childishness. Yet I honestly couldn’t see why they had to be that way.¶</p>
<p>My own experience had revealed to me what many other teachers must learn along the way, too, yet keep to themselves for fear of reprisal: we could easily and inexpensively jettison the old, stupid {structures} and help kids take an education [rather] than merely receive schooling. We could encourage the best qualities of youthfulness by being more flexible about time, texts and tests, introducing kids to truly competent adults, and giving each student the autonomy he or she needs to take risks in §80</p>
<p>We’ve been taught (that is, schooled) to think of “success” as synonymous with, or at least dependent on, “schooling,” but historically that isn’t true in either a financial or intellectual sense. Plenty of people [throughout] the world find ways to educate ¦ themselves without resorting to a system of standard school programs that all too often resembles prisons. Why then do we confuse education with such a system? What exactly is the purpose of our schools?</p>
<p>Mass schooling of a [HORROH] nature was conceived and advocated throughout {NOSSON}most of the 19th century. The “reason” given for this enormous upheaval of family life and cultural traditions was, roughly speaking, threefold: to make good people, to make good citizens, to make each person his or her personal best.</p>
<p>These goals are still trotted out today on a regular basis, and most of us accept them as a decent definition of public education’s mission, however short schools fall in achieving them. But we’d better look at Àlexander Inglis’ 1418 book, available for $60 and 50¢ or £30 and even in some places for ¤40 or ¥80 and perhaps €80, “Principles of Secondary Education.”</p>
<p>Inglis breaks down the actual purpose of modern schooling into six basic functions, any one of which is enough to curl the hair of those innocent enough to believe the three traditional goals of education listed earlier:  2 + 2 = 5  2+2=5 but when 3-3¬9 6×8×3=4×4 and 4÷2=2</p>"""
  fileName = "%(fontName)s.html" % locals()
  writeDoc(document,fileName)


#TODO: make a layer stack and pop the oldest layer off the stack (delete it)
#You may remove a layer with del font.layers["unneeded layer"]

def layerJig(myFont):
  # make all layers background layers
  for layer in myFont.layers:
    myFont.layers[layer].is_background = True
  # add layer "myDate" not quadratic, not background
  myFont.layers.add(myDate,0,0)
# TODO copy foreground to new layer! XXX
#  myFont.layer


def nextStep(junk,glyph):
  """Roll a font forward"""
  myFont = fontforge.activeFont()
  snapShot(myFont)
  fontforge.logWarning("All done!")



def finalContours(junk,glyph):
  glyph = fontforge.activeGlyph()
  glyph.round(100)
  glyph.addExtrema("all")
  glyph.simplify()
  glyph.simplify()
  glyph.correctDirection()
  print "Finalised %s" % glyph.glyphname

if fontforge.hasUserInterface():
  keyShortcut="Ctl+Shft+n"
  fontforge.registerMenuItem(nextStep,None,None,("Font","Glyph"),keyShortcut,"Generate Sample");
  keyShortcut="Ctl+Shft+p"
  fontforge.registerMenuItem(finalContours,None,None,("Font","Glyph"),keyShortcut,"Finalise Contours");

#  London Law -- a networked manhunting board game
#  Copyright (C) 2003-2004, 2005 Paul Pelzl
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License, Version 2, as 
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA




# PlayerIcon.py
#
# These classes handle display of a set of icons that show the player status.
# There are captions for names and readouts of the available tokens.
# Status icons can be overlaid on the player icons to show whose turn it is, etc.

import os, gettext, wx
from .TextPanel import *
from common.config import *


# draw an icon to represent a player, with a caption for the name and a
# readout of the available tokens.
# expects a list of three tokens (taxi, bus, undergnd) or a list of five
# tokens (taxi, bus, undergnd, black, double)
class PlayerIcon(wx.Panel):
   def __init__(self, parent, imagefile, thinkingimagefile, stuckimagefile, 
            name, tokenList, isMrX = False):
      wx.Panel.__init__(self, parent, -1) #wx.DefaultPosition, wx.DefaultSize, wx.SIMPLE_BORDER)

      self.iconPanel = wx.Panel(self, -1)
      self.isStuck   = False
      self.isMrX     = isMrX

      # load the image
      iconImage = wx.Image(imagefile, wx.BITMAP_TYPE_ANY)
      # we need an extra copy of the player icon, so we can blit to one of them in memory
      self.playerBitmap = wx.Bitmap(iconImage)
      self.iconBitmap   = wx.Bitmap(iconImage)
      self.iconBitmap2  = wx.Bitmap(iconImage)
      self.icon = wx.StaticBitmap(self.iconPanel, -1, self.iconBitmap)

      # load the overlay image for the "I'm thinking" question mark
      thinkingImage = wx.Image(thinkingimagefile, wx.BITMAP_TYPE_ANY)
      thinkingImage.SetMaskColour(255, 0, 242) # the purplish colour is not to be drawn
      self.thinkingBitmap = wx.Bitmap(thinkingImage)

      # load the overlay image for the "I'm stuck" stop sign
      stuckImage = wx.Image(stuckimagefile, wx.BITMAP_TYPE_ANY)
      stuckImage.SetMaskColour(255, 0, 242) # the purplish colour is not to be drawn
      self.stuckBitmap = wx.Bitmap(stuckImage)

      iconSizer = wx.BoxSizer(wx.VERTICAL)
      iconSizer.Add(self.icon, 0, wx.ADJUST_MINSIZE)
      self.iconPanel.SetSizer(iconSizer)
      iconSizer.Fit(self.iconPanel)


      # create the caption
      self.caption = wx.StaticText(self, label=" "+name[:20]+" ")
      self.caption.SetBackgroundColour(wx.Colour(255,255,255))

      # create the inventory labels
      if self.isMrX:
         self.blackLabel = wx.StaticText(self, label=" "+repr(tokenList[3])+" ")
         self.blackLabel.SetBackgroundColour(wx.Colour(0,0,0))
         self.blackLabel.SetForegroundColour(wx.Colour(255,255,255))
         self.doubleLabel = wx.StaticText(self, label=" "+repr(tokenList[4])+" ")
         self.doubleLabel.SetBackgroundColour(wx.Colour(255,84,166))
      else:
         self.taxiLabel = wx.StaticText(self, label=" "+repr(tokenList[0])+" ")
         self.taxiLabel.SetBackgroundColour(wx.Colour(255, 191, 0))
         self.busLabel = wx.StaticText(self, label=" "+repr(tokenList[1])+" ")
         self.busLabel.SetBackgroundColour(wx.Colour(7, 155, 0))
         self.ugndLabel = wx.StaticText(self, label=" "+repr(tokenList[2])+" ")
         self.ugndLabel.SetBackgroundColour(wx.Colour(160, 36, 96))
         self.ugndLabel.SetForegroundColour(wx.Colour(255, 255, 255))

      # stack the inventory labels vertically
      self.invSizer = wx.BoxSizer(wx.VERTICAL)
      if self.isMrX:
         self.invSizer.Add(self.blackLabel, 1, wx.EXPAND|wx.ADJUST_MINSIZE)
         self.invSizer.Add(self.doubleLabel, 1, wx.EXPAND|wx.ADJUST_MINSIZE)
      else:
         self.invSizer.Add(self.taxiLabel, 1, wx.EXPAND|wx.ADJUST_MINSIZE)
         self.invSizer.Add(self.busLabel, 1, wx.EXPAND|wx.ADJUST_MINSIZE)
         self.invSizer.Add(self.ugndLabel, 1, wx.EXPAND|wx.ADJUST_MINSIZE)

      # group the icon with the inventory
      iconInvSizer = wx.BoxSizer(wx.HORIZONTAL)
      iconInvSizer.Add(self.iconPanel, 0, wx.ALIGN_TOP|wx.ADJUST_MINSIZE)
      iconInvSizer.Add(self.invSizer, 0, wx.ALIGN_TOP|wx.ADJUST_MINSIZE)

      # put the caption under the bitmap and inventory lists
      self.topSizer = wx.BoxSizer(wx.VERTICAL)
      self.topSizer.Add(iconInvSizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.ADJUST_MINSIZE, 20)
      self.topSizer.Add(self.caption, 0, wx.ALIGN_CENTRE|wx.ALL, 2)
      self.SetSizer(self.topSizer)
      self.topSizer.SetSizeHints(self)

      self.iconDC = wx.MemoryDC()
      self.srcDC  = wx.MemoryDC()


   def updateTokens(self, tokenList):
      if self.isMrX:
         pass 
         self.blackLabel.SetLabel(" "+str(tokenList[3])+" ")
         self.doubleLabel.SetLabel(" "+str(tokenList[4])+" ")
      else:
         self.taxiLabel.SetLabel(" "+str(tokenList[0])+" ")
         self.busLabel.SetLabel(" "+str(tokenList[1])+" ")
         self.ugndLabel.SetLabel(" "+str(tokenList[2])+" ")
      self.invSizer.Layout()


   def setTurn(self):
      self.srcDC.SelectObject(self.playerBitmap)
      self.iconDC.SelectObject(self.iconBitmap2)
      self.iconDC.Blit(0, 0, self.iconBitmap.GetWidth(), self.iconBitmap.GetHeight(),
            self.srcDC, 0, 0)
      self.srcDC.SelectObject(self.thinkingBitmap)
      self.iconDC.Blit(0, 0, self.iconBitmap.GetWidth(), self.iconBitmap.GetHeight(),
            self.srcDC, 0, 0, wx.COPY, True)
      self.iconDC.SelectObject(wx.NullBitmap)
      temp             = self.iconBitmap
      self.iconBitmap  = self.iconBitmap2
      self.iconBitmap2 = temp
      self.icon.SetBitmap(self.iconBitmap)
      self.icon.Refresh(False)
      self.isStuck = False


   def setStuck(self):
      self.srcDC.SelectObject(self.playerBitmap)
      self.iconDC.SelectObject(self.iconBitmap2)
      self.iconDC.Blit(0, 0, self.iconBitmap.GetWidth(), self.iconBitmap.GetHeight(),
            self.srcDC, 0, 0)
      self.srcDC.SelectObject(self.stuckBitmap)
      self.iconDC.Blit(0, 0, self.iconBitmap.GetWidth(), self.iconBitmap.GetHeight(),
            self.srcDC, 0, 0, wx.COPY, True)
      self.iconDC.SelectObject(wx.NullBitmap)
      temp             = self.iconBitmap
      self.iconBitmap  = self.iconBitmap2
      self.iconBitmap2 = temp
      self.icon.SetBitmap(self.iconBitmap)
      self.icon.Refresh(False)
      self.isStuck = True


   def clearOverlay(self):
      self.srcDC.SelectObject(self.playerBitmap)
      self.iconDC.SelectObject(self.iconBitmap2)
      self.iconDC.Blit(0, 0, self.iconBitmap.GetWidth(), self.iconBitmap.GetHeight(),
            self.srcDC, 0, 0)
      self.iconDC.SelectObject(wx.NullBitmap)
      temp             = self.iconBitmap
      self.iconBitmap  = self.iconBitmap2
      self.iconBitmap2 = temp
      self.icon.SetBitmap(self.iconBitmap)
      self.icon.Refresh(False)



# Manage a group of icons to represent all six players.
class PlayerIconGroup(wx.Panel):
   def __init__(self, parent, nameList, tokenList):
      wx.Panel.__init__(self, parent, -1)

      # Get icons for all the players
      if len(nameList) != 6:
         sys.exit("PlayerIconGroup must be called with len(nameList) == 6\n" +
            "(here it was called with length "+repr(len(nameList))+")")

      cwd=os.getcwd()
      self.players = [PlayerIcon(self, 
         cwd+"/londonlaw/guiclient/images/playericon0.jpg",
         cwd+"/londonlaw/guiclient/images/thinking.png", 
         cwd+"/londonlaw/guiclient/images/stuck.png", 
         nameList[0], tokenList[0], True)]
      for i in list(range(1, 6)):
         filename = cwd+"/londonlaw/guiclient/images/playericon" + str(i) + ".jpg"
         self.players.append(PlayerIcon(self, filename,
            cwd+"/londonlaw/guiclient/images/thinking.png", 
            cwd+"/londonlaw/guiclient/images/stuck.png", 
            nameList[i], tokenList[i]))


      self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
      for p in self.players:
         self.topSizer.Add(p, 0, wx.ALIGN_CENTRE) 
      self.SetSizer(self.topSizer)
      self.topSizer.SetSizeHints(self)


   # update the icons to show whose turn it is
   def setTurn(self, index):
      for i in list(range(6)):
         if i == index:
            self.isStuck = False
            self.players[i].setTurn()
         else:
            if not self.players[i].isStuck:
               self.players[i].clearOverlay()


   # update the icons to show someone is stuck
   def setStuck(self, index):
      self.players[index].setStuck()




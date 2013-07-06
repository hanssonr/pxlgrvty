"""
Handles all the chunks on the map!
"""

from Box2D import b2Vec2
import math
#from Level import TestTile
from Tile import Tile

class ChunkHandler(object):
    
    __mActiveChunks = []
    __mChunks = []
    CHUNK_SIZE = None
    mActiveTiles = []
    
    def __init__(self, physworld, chunksize):
        self.mWorld = physworld
        self.CHUNK_SIZE = chunksize
    
    """ Puts active chunks in activelist and removes the ones thats not active """
    def manageChunks(self, pos):
        center = self.getChunkPosition(pos)
        top = b2Vec2(center.x, max(center.y-1, 0))
        right = b2Vec2(min(center.x+1, len(self.chunkslist[0])), center.y)
        bottom = b2Vec2(center.x, min(center.y+1, len(self.chunkslist)))
        left = b2Vec2(max(center.x-1, 0), center.y)
        topleft = b2Vec2(left.x, top.y)
        topright = b2Vec2(right.x, top.y)
        bottomleft = b2Vec2(left.x, bottom.y)
        bottomright = b2Vec2(right.x, bottom.y)
        
        list = [center, top, right, bottom, left, topleft, topright, bottomleft, bottomright]
        
        #try add new active chunks
        for pos in list:
            chunk = self.getChunk(pos)
                
            if chunk != None:
                self.activateChunk(chunk)
        
        toRemove = []  
        #remove chunks thats arent necessary
        for chunk in self.activechunks:
            remove = True
            for pos in list:
                if chunk.position == pos:
                    remove = False
                    break
        
            if remove:
                toRemove.append(chunk)
                
        for chunk in toRemove:
            for tile in chunk.tiles:
                self.mActiveTiles.remove(tile)
                tile.destroy()
            self.activechunks.remove(chunk)
            
        
    def isPositionInActiveChunks(self, position):
        chunkpos = self.getChunkPosition(position)
        
        if any(x.position == chunkpos for x in self.activechunks):
            return True
        
        return False
    
    def addChunk(self, chunk):
        if not any(x.position == chunk.position for x in self.chunks):        
            self.__mChunks.append(chunk)
    
    def activateChunk(self, chunk):
        if len(self.activechunks) > 0:                   
            if not any(x.position == chunk.position for x in self.activechunks):
                #print "activate chunk: %s" % chunk.position
                self.__mActiveChunks.append(chunk)
                self.__createChunkTiles(chunk)
        else:
            self.__mActiveChunks.append(chunk)
            self.__createChunkTiles(chunk)
    
    def __createChunkTiles(self, chunk):
        for tile in chunk.tiles:
            self.mActiveTiles.append(tile)
            tile.create()
    
    def deactivateChunk(self, chunk):
        if any(x.position == chunk.position for x in self.activechunks):
            self.__mActiveChunks.remove(x)
    
    """ Returns a chunkobject depending on chunkposition """        
    def getChunk(self, chunkpos):
        try:
            return self.__mChunks[int(chunkpos.y)][int(chunkpos.x)]
            #if any(x.position == chunkpos for x in self.__mChunks):
                #return x
        except IndexError:
            pass
    
    def __getChunks(self):
        return self.__mChunks
    
    def __getActiveChunks(self):
        return self.__mActiveChunks
    
    def getChunkPosition(self, pos):
        return b2Vec2(int(pos.x / self.CHUNK_SIZE), int(pos.y / self.CHUNK_SIZE))
    
    chunkslist = property(__getChunks, None)
    activechunks = property(__getActiveChunks, None)
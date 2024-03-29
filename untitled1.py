# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1guZLPfEMKNhWb3H3xirmbrjpp_i1nXmF
"""

import random
import string
import itertools
from difflib import SequenceMatcher

target = "hsasd".upper()

class Word:
  def __init__(self,word):
    self.word = word
  def fitLevel(self, fitness = 0.0):
    self.fitness = fitness
  def getFit(self):
    return self.fitness
  def getWord(self):
    return self.word
  def setWord(self,word):
    self.word = word

def populate(x=[]):
  for i in range(5):
    p1 = Word(word=(''.join([random.choice(string.ascii_letters) for n in range(len(target))])).upper())
    x.append(p1)
  return x

def fitness(x=[]):
  z = [0.0,0.0]
  maxrate = 0.0
  smaxrate = 0.0
  for i in x:
    if i.getFit() > smaxrate:
      if i.getFit() > maxrate:
        smaxrate = maxrate
        maxrate = i.getFit()
        z[1] = z[0]
        z[0] = i
      else:
        smaxrate = i.getFit()
        z[1] = i
  return z

def offsprings(x=[]):
  f = list(x[1].getWord())
  x = list(x[0].getWord())
  for i in x:
    f.append(i)
  final = list(itertools.permutations(f))
  final2 = []
  for i in final:
    p = i[0] + i[1] + i[2] + i[3] + i[4]
    final2.append(p)
    p = i[5] + i[6] + i[7] + i[8] + i[9]
    final2.append(p)
  return final2

def mutate(x=[]):
  for i in range(int(len(x)/100)):
    d = random.randint(0,len(x))
    p = list(x[d])
    p[random.randint(0,len(p)-1)] = '' + random.choice(string.ascii_letters).upper()
    x[d] = ''.join(p)
  return x

x = populate()
state = False
right = ''
while state == False:
  x = offsprings(x=x)
  x = mutate(x=x)
  for i in x:
    if i == target:
      state = True
      right = i
      break
  d = []
  for i in x:
    d.append(Word(i))
  x = d
print(right)
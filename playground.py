from keep_alive import keep_alive
import random
import discord 
from discord.ext import commands
import asyncio
from asyncio import sleep
import time 
import threading
import os
import requests
import json
import typing
import aiohttp
import logging
from main.py import client


@client.command()
async def dietophat(ctx, password):
  if password == 'tophat':
    if (random.randint(1, 100) == 1):
      await ctx.send('Die TopHat')
    else:
      await ctx.send('god fucking hates you lol')
  else:
    pass

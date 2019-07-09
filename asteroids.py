#!/usr/bin/env python3

import sys
import pygame as pg
from src.main import main
import cProfile

if __name__=='__main__':
    main()
    pg.quit()
sys.exit()
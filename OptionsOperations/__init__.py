#  System Requirements / Packages and Libraries Import

import requests
import decimal
import time
import os
import subprocess
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from datetime import date
from datetime import timedelta


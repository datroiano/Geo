#  System Requirements / Packages and Libraries Import

import requests
import decimal
import time
import os
import subprocess
import json
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from datetime import date
from datetime import timedelta
from pathlib import Path
from openpyxl.utils import get_column_letter



def save_to_excel(df):
    # Get the path to the Downloads folder
    downloads_path = Path.home() / "Downloads"

    # Create the full path for the Excel file
    excel_file_path = downloads_path / "simulated_data.xlsx"

    # Set up ExcelWriter and specify a larger column width for all columns
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        df.to_excel(writer, index=False)
        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            col_letter = get_column_letter(col_idx + 1)
            writer.sheets['Sheet1'].column_dimensions[
                col_letter].width = column_width * 1.2  # Adjusted for better readability

    print(f"Excel file saved to: {excel_file_path}")

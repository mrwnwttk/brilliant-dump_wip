# brilliant_dump

This is the broken codebase for a tool to dump courses from brilliant.org as pdf files. My trial expired so I have no intention of working on this any further. The pdf.py file contains code that can save a website as both HTML as well as PDF. My initial plan was to download the file using PDFCrowd (with the watermarks) and use the metadata (most importantly the page height) to adjust it the way PyPDF2 can handle it. For some reason Selenium and ChromeDriver can't see the buttons on brilliant's website, so that needs to be fixed first. Maybe someone can make it work :)
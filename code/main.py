'''
1Feb22 BIOT670 Group 6
Main script for bioinformatics database
'''

from app import create_app
from settings import DevelopmentSettings

app = create_app()

if __name__ == '__main__':
    app.run()

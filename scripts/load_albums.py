import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ml_project.settings")

import django
django.setup()

from reviews.models import Album


def save_album_from_row(album_row):
    album = Album()
    album.id = album_row[0]
    album.name = album_row[1]
    album.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        albums_df = pd.read_csv(sys.argv[1])
        print albums_df

        albums_df.apply(
            save_album_from_row,
            axis=1
        )

        print "There are {} albums".format(Album.objects.count())
        
    else:
        print "Please, provide Album file path"

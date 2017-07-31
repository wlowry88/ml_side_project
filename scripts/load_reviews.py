import sys, os
from os.path import realpath, join, dirname
import datetime
import pandas as pd

sys.path.insert(0, join(dirname(realpath(__file__)),'../'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ml_project.settings")

import django
django.setup()

from reviews.models import Review, Album
from django.contrib.auth.models import User


def save_review_from_row(review_row):
    review = Review()
    review.id = review_row[0]
    review.user = User.objects.get(id=review_row[1])
    review.album = Album.objects.get(id=review_row[2])
    review.rating = review_row[3]
    review.pub_date = datetime.datetime.now()
    review.comment = review_row[4]
    review.save()
    
    
# the main function for the script, called by the shell    
if __name__ == "__main__":
    
    # Check number of arguments (including the command name)
    if len(sys.argv) == 2:
        print "Reading from file " + str(sys.argv[1])
        reviews_df = pd.read_csv(sys.argv[1])
        print reviews_df

        # apply save_review_from_row to each review in the data frame
        reviews_df.apply(
            save_review_from_row,
            axis=1
        )

        print "There are {} reviews in DB".format(Review.objects.count())
        
    else:
        print "Please, provide Reviews file path"


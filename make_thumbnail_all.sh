find $1 | grep mp4 | perl -ne "chomp; print \"python make_thumbnail.py '\$_'\n\"" > tmp.sh
find $1 | grep mkv | perl -ne "chomp; print \"python make_thumbnail.py '\$_'\n\"" >> tmp.sh
# sh tmp.sh

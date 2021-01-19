find /Volumes/VIDEO/SERIES/명탐정\ 코난 | grep mp4 | perl -ne "chomp; print \"python make_thumbnail.py $1 '\$_'\n\"" > tmp.sh
find /Volumes/VIDEO/SERIES/명탐정\ 코난 | grep mkv | perl -ne "chomp; print \"python make_thumbnail.py $1 '\$_'\n\"" >> tmp.sh
sh tmp.sh

find /Volumes/SERIES/명탐정\ 코난 | grep mp4 | perl -ne "chomp; print \"python run.py '\$_'\n\"" > tmp.sh
find /Volumes/SERIES/명탐정\ 코난 | grep mkv | perl -ne "chomp; print \"python run.py '\$_'\n\"" >> tmp.sh
sh tmp.sh
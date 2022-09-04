# Making video thumbnails by template matching.
* It needs ffmpeg, iconv command and python libraries (opencv-python,numpy and chardet).
* Make a snapshot as `tmpl.jpg` for finding signature frame.
* Edit delay and thumbnail features in `make_thumbnail.py` for you.

```bash
$ pip install -r requirements.txt
$ sh make_thumbnail_all.sh TARGET_DIR
```

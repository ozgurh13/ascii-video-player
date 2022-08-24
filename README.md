# ascii video player

play a video in ascii (no sound)

external dependencies: `openCV`, `pillow`, `numpy`, `youtube-dl`



## usage

there are 4 commands

1. **image**: used for converting images
```
# convert an image to ascii and print to stdout
main.py image myimage.png

# convert an image and write to a file
main.py image myimage.jpg -o myimage
```
 * options:
   * `-o`/`--output`: output destination
   * `-s`/`--size`: width of the frame (in ascii characters)
   * `--light`: use light mode



2. **video**: used for converting/playing videos
```
# convert a video and write to file
main.py video myvideo.mkv -o myvideo

# play a video as it's being converted
main.py video myvideo.mkv --live
```
 * options
   * `-o`/`--output`: output destination
   * `-s`/`--size`: width of the frame (in ascii characters)
   * `--live`: play the video as it's being converted
   * `--light`: use light mode



3. **link**: used for converting/playing videos from the web
```
# play a video directly from youtube
main.py link https://www.youtube.com/watch\?v\=jNQXAC9IVRw --live

# convert a video from youtube and save it to a file
main.py link https://www.youtube.com/watch\?v\=jNQXAC9IVRw -o myvideo
```
 * options
   * `-q`/`--quality`: quality of the video to be retrieved
   * `-o`/`--output`: output destination
   * `-s`/`--size`: width of the frame (in ascii characters)
   * `--live`: play the video as it's being converted
   * `--light`: use light mode

*note: `youtube_dl` is used to get the url, so any website it supports should work*



4. **play**: used for playing videos that were previously converted to ascii
```
# convert a video from youtube and save it a file
main.py link https://www.youtube.com/watch\?v\=jNQXAC9IVRw -o myvideo
# play the video that was converted
main.py play myvideo
```


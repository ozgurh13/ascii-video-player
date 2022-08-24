
from  utils            import  die
from  get_url          import  get_url
from  argparse         import  ArgumentParser, Namespace
from  ascii_converter  import  *

import bz2



def main():
    args = get_cmdline_args()
    args.func(args)



def get_cmdline_args() -> Namespace:
    '''
    parses command line arguments
    '''
    cmdline = ArgumentParser(
        description = 'play a video in ascii or convert a video/image to ascii'
    )
    subparsers = cmdline.add_subparsers()


    '''
    convert an image to ascii
        image path/to/image -o path/to/output
        image path/to/image -s 750
        image path/to/image --light
    '''
    image = subparsers.add_parser('image', help = 'convert an image')
    image.add_argument('image', type = str, help = 'path to image')
    image.add_argument( '-o', '--output', dest = 'output', type = str
                      , help = 'output file (default is stdout)' )
    image.add_argument( '--light', dest = 'light', action = 'store_true', default = False
                      , help = 'light mode (default is dark)' )
    image.add_argument( '-s', '--size', dest = 'size', type = int , default = 500
                      , help = 'size of the output (default is 500)' )
    image.set_defaults(func = do_image)


    '''
    convert a video to ascii
        video path/to/video -o path/to/output
        video path/to/video -s 650 -o path/to/output

    play a video in ascii (live)
        video path/to/video --live
        video path/to/video --live --light
    '''
    video = subparsers.add_parser('video', help = 'convert/play a video')
    video.add_argument('video', type = str, help = 'path to video')
    video.add_argument( '--light', dest = 'light', action = 'store_true', default = False
                      , help = 'light mode (default is dark)' )
    video.add_argument( '-s', '--size', dest = 'size', type = int , default = 500
                      , help = 'size of the output (default is 500)' )
    video_output = video.add_mutually_exclusive_group()
    video_output.add_argument( '--live', dest = 'live', action = 'store_true', default = False
                             , help = 'play video as it\'s being converted' )
    video_output.add_argument( '-o', '--output', dest = 'output', type = str
                             , help = 'output file (default is stdout)' )
    video.set_defaults(func = do_video)


    '''
    convert a video from a link to ascii
        link link.to/video -o path/to/output
        link link.to/video -s 850 -o path/to/output --light

    play a video from a link in ascii (live)
        link link.to/video --live
        link link.to/video --light --live
    '''
    link = subparsers.add_parser('link', help = 'convert/play a video from link')
    link.add_argument('link', type = str, help = 'link to video')
    link.add_argument( '-q', '--quality', dest = 'quality', type = int , default = 1080
                     , choices = [360, 480, 720, 1080, 1440, 2160]
                     , help = 'quality of video from link (default is 1080)' )
    link.add_argument( '--light', dest = 'light', action = 'store_true', default = False
                     , help = 'light mode (default is dark)' )
    link.add_argument( '-s', '--size', dest = 'size', type = int , default = 500
                     , help = 'size of the output (default is 500)' )
    link_output = link.add_mutually_exclusive_group()
    link_output.add_argument( '--live', dest = 'live', action = 'store_true', default = False
                            , help = 'play link as it\'s being converted' )
    link_output.add_argument( '-o', '--output', dest = 'output', type = str
                            , help = 'output file (default is stdout)' )
    link.set_defaults(func = do_link)


    '''
    play video that was converted to ascii
        play path/to/ascii_video
    '''
    play = subparsers.add_parser('play', help = 'play a converted video')
    play.add_argument('play', type = str, help = 'path to video')
    play.set_defaults(func = do_play)


    return cmdline.parse_args()



def do_image(args):
    '''
    convert an image
    '''
    ascii_image = convert_image_to_ascii(args.image, args.size, args.light)
    write_image(args.output, ascii_image)



def do_video(args):
    '''
    convert/play a video
    '''
    video_link(args.video, args)



def do_link(args):
    '''
    convert/play a video from link
    '''
    video_url = get_url(args.link, args.quality)
    video_link(video_url, args)



def video_link(path, args):
    '''
    either play or convert a video/link
    '''
    if args.live:       # play video as it's being conveted
        play_video_as_ascii(path, args.size, args.light)

    else:               # convert video and write to destination file
        ascii_video = convert_video_to_ascii(path, args.size, args.light)
        write_video(args.output, ascii_video)



def do_play(args):
    '''
    play a converted video
    '''
    play_ascii_video_from_file(args.play)



def write_image(output, contents):
    '''
    output an image file
    '''
    if output is None:
        print(contents)

    else:
        with open(output, 'w') as file:
            file.write(contents)



def write_video(output, contents):
    '''
    output a video file using bz2 compression
    '''
    if output is None:
        print(contents)

    else:
        with bz2.open(output, 'wb') as file:
            file.write(contents.encode())



if __name__ == '__main__':
    main()


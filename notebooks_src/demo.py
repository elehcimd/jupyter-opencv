def cells():
    '''
    # Example of embedded video player and OpenCV processing
    '''

    import cv2
    from lab.helpers.notebook_helpers import play_video

    '''
    '''

    # video player
    play_video('../datasets/small.mp4')

    '''
    '''

    # load video with OpenCV
    cap = cv2.VideoCapture('../datasets/small.mp4')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print("Width={} Height={} FPS={}".format(width, height, fps))

    '''
    '''

    # convert video to grayscale and save it to file

    # seek to first frame in input video
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # open video writer
    vid = cv2.VideoWriter('/playground/datasets/small_bw.mp4',
                          0x00000021,
                          fps,
                          (width, height),
                          isColor=False)

    # initialize number of frames
    frames_count = 0

    while(True):
        ret, frame = cap.read()
        frames_count += 1 if ret else 0
        if ret:
            # convert frame from color to grayscale and write it
            frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vid.write(frame_bw)
        else:
            vid.release()
            break

    print("Processed {} frames".format(frames_count))

    '''
    '''

    play_video('../datasets/small_bw.mp4')

    '''
    '''

import cv2
import easyocr
import argparse
import logging

def create_reader(language: str):
    try:
        reader = easyocr.Reader([language])
        return reader
    except:
        logging.exception('Lingua nao selecionada')


def write_on_frame(reader, frame, bottom_left_corner = (10, 50), font = cv2.FONT_HERSHEY_SIMPLEX, font_scale = 1, font_color = (255, 255, 255), thickness = 1, line_type = 2):
    return cv2.putText(frame, ' '.join(str(element) for element in reader.readtext(frame, detail = 0)), bottom_left_corner,
                       font, font_scale, font_color,
                       thickness, line_type)


def display_text_on_photo(reader, photo_path):
    capture = cv2.VideoCapture(photo_path)
    ret, frame = capture.read()

    cv2.namedWindow('Text_on_image', frame)
    write_on_frame(reader, frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def display_text_on_video(reader, video_path = 0):
    try:
        video = cv2.VideoCapture(video_path)
        while True:
            ret, frame = video.read()
            frame = write_on_frame(reader, frame)
            cv2.imshow('frame_with_text', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        video.release()
        cv2.destroyAllWindows()
    except:
        logging.exception('Erro na leitura da webcam')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Select your language')
    parser.add_argument('-l', '--language', help = 'selecione uma das linguas -> en, ch, ch_sim')
    parser.add_argument('-m', '--mode', help = 'modo de leitura video, foto ou webcam')
    parser.add_argument('-p', '--path', help = 'caso tenha escolhido video ou foto coloque o path', nargs = '?')
    args = vars(parser.parse_args())

    reader = create_reader(args['language'])
    if args['mode'] == 'video':
        #call video reading function
        display_text_on_video(reader, args['path'])
    elif args['mode'] == 'photo':
        #call photo reading function
        display_text_on_photo(reader, args['path'])
    elif args['mode'] == 'webcam':
        #call webcam reading function
        display_video(reader)
    else:
        raise NotImplementedError
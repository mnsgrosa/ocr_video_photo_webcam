import cv2
import easyocr
import argparse
import logging

def create_reader(language: str):
    '''
    Funcao responsavel por criar o leitor das imagens
    
    param: language -> linguagem que deseja ler
    return: reader -> modelo responsavel por ler o que esta na imagem
    '''
    try:
        reader = easyocr.Reader([language])
        return reader
    except:
        logging.exception('Lingua nao selecionada')


def write_on_frame(reader, frame, bottom_left_corner = (10, 50), font = cv2.FONT_HERSHEY_SIMPLEX, font_scale = 1, font_color = (255, 255, 255), thickness = 1, line_type = 2):
    '''
    Funcao responsavel pela escrita nos frames

    params: reader -> Objeto responsavel pela leitura nas imagens
            frame -> frame em que ocorrera leitura e escrita
            bottom_left_corner -> ponto inferior esquerdo de onde comecara a escrita
            font -> fonte do texto
            font_scale -> escala da fonte
            font_color -> cor da fonte 
            thicknesss -> grossura da fonte
            line_type -> tipo de linha

    return: Retorna o frame com o texto escrito na posicao escolhida
    '''
    return cv2.putText(frame, ' '.join(str(element) for element in reader.readtext(frame, detail = 0)), bottom_left_corner,
                       font, font_scale, font_color,
                       thickness, line_type)


def display_text_on_photo(reader, photo_path):
    '''
    Funcao responsavel por mostrar a imagem com o texto escrito

    params: reader -> objeto responsavel pela leitura da imagem
            photo_path-> caminho do arquivo da foto
    return: None
    '''
    try:
        capture = cv2.VideoCapture(photo_path)
        ret, frame = capture.read()
    
        cv2.namedWindow('Text_on_image', frame)
        write_on_frame(reader, frame)
        cv2.imshow('frame', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        logging.exception('Erro ao carregar foto')

def display_text_on_video(reader, video_path = 0):
    '''
    Funcao responsavel por mostrar a imagem do video com o texto escrito

    params: reader -> objetto responsavel pela leitura da imagem
            video_path -> caminho do arquivo do video ou por default a webcam

    return: None
    '''
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

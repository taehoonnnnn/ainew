from threading import Thread
from tkinter import *
import tkinter.font
from tkinter import messagebox, filedialog, ttk
from tkinter.tix import COLUMN
import cv2, av, subprocess
import pkgutil

# 설정
bg = '#2c3e50'
bnbg = '#2f3640'
fg = 'white'


def get_duration(filename): # 비디오 정보 추출
    container = av.open(filename)
    video = container.streams.video[0]
    frames = container.decode(video=0)
    fps = video.average_rate
    fps_calculate = int(str(fps).split('/')[0]) / int(str(fps).split('/')[1])
    print("fps : " + str(fps_calculate))
    print("movie seconds : " + str(round(video.frames, 2) / fps_calculate))
    seconds = video.frames/fps_calculate
    vdlab4.config(text='-영상길이 : ' + str(round(fps_calculate, 2)) + '프레임' + f'({round(seconds,1)}초)')


# -- 동영상 메인 사진 변경 --
def get_video_image(path, name):
    vidcap = cv2.VideoCapture(path)
    success,image = vidcap.read()
    success = True
    resize_img = cv2.resize(image, (309,331))
    cv2.imwrite(f"./image/{name}.png", resize_img)
    vidcap.release()


def video_open(): # 비디오 파일 열기
    global video_file_path
    video_file_path = filedialog.askopenfilename(initialdir='', title='동영상 파일선택', filetypes=(
    ('mp4 files', '*.mp4'), ('avi files', '*.avi'), ('all files', '*.*')))
    try:
        get_duration(video_file_path)
        print(video_file_path)
        vdlab1.config(text='-파일경로 : ' + video_file_path)
        name = 'image'
        get_video_image(video_file_path, name)
        img_change = PhotoImage(file=f'./image/{name}.png', master=frame_videorg)
        videoimglab.image = img_change
        videoimglab.configure(image=img_change)
    except:
        messagebox.showinfo("오류", "오류")


# -- final_ai Thread --
def get_select_file_therading():
    try:
        t1 = Thread(target=get_select_file)
        t1.daemon = True
        t1.start()
    except:
        print(f'Thread error : {t1}')

def get_select_file():
    from one_create import text_edit
    create_selects = create_select.get()
    model_selects = model_select.get()
    print(create_selects, model_selects)

    if create_selects == '음성' and model_selects != '선택해주세요.':
        text_edit(model_selects)

    elif create_selects == '비디오' and model_selects != '선택해주세요.':
        if not 'video_file_path' in locals() and not 'asdf' in globals():
            text_edit(model_selects)
            final_ai()
            del video_file_path
    else:
        messagebox.showinfo("오류", "체크사항을 확인해주세요.")


# -- final_ai Thread --
def final_ai_therading():
    try:
        t1 = Thread(target=final_ai)
        t1.daemon = True
        t1.start()
    except:
        print(f'Thread error : {t1}')


# -- TTS + LipFake Start --
def final_ai():
    try:
        loding.config(text='비디오 생성중...')
        cmd = f'python lipfake/inference.py --checkpoint_path ./checkpoints/wav2lip_gan.pth --face {video_file_path} --audio ./TTSOUT/audio/file.wav --outfile ./TTSOUT/video/file.mp4 --resize_factor 2'
        print(cmd)
        subprocess.run(cmd)
        progressbar['value'] = 100
        progressbar.update()
    
    except:
        messagebox.showinfo("오류", "오류")


def loding_cnt(text):
    loding.config(text=f'{text}')


def human_win():  # AI_HUMAN


    newWindow = Tk()
    mainfont2 = tkinter.font.Font(family='맑은 고딕', size=15, weight='bold')
    newWindow.geometry('800x770')
    newWindow.title('AI NEWS ROOM')
    
    inco_frame = LabelFrame(newWindow, bg=bg, relief='flat')
    inco_frame.pack(fill='both', expand=False)

    Label(inco_frame, text='AI NEWS ROOM', bg=bg, fg='white', font=mainfont2).pack() # 타이틀
    Label(inco_frame, bg=bg, text='  ').pack(side='left') # 여백용
    Label(inco_frame, bg=bg, text='  ').pack(side='right')

    frame1 = LabelFrame(inco_frame, bg=bg, relief='flat',width=800, height=150)
    frame1.pack(fill='both', expand=True, side='left')

    # 동영상 프레임
    frame_video = LabelFrame(frame1, bg=bg, text='동영상', relief='groove', width=500, height=150, font=mainfont2, fg='white')
    frame_video.pack(fill='both', expand=False) # 메인프레임

    frame_videolf = LabelFrame(frame_video, bg=bg, relief='flat') # 왼쪽 프레임
    frame_videolf.pack(fill='both', expand=True, side='left', padx=20)

    bnvd = Button(frame_videolf, text='파일업로드', height=3, widt=25, bg=bnbg, 
                    fg='white', relief='flat', command=video_open).pack(pady=20)
    
    global vdlab1, vdlab4, videoimglab, frame_videorg
    vdlab1 = Label(frame_videolf, text='-파일경로 : '+'C:\영상경로.mp4', bg=bg, fg='white')
    vdlab1.pack(anchor='nw', padx=20, pady=10)
    
    vdlab2 = Label(frame_videolf, text='-지원가능한 파일확장자 : MP4,AVI..', bg=bg, fg='white')
    vdlab2.pack(anchor='nw', padx=20, pady=10)
    
    vdlab3 = Label(frame_videolf, text='-해상도 : 1080x1920', bg=bg, fg='white')
    vdlab3.pack(anchor='nw', padx=20, pady=10)
    
    vdlab4 = Label(frame_videolf, text='-영상길이 : ~~~fps(0.00)', bg=bg, fg='white')
    vdlab4.pack(anchor='nw', padx=20, pady=10)

    frame_videorg = LabelFrame(frame_video, bg=bg) # 오른쪽 프레임
    frame_videorg.pack(fill='both', expand=True, side='right')

    videoimg = PhotoImage(file='./image/image.png', master=frame_videorg)
    videoimglab = Label(frame_videorg, image=videoimg, relief='flat') # 아나운서 이미지 라벨
    videoimglab.image = videoimg # 가비지 컬렉션 삭제 방지
    videoimglab.pack(anchor='center', pady=10) # **** 이미지에 따른 위치 수정 필요( 파일크기 확인하세요 )


    # 오디오 파일 프레임
    frame_audio = LabelFrame(frame1, bg=bg, text='생성', relief='groove',width=500, height=450, font=mainfont2, fg='white') # 메인 프레임
    frame_audio.pack(fill='both', expand=False)

    frame_audiolf = LabelFrame(frame_audio, bg=bg, relief='flat') # 왼쪽 프레임
    frame_audiolf.pack(fill='both', expand=True, side='left', padx=20)

    global adlab2, frame_audiorg,audioimglab
    bnad = Button(frame_audiolf, text='파일업로드', height=3, widt=25, bg=bnbg, fg='white', relief='flat',
                    command=get_select_file_therading).pack(pady=30)


    adlab1 = Label(frame_audiolf, text='   - 모델선택', bg=bg, fg='white').pack(anchor='nw',  pady=10)
    global model_select, create_select, loding, progressbar
    model_select = ttk.Combobox(frame_audiolf)
    model_select['values'] = ('선택해주세요.','AI_황이화','AI_추민선', 'AI 3(대기)', 'AI 4(대기)')
    model_select.current(0)
    model_select.pack()

    choselabal = Label(frame_audiolf, text='   - 생성 종류 선택', bg=bg, fg='white').pack(anchor='nw',  pady=10)

    create_select = ttk.Combobox(frame_audiolf)
    create_select['values'] = ('선택해주세요.', '음성', '비디오')
    create_select.current(0)
    create_select.pack()
    

    
    frame_audiorg = LabelFrame(frame_audio, bg=bg, width=400, height=500, text='진행상태', font=mainfont2, fg='white', labelanchor='n') # 오른쪽 프레임
    frame_audiorg.pack(fill='both', expand=True, side='right', padx=20, pady=80)

    progressbar = ttk.Progressbar(frame_audiorg, maximum=100, length=300)
    progressbar.pack(padx=30, pady=30)

    loding = Label(frame_audiorg, text='대기', bg=bg, fg='white')
    loding.pack(pady=10)
    

    newWindow.resizable(False, False)
    newWindow.mainloop()


if __name__ == '__main__':
    print(list(pkgutil.iter_modules()))
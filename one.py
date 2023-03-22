from threading import Thread
from threading import *
from tkinter import *
from tkinter import messagebox, filedialog, ttk
from tkinter.tix import COLUMN
import cv2, av, os, wave, subprocess, datetime, shutil, wave
import librosa, librosa.display
import matplotlib.pyplot as plt

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
    
    
def get_duration_audio(filename): # 오디오 정보 추출
    audio = wave.open(filename)
    frames = audio.getnframes()
    rate = audio.getframerate()
    seconds = frames/float(rate)
    adlab2.config(text='-오디오길이 : ' + f'{round(seconds,1)}초')


# -- 오디오 메인 스펙트럼 사진 변경 --
def get_audio_image(path, name):
    sig, sr = librosa.load(path, sr = 23500)
    plt.figure(figsize = (5.04,2.88))
    plt.axis('off')
    librosa.display.waveshow(sig, sr, color='white', alpha=1)
    plt.savefig(f'./image/{name}.png', facecolor=bg, pad_inches=0)
    
    
def audio_open(): # 오디오 파일 열기
    global audio_file_path
    audio_file_path = filedialog.askopenfilename(initialdir='', title='동영상 파일선택', filetypes=(
    ('wav files', '*.wav'), ('mp3 files', '*.mp3'), ('all files', '*.*')))
    try:
        get_duration_audio(audio_file_path)
        print(audio_file_path)
        name = 'audio'
        get_audio_image(audio_file_path, name)
        img_change = PhotoImage(file=f'./image/{name}.png', master=frame_audiorg)
        audioimglab.image = img_change
        audioimglab.configure(image=img_change)     
    except:
        messagebox.showinfo("오류", "파일을 선택해주세요.")


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
        text_edit(model_selects)
        final_ai()

    else:
        messagebox.showinfo("오류", "체크사항을 확인해주세요.")

# -- 최종 AI 모델 저장 경로 --
# def lipfake_path():
#     global ai_path
#     ai_path = filedialog.askdirectory()
#     print(ai_path)
#     fileload.config(text=ai_path)

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
        # outfile = ai_path+'/'+fake_filename.get()
        cmd = f'python lipfake/inference.py --checkpoint_path ./checkpoints/wav2lip_gan.pth --face {video_file_path} --audio ./TTSOUT/audio/file.wav --outfile ./TTSOUT/video/file.mp4 --resize_factor 2'
        loding.config(text='비디오 생성중...')
        print(cmd)
        subprocess.run(cmd)
 
        # start_Lab.config(text='최근작업 저장중...')   
        
        # -- 이미지 복사 --
        # path_dir = './save'
        # filecnt = os.listdir(path_dir)[:4]
        
        # vidcap2 = cv2.VideoCapture(video_file_path)
        # success,image = vidcap2.read()
        # success = True
        # resize_img2 = cv2.resize(image, (100,90))
        
        # if '1.png' not in filecnt:
        #     cv2.imwrite('./save/1.png', resize_img2)
        #     print('1')
            
        # elif '2.png' not in filecnt:
        #     cv2.imwrite('./save/2.png', resize_img2)
        #     print('2')
            
        # elif '3.png' not in filecnt:
        #     cv2.imwrite('./save/3.png', resize_img2)
        #     print('3')
            
        # elif '4.png' not in filecnt:
        #     cv2.imwrite('./save/4.png', resize_img2)
        #     print('4')

        # elif '4.png' in filecnt:
        #     cv2.imwrite('./save/5.png', resize_img2)
        #     os.remove('./save/1.png')

            # for i in range(len(filecnt)):
            #     src = os.path.join(path_dir, str(i+2)+'.png')
            #     dst = str(i+1) + '.png'
            #     dst = os.path.join(path_dir, dst)
            #     os.rename(src, dst)
        
    #     # -- 영상 복사 --
    #     video_path_dir = './save/video/'
    #     videocnt = os.listdir(video_path_dir)
        
    #     if 'save_1.mp4' not in videocnt:
    #         shutil.copy2(f'{outfile}.mp4', f'{video_path_dir}save_1.mp4')
            
    #     elif 'save_2.mp4' not in videocnt:
    #         shutil.copy2(f'{outfile}.mp4', f'{video_path_dir}save_2.mp4')
            
    #     elif 'save_3.mp4' not in videocnt:
    #         shutil.copy2(f'{outfile}.mp4', f'{video_path_dir}save_3.mp4')
            
    #     elif 'save_4.mp4' not in videocnt:
    #         shutil.copy2(f'{outfile}.mp4', f'{video_path_dir}save_4.mp4')

    #     elif 'save_4.mp4' in videocnt:
    #         shutil.copy2(f'{outfile}.mp4', f'{video_path_dir}save_5.mp4')
    #         os.remove('./save/video/save_1.mp4')
            
    #         for i in range(len(videocnt)):
    #             src = os.path.join(video_path_dir, f'save_{str(i+2)}.mp4')
    #             dst = f'save_{str(i+1)}.mp4'
    #             dst = os.path.join(video_path_dir, dst)
    #             os.rename(src, dst)
        
    #     befo_img = PhotoImage(file='./save/1.png', master=before_file_image)
    #     Label_test1.image = befo_img
    #     Label_test1.configure(image=befo_img)
        
    #     befo_img = PhotoImage(file='./save/2.png', master=before_file_image)
    #     Label_test2.image = befo_img
    #     Label_test2.configure(image=befo_img)

    #     befo_img = PhotoImage(file='./save/3.png', master=before_file_image)
    #     Label_test3.image = befo_img
    #     Label_test3.configure(image=befo_img)

    #     befo_img = PhotoImage(file='./save/4.png', master=before_file_image)
    #     Label_test4.image = befo_img
    #     Label_test4.configure(image=befo_img)
        
    #     video_dir = os.getcwd()
        
    #     Label_test4.image = befo_img
    #     Label_test4.configure(image=befo_img)
        
    #     Label_name1.config(text=fr"{video_dir}\save\video\{videocnt[0]}")
    #     Label_time1.config(text=f"{datetime.datetime.fromtimestamp(os.path.getmtime(video_path_dir+videocnt[0]))}")
        
    #     Label_name2.config(text=fr"{video_dir}\save\video\{videocnt[1]}")
    #     Label_time2.config(text=f"{datetime.datetime.fromtimestamp(os.path.getmtime(video_path_dir+videocnt[1]))}")
        
    #     Label_name3.config(text=fr"{video_dir}\save\video\{videocnt[2]}")
    #     Label_time3.config(text=f"{datetime.datetime.fromtimestamp(os.path.getmtime(video_path_dir+videocnt[2]))}")
        
    #     Label_name4.config(text=fr"{video_dir}\save\video\{videocnt[3]}")
    #     Label_time4.config(text=f"{datetime.datetime.fromtimestamp(os.path.getmtime(video_path_dir+videocnt[3]))}")
        
    #     start_Lab.config(text='생성 완료')
    except:
        messagebox.showinfo("오류", "오류")
        # start_Lab.config(text='파일 생성 오류')



def human_win(win, mainfont2):  # AI_HUMAN

    newWindow = Toplevel(win)
    newWindow.geometry('800x770')
    
    inco_frame = LabelFrame(newWindow, bg=bg, relief='flat')
    inco_frame.pack(fill='both', expand=False)

    Label(inco_frame, text='AI NEWS ROOM', bg=bg, fg='white', font=mainfont2).pack() # 타이틀
    Label(inco_frame, bg=bg, text='  ').pack(side='left') # 여백용
    Label(inco_frame, bg=bg, text='  ').pack(side='right')

    frame1 = LabelFrame(inco_frame, bg=bg, relief='flat',width=800, height=150)
    frame1.pack(fill='both', expand=True, side='left')

    # frame2 = LabelFrame(inco_frame, bg=bg, relief='flat',width=800, height=150)
    # frame2.pack(fill='both', expand=True, side='right')

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
    

    # audioimg = PhotoImage(file='./image/audio.png', master=frame_videorg)
    # audioimglab = Label(frame_audiorg, image=audioimg) # 소리 음파 이미지 라벨
    # audioimglab.image = audioimg # 가비지 컬렉션 삭제 방지
    # audioimglab.pack(anchor='center', pady=10) # **** 이미지에 따른 위치 수정 필요( 파일크기 확인하세요 )

    # ai 관
    # 리
    # frame_ai = LabelFrame(frame1, bg=bg, text='ai', relief='groove',
    #                         width=500, height=150, font=mainfont2, fg='white')
    # frame_ai.pack(fill='both', expand=True)
    # ai_btn1 = Button(frame_ai, text='최근파일열기', height=3, width=25, bg=bnbg, fg='white', relief='flat')
    # ai_btn1.place(relx=0.08, rely=0.15)
    # ai_btn2 = Button(frame_ai, text='프로젝트열기', height=3, width=25, bg=bnbg, fg='white', relief='flat')
    # ai_btn2.place(relx=0.38, rely=0.15)
    # ai_btn3 = Button(frame_ai, text='프로젝트저장', height=3, width=25, bg=bnbg, fg='white', relief='flat')
    # ai_btn3.place(relx=0.68, rely=0.15)


    # -- 작업진행 --
    # frame_start = LabelFrame(frame2, bg=bg, text='작업진행', relief='groove',
    #                         width=5000, height=20, font=mainfont2, fg='white')
    # frame_start.pack(expand=False, fill="both")

    # frame_startbom = LabelFrame(frame_start, bg=bg, relief='flat')
    # frame_startbom.pack(fill='both', expand=False, side='bottom', pady=10) # 하단프레임
    
    # start_btn = Button(frame_startbom, text='합성시작', bg=bnbg, fg='white', height=3, width=110, relief='flat', command=final_ai_therading)
    # start_btn.pack()
    
    # global start_Lab
    # start_Lab = Label(frame_startbom, text='시작대기중', bg=bg, fg='white', relief='groove',height=2, width=110)
    # start_Lab.pack()

    # frame_startle = LabelFrame(frame_start, bg=bg, relief='flat')
    # frame_startle.pack(fill='both', expand=False, side='left', pady=10) # 왼쪽프레임
    
    # Last1 = Label(frame_startle, bg=bg, text='저장경로', fg='white').pack(anchor='nw', padx=20, pady=3)
    # Last1 = Label(frame_startle, bg=bg, text='저장파일이름', fg='white').pack(anchor='nw', padx=20, pady=3)

    # frame_startrg = LabelFrame(frame_start, bg=bg, relief='flat')
    # frame_startrg.pack(fill='both', expand=True, side='right', pady=10) # 오른쪽프레임
    
    # global fileload, fake_filename

    # fileload = Label(frame_startrg, text='', bg=bg, fg='white')
    # fileload.grid(row=0, column=0, padx=5, pady=3, columnspan=5, sticky=W) # 저장경로
    
    # btnfile_load = Button(frame_startrg, width=8, bg=bnbg, text='...', relief='flat', fg='white', command=lipfake_path)
    # btnfile_load.grid(row=0, column=5, padx=3, pady=2)
    
    # fake_filename = Entry(frame_startrg, width = 30)
    # fake_filename.grid(row=1, column=0, padx=5, pady=3, columnspan=6, sticky='NEWS') # 저장파일이름

    # # 최근결과물
    # before_frame = LabelFrame(frame2, bg=bg, text='최근결과물', relief='groove',
    #                         width=500, height=20, font=mainfont2, fg='white')
    # before_frame.pack(fill='both', expand=True) # DB 작업 이후에 만들 것(DB에서 데이터 가져와야함)
    
    # global before_file_image
    # before_file_image = Frame(before_frame, bg=bg, width=150, height=550)
    # before_file_image.pack(side='left', expand=True)

    # before_file_text = Frame(before_frame, bg=bg, width=300, height=550)
    # before_file_text.pack(side='right', expand=True)


    # global Label_test1, Label_test2, Label_test3, Label_test4
    # # 최근 이미지 파일
    # img = PhotoImage(file='./save/1.png', master=before_file_image)
    # Label_test1 = Label(before_file_image, bg=bg, pady=50, padx=60, image=img)
    # Label_test1.image = img
    # Label_test1.grid(row=0, column=0)
    
    # Label(before_file_image, bg=bg, pady=3).grid(row=1)
    
    # img = PhotoImage(file='./save/2.png', master=before_file_image)
    # Label_test2 = Label(before_file_image, bg=bg, pady=50, padx=60, image=img)
    # Label_test2.image = img 
    # Label_test2.grid(row=2, column=0)
    # Label(before_file_image, bg=bg, pady=3).grid(row=3)
    
    
    # img = PhotoImage(file='./save/3.png', master=before_file_image)
    # Label_test3 = Label(before_file_image, bg=bg, pady=50, padx=60, image=img)
    # Label_test3.image = img
    # Label_test3.grid(row=4, column=0)
    # Label(before_file_image, bg=bg, pady=3).grid(row=5)
    
    
    # img = PhotoImage(file='./save/4.png', master=before_file_image)
    # Label_test4 = Label(before_file_image, bg=bg, pady=50, padx=60, image=img)
    # Label_test4.image = img
    # Label_test4.grid(row=6, column=0)


    # global Label_name1, Label_name2, Label_name3, Label_name4
    # global Label_time1, Label_time2, Label_time3, Label_time4

    
    
    # # 최근 저장경로 및 파일 이름 // 저장 날짜
    # video_dir = os.getcwd()
    
    # save_dir_path = './save/video/'
    # save_dir_path_file = os.listdir(save_dir_path)
    
    # Label_name1 = Label(before_file_text, bg=bg, pady=13, padx=5, fg=fg,
    #                     text=fr'{video_dir}\save\video\{save_dir_path_file[0]}.mp4')
    # Label_name1.grid(row=1, column=0, sticky='nw')
    # Label_time1 = Label(before_file_text, bg=bg, pady=15, padx=5, fg=fg,
    #                     text=f'{datetime.datetime.fromtimestamp(os.path.getmtime(save_dir_path+save_dir_path_file[0]))}')
    # Label_time1.grid(row=2, column=0, sticky='nw')    
    # Label(before_file_text, bg=bg, pady=2, padx=180).grid(row=3)
    
    
    # Label_name2 = Label(before_file_text, bg=bg, pady=13, padx=5, fg=fg,
    #                     text=fr'{video_dir}\save\video\{save_dir_path_file[1]}.mp4')
    # Label_name2.grid(row=4, column=0, sticky='nw')
    # Label_time2 = Label(before_file_text, bg=bg, pady=15, padx=5, fg=fg,
    #                     text=f'{datetime.datetime.fromtimestamp(os.path.getmtime(save_dir_path+save_dir_path_file[1]))}')
    # Label_time2.grid(row=5, column=0, sticky='nw')
    # Label(before_file_text, bg=bg, pady=3).grid(row=6)
    
    
    # Label_name3 = Label(before_file_text, bg=bg, pady=13, padx=5, fg=fg, 
    #                     text=fr'{video_dir}\save\video\{save_dir_path_file[2]}.mp4')
    # Label_name3.grid(row=7, column=0, sticky='nw')
    # Label_time3 = Label(before_file_text, bg=bg, pady=15, padx=5, fg=fg,
    #                     text=f'{datetime.datetime.fromtimestamp(os.path.getmtime(save_dir_path+save_dir_path_file[2]))}')
    # Label_time3.grid(row=8, column=0, sticky='nw')
    # Label(before_file_text, bg=bg, pady=2).grid(row=9)
    
    
    # Label_name4 = Label(before_file_text, bg=bg, pady=13, padx=5, fg=fg,
    #                     text=fr'{video_dir}\save\video\{save_dir_path_file[3]}.mp4')
    # Label_name4.grid(row=10, column=0, sticky='nw')
    # Label_time4 = Label(before_file_text, bg=bg, pady=15, padx=5, fg=fg,
    #                     text=f'{datetime.datetime.fromtimestamp(os.path.getmtime(save_dir_path+save_dir_path_file[3]))}')
    # Label_time4.grid(row=11, column=0, sticky='nw')

    newWindow.resizable(False, False)
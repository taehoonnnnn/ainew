from threading import *
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os, re, subprocess, glob
from num2words import num2words as nws
import soundfile as sf
import numpy as np

# 숫자 -> 한글 변환
def num_kr_change(item):
    item_return = []
    run = []
    
    if re.findall("\d+", item) != []:
        item_num_list = re.findall("\d+", item)
        
        for i in item_num_list:
            run1 = ''.join(i)
            run.append(int(run1))
            run2 = sorted(run, reverse=True)
        
        for i in range(len(item_num_list)):
            # run3 = sorted(run, reverse=True)
            item_return.append(nws(run2[i], lang='ko'))
            item = item.replace(str(run2[i]), item_return[i])
    return item



# 텍스트 활성화
def getTextInput(): # input_text 가져올 함수
    from tts_model import input_text
    result=input_text.get("1.0","end") # 문자열 1.0위치 부터 ~ end
    print(result)# result 값사용
    
# 텍스트 불러오기
def getText():
    from tts_model import input_text, loding
    try:
        try:
            file = filedialog.askopenfilename(initialdir='/', title='Select file', defaultextension='.txt',
                                        filetypes=(("text files", "*.txt"),("all files", "*.*")))
            f = open(file, 'rt', encoding='cp949')
            input_text.delete('1.0', END)
            input_text.insert(END,f.read())
            loding.config(text = '텍스트 불러오기 성공')
        except:
            f = open(file, 'rt', encoding='utf-8')
            input_text.delete('1.0', END)
            input_text.insert(END,f.read())
            loding.config(text = '텍스트 불러오기 성공')         
    except:
        loding.config(text = '텍스트 불러오기 에러')
   

# 텍스트 저장 
def save():
    from tts_model import input_text, loding
    try:
        file = filedialog.asksaveasfile(title= 'file save', mode='w', defaultextension=".txt",
                                        filetypes=(("text files", "*.txt"),("all files", "*.*")))
        if file != None:
            lines = input_text.get('1.0', 'end') # 마지막에서 1 char 뺀다, \n제거!
            file.write(lines)
            file.close()
            loding.config(text = '텍스트 저장 성공')
    except:
        messagebox.showinfo('에러', '에러')
    #     loding.config(text = '텍스트 저장 성공')         



# Thread 사용
def edit_therading():
    try:
        t1 = Thread(target = text_edit)
        t1.daemon = True
        t1.start()
    except:
        print(f'Thread error : {t1}')


def text_edit(model_select):
    from one import loding, progressbar
    # try:
    test2 = []
    tts_text = []
    
    file = filedialog.askopenfilename(initialdir='/', title='Select file', defaultextension='.txt',
                                filetypes=(("text files", "*.txt"),("all files", "*.*")))
    
    try:
        f = open(file, 'r', encoding='cp949')
        txt_file = f.readlines()
        print('cp949')
    except:
        f = open(file, 'r', encoding='utf-8')
        txt_file = f.readlines()
        print('utf-8')
        
    loding.config(text = '음성 생성 시작')

    for i in range(len(txt_file)):
        a = (txt_file[i])
        del_t = a
        
        # if del_t2.find('니다') != -1:
        #     sp_text = del_t2.index('다.')+2 # 개행 위치
        #     del_t = del_t2[:sp_text] # 전처리 문자열 반환
        #     del_t2 = del_t2[sp_text+1:] # 개행된 문자 외 나머지 반환
            
        # else :
        #     del_t = del_t2
    
        if del_t[0] == ' ': # 문자열 start 공백 제거
            del_t = del_t[1:]
            

        # if del_t in '다.':
        #     del_t.split()
        # loding.config(text = f'{del_t} - 음성 생성 진행중')
        
        # if ', ' or ' ' not in del_t:
            # del_t = list(del_t)
            # del_t = del_t.replace(',',' ')
            # del_t = del_t.replace('.','')
        
        if '  ' in del_t:
            del_t = del_t.replace('  ',' ')
        
        
        del_t = del_t.replace('kg','킬로그램')
        del_t = del_t.replace('cm','센티미터')
        del_t = del_t.replace('km','킬로미터')
        del_t = del_t.replace('mm','밀리미터')
        del_t = del_t.replace('%', '퍼센트')
        del_t = del_t.replace('·', ' ')
        
        
        del_t = del_t.replace('“','')
        
        del_t = del_t.replace('. ',' ')
            
        del_t = del_t.replace('.','쩜')
        
        # del_t = del_t.replace(',','')
        del_t = del_t.replace('"','')
        del_t = del_t.replace('  ',' ')
        # del_t = del_t.replace("'",'')
        del_t = del_t.strip('\n')
        del_t = del_t.strip('\t')
        
        
        del_t = del_t.replace('A', '에이')
        del_t = del_t.replace('B', '비')
        del_t = del_t.replace('C', '씨')
        del_t = del_t.replace('D', '디')
        del_t = del_t.replace('E', '이')
        del_t = del_t.replace('F', '에프')
        del_t = del_t.replace('G', '지')
        del_t = del_t.replace('H', '에이치')
        del_t = del_t.replace('I', '아이')
        del_t = del_t.replace('J', '제이')
        del_t = del_t.replace('K', '케이')
        del_t = del_t.replace('L', '앨')
        del_t = del_t.replace('M', '엠')
        del_t = del_t.replace('N', '엔')
        del_t = del_t.replace('O', '오')
        del_t = del_t.replace('P', '피')
        del_t = del_t.replace('Q', '큐')
        del_t = del_t.replace('R', '알')
        del_t = del_t.replace('S', '에스')
        del_t = del_t.replace('T', '티')
        del_t = del_t.replace('U', '유')
        del_t = del_t.replace('V', '브이')
        del_t = del_t.replace('W', '더블유')
        del_t = del_t.replace('X', '엑스')
        del_t = del_t.replace('Y', '와이')
        del_t = del_t.replace('Z', '제트')
        
        del_t = del_t.replace('a', '에이')
        del_t = del_t.replace('b', '비')
        del_t = del_t.replace('c', '씨')
        del_t = del_t.replace('d', '디')
        del_t = del_t.replace('e', '이')
        del_t = del_t.replace('f', '에프')
        del_t = del_t.replace('g', '지')
        del_t = del_t.replace('h', '에이치')
        del_t = del_t.replace('i', '아이')
        del_t = del_t.replace('j', '제이')
        del_t = del_t.replace('k', '케이')
        del_t = del_t.replace('l', '앨')
        del_t = del_t.replace('m', '엠')
        del_t = del_t.replace('n', '엔')
        del_t = del_t.replace('o', '오')
        del_t = del_t.replace('p', '피')
        del_t = del_t.replace('q', '큐')
        del_t = del_t.replace('r', '알')
        del_t = del_t.replace('s', '에스')
        del_t = del_t.replace('t', '티')
        del_t = del_t.replace('u', '유')
        del_t = del_t.replace('v', '브이')
        del_t = del_t.replace('w', '더블유')
        del_t = del_t.replace('x', '엑스')
        del_t = del_t.replace('y', '와이')
        del_t = del_t.replace('z', '제트')

        # if del_t[-1:] == ' ':
        #     del_t = del_t[:len(del_t)-1]
        
        if del_t[-1:] == ' ':
            del_t = del_t[:-1]
        
        if del_t[0] == ' ':
            del_t = del_t[1:]
            
        if del_t[-1:] == '쩜':
            del_t = del_t[:-1]
            
        test2.append(del_t[:])       
            
    for i in test2:
        tts_text.append(num_kr_change(i))
    
    tts_text_cnt = 1
    
    # model_sel = model_select.get()
    # 단일화자
    # if model_sel == 'AI_황이화':
    #     models = 'model_1'
    # elif model_sel == 'AI_추민선':
    #     models = 'model_2'

    # 다중화자
    if model_select == 'AI_황이화':
        models = '1'
    elif model_select == 'AI_추민선':
        models = '0'
    print(models)
    
    for i in tts_text:
        # 단일화자
        # cmd = f'python audio_create/synthesizer.py --load_path audio_create/model/{models} --sample_path sample --text "{i}"'
        # 다중화자
        cmd = f'python audio_create/synthesizer.py --load_path audio_create/model/1and2 --num_speaker 2 --speaker_id {models} --sample_path sample --text "{i}"'
        subprocess.run(cmd)
        print(f'{i} - 오디오 생성 진행중')
        cnt = (tts_text_cnt/len(tts_text))*100
        loding.config(text = f'진행률 - {int(cnt)}%')
        progressbar['value'] = int(cnt)
        progressbar.update()
        tts_text_cnt += 1
        
    print('파일 이름 변경 시작')
    paths = glob.glob('./sample/**', recursive=True)

    exts = ('png', 'jpg', 'txt', 'mp4') # 폴더에 해당 확장자 파일 삭제
    for path in paths:
        if any(ext in path for ext in exts):
            os.remove(path)


    path = "./sample" # 오디오 파일 저장 경로
    file_names = os.listdir(path)
    file_names

    str_cnt = 1
    for name in file_names:
        src = os.path.join(path, name)
        dst = str(str_cnt) + '.wav'
        dst = os.path.join(path, dst)
        os.rename(src, dst)
        str_cnt += 1

    # ------------------------ 개별 생성시 여기서부터 주석 -------------------------        
    # -- 오디오 생성 부 --
    audio_list = [] # 합칠 오디오 파일 리스트
    sample_rate = 24000
    filecnt = os.listdir('./sample/')

    # -- 파일마다 1초의 간격 추가 --
    for i in range(len(filecnt)):
        x, sr = sf.read(f'./sample/{i+1}.wav')
        y, sr = sf.read(f'./TTSOUT/1sec/1sec.wav')
        x = np.concatenate((x,y),axis=0)
        sf.write(f'./TTSOUT/audio_{i+1}.wav', x, sample_rate)

    # -- 전체 오디오 결합 --    
    for i in range(len(filecnt)):
        cnt, sr = sf.read(f'./TTSOUT/audio_{i+1}.wav')
        audio_list.append(cnt)

    audio_list = np.concatenate((audio_list), axis=0)
    
    name = 'file'
    print(name)
    
    sf.write(f'./TTSOUT/audio/{name}.wav', audio_list, sample_rate)

    # -- 생성된 파일 삭제 --
    [os.remove(f) for f in glob.glob('./TTSOUT/*.wav')]
    [os.remove(f) for f in glob.glob('./sample/*.wav')]
    
    print("오디오 생성완료")
    loding.config(text = '음성 생성 완료')
    
    # 다음 프로그래밍을 위해 초기화
    txt_file = ''
    tts_text = []
    f.close()
# except:
    messagebox.showinfo('에러', '에러')
    loding.config(text = '음성 생성')
    [os.remove(f) for f in glob.glob('./TTSOUT/*.wav')]
    [os.remove(f) for f in glob.glob('./sample/*.wav')]
    f.close()

    # ----------------------------------------------------------------------
import mediapipe as mp
import pyautogui as p
import cv2
import speech_recognition
from gtts import gTTS
import os
def record_voice():
	microphone = speech_recognition.Recognizer()

	with speech_recognition.Microphone() as live_phone:
		microphone.adjust_for_ambient_noise(live_phone)

		print("I'm trying to hear you: ")
		audio = microphone.listen(live_phone)
		try:
			phrase = microphone.recognize_google(audio, language='en')
			return phrase
		except speech_recognition.UnkownValueError:
			return "I didn't understand what you said"

p.sleep(5)
p.doubleClick(200,400)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS,1)

hd=mp.solutions.hands.Hands()
drawing_utils=mp.solutions.drawing_utils
#t=100
sw,sh=p.size()
iy=0
while 1:

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_hight,frame_width,_=frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    op=hd.process(rgb_frame)

    hands = op.multi_hand_landmarks
    if hands:
        for hand in hands[:1]:
            drawing_utils.draw_landmarks(frame,hand)
            landmarks =hand.landmark
            for id, landmark in enumerate(landmarks):

                x=int(landmark.x*frame_width)
                y=int(landmark.y*frame_hight)
                #print(x,y)

                if id == 8:
                    cv2.circle(img= frame, center=(x,y),radius=10,color=(0,222,0))
                    ix=sw/frame_width*x
                    iy=sh/frame_hight*y
                    p.moveTo(ix*1.2,iy*1.2)

                if id == 12:
                    cv2.circle(img= frame, center=(x,y),radius=10,color=(0,222,0))
                    tx=sw/frame_width*x
                    ty=sh/frame_hight*y
                    #print('outside', abs(iy - ty))# print cordinartes
                    print("ld diff",abs(ix - tx))
                    if abs(ix - tx)<20 : #and abs(iy-ty)<20
                        p.leftClick()
                        p.click()
                        p.sleep(1)
                        print("  left   click")


                if id == 16:
                    cv2.circle(img= frame, center=(x,y),radius=10,color=(0,285,0))
                    cx=sw/frame_width*x
                    cy=sh/frame_hight*y
                    print("rd diff",abs(tx - cx))
                    if abs(tx - cx)<30 : #and or abs(ty-cy)<20
                        p.rightClick();
                        p.sleep(1)
                        print("   right      click")
                if id ==20:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 285, 0))
                    tix = sw / frame_width * x
                    tiy = sh / frame_hight * y

                    print('scroll diff is ',abs(tix-cx))
                    if abs(tix-cx)<40:
                        print("----scrolled----- ")
                        p.scroll(-999)
                #bilow code for keyboard opening
                if id == 6:

                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 285, 0))
                    ttx = sw / frame_width * x
                    tty = sh / frame_hight * y
                    print( " -----   text to speech ",abs(tty - iy))
                    if abs(tty - iy) < 20:
                       # p.hotkey("ctrl", "Win", "o")
                        print("--     -text to speech and speech to text           --")
                        p.click(x,y)
                        p.sleep(5)
                        phrase = record_voice()

                        with open('yst.txt', 'w') as file:
                            file.write(phrase)
                        print('the last sentence you spoke was saved in you_said_this.txt')
                        file = open("yst.txt", "r").read()

                        speech = gTTS(text=file, lang='en', slow=False)
                        speech.save("voice.mp3")
                        print(os.system('voice.mp3'))
                        print("last")



        #print(hands)
    cv2 . imshow('virtualMouse', frame)
    cv2.waitKey(1)

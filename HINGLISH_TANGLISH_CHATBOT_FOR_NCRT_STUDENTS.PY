import sys
import sympy as sp
import wikipedia
from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox,
    QTextEdit, QPushButton, QVBoxLayout, QFileDialog
)

x = sp.symbols('x')

# -----------------------------
# MATH ENGINE
# -----------------------------

def solve_math(question):

    try:

        q = question.lower().replace("^","**")

        if "derivative" in q:

            expr = q.replace("derivative of","")

            return str(sp.diff(sp.sympify(expr),x))

        if "=" in q:

            left,right=q.split("=")

            eq=sp.Eq(sp.sympify(left),sp.sympify(right))

            return str(sp.solve(eq,x))

        result=sp.sympify(q)

        return str(sp.simplify(result))

    except:
        return None


# -----------------------------
# WIKIPEDIA
# -----------------------------

def wiki_search(q):

    try:
        wikipedia.set_lang("en")
        return wikipedia.summary(q, sentences=3)
    except:
        return "No theory found"


# -----------------------------
# ANSWER ROUTER
# -----------------------------

def get_answer(subject,question):

    m=solve_math(question)

    if subject=="Mathematics" and m:
        return m

    return wiki_search(question)


# -----------------------------
# PDF READER
# -----------------------------

def read_pdf_text(path):

    reader=PdfReader(path)

    text=""

    for page in reader.pages:

        t=page.extract_text()

        if t:
            text+=t+"\n"

    return text


# -----------------------------
# OCR
# -----------------------------

def read_pdf_ocr(path):

    images=convert_from_path(path)

    text=""

    for img in images:

        text+=pytesseract.image_to_string(img)

    return text


# -----------------------------
# SOLVE PDF QUESTIONS
# -----------------------------

def solve_pdf(path):

    text=read_pdf_text(path)

    if not text.strip():

        text=read_pdf_ocr(path)

    lines=text.split("\n")

    answers=[]

    for line in lines:

        result=solve_math(line)

        if result:

            answers.append(f"{line} = {result}")

    if not answers:
        return "No math detected"

    return "\n".join(answers)


# -----------------------------
# SPEECH
# -----------------------------

def listen_question():

    r=sr.Recognizer()

    with sr.Microphone() as source:

        audio=r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return "Speech not recognized"


# -----------------------------
# UNIVERSAL DIAGRAM ENGINE
# -----------------------------

def draw_diagram(topic):

    topic=topic.lower()

    plt.figure()

# -----------------------------
# MATH
# -----------------------------

    if "triangle" in topic:

        pts=np.array([[0,0],[4,0],[2,3],[0,0]])

        plt.plot(pts[:,0],pts[:,1],marker='o')

        plt.title("Triangle")

    elif "square" in topic:

        pts=np.array([[0,0],[3,0],[3,3],[0,3],[0,0]])

        plt.plot(pts[:,0],pts[:,1],marker='o')

        plt.title("Square")

    elif "circle" in topic:

        t=np.linspace(0,2*np.pi,200)

        plt.plot(np.cos(t),np.sin(t))

        plt.gca().set_aspect('equal')

        plt.title("Circle")

    elif "parabola" in topic:

        x=np.linspace(-10,10,200)

        y=x**2

        plt.plot(x,y)

        plt.title("Parabola")

    elif "sine" in topic:

        x=np.linspace(0,10,200)

        plt.plot(x,np.sin(x))

        plt.title("Sine Wave")

    elif "cosine" in topic:

        x=np.linspace(0,10,200)

        plt.plot(x,np.cos(x))

        plt.title("Cosine Wave")

# -----------------------------
# PHYSICS
# -----------------------------

    elif "vector" in topic:

        plt.quiver(0,0,4,3)

        plt.title("Vector")

    elif "free body" in topic:

        plt.scatter(0,0)

        plt.quiver(0,0,2,0)
        plt.quiver(0,0,0,2)
        plt.quiver(0,0,-2,0)

        plt.title("Free Body Diagram")

    elif "projectile" in topic:

        x=np.linspace(0,10,100)

        y=x-0.1*x**2

        plt.plot(x,y)

        plt.title("Projectile Motion")

    elif "electric field" in topic:

        x,y=np.meshgrid(np.linspace(-5,5,20),np.linspace(-5,5,20))

        u=x/(x**2+y**2+1)

        v=y/(x**2+y**2+1)

        plt.quiver(x,y,u,v)

        plt.title("Electric Field")

# -----------------------------
# ELECTRONICS
# -----------------------------

    elif "circuit" in topic:

        plt.plot([0,2],[0,0])
        plt.plot([2,4],[0,0])
        plt.scatter([0,4],[0,0])

        plt.text(2,0.2,"Resistor")

        plt.title("Simple Circuit")

# -----------------------------
# CHEMISTRY
# -----------------------------

    elif "benzene" in topic:

        theta=np.linspace(0,2*np.pi,7)

        x=np.cos(theta)

        y=np.sin(theta)

        plt.plot(x,y)

        for i in range(6):

            plt.text(x[i],y[i],"C")

        plt.gca().set_aspect('equal')

        plt.title("Benzene Ring")

    elif "atom" in topic:

        circle1=plt.Circle((0,0),1,fill=False)

        circle2=plt.Circle((0,0),2,fill=False)

        ax=plt.gca()

        ax.add_patch(circle1)
        ax.add_patch(circle2)

        plt.scatter([1,-1],[0,0])

        plt.text(0,0,"Nucleus")

        plt.title("Atom Model")

    elif "molecule" in topic:

        x=[0,1,2]

        y=[0,0,0]

        plt.plot(x,y,marker='o')

        plt.text(0,0,"H")
        plt.text(1,0,"O")
        plt.text(2,0,"H")

        plt.title("Water Molecule")

    else:

        plt.text(0.3,0.5,"Diagram not recognized")

    plt.grid()

    plt.show()


# -----------------------------
# UI
# -----------------------------

class TutorApp(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("NCERT AI Tutor")

        self.setGeometry(300,150,700,700)

        layout=QVBoxLayout()

        layout.addWidget(QLabel("Class"))

        self.class_box=QComboBox()

        for i in range(1,13):
            self.class_box.addItem(f"Class {i}")

        layout.addWidget(self.class_box)

        layout.addWidget(QLabel("Subject"))

        self.subject_box=QComboBox()

        self.subject_box.addItems([
        "Mathematics","Physics","Chemistry","Biology","History"
        ])

        layout.addWidget(self.subject_box)

        layout.addWidget(QLabel("Question"))

        self.question=QTextEdit()

        layout.addWidget(self.question)

        ask_btn=QPushButton("Get Answer")

        ask_btn.clicked.connect(self.process_question)

        layout.addWidget(ask_btn)

        speech_btn=QPushButton("Speak")

        speech_btn.clicked.connect(self.speech_input)

        layout.addWidget(speech_btn)

        pdf_btn=QPushButton("Upload PDF")

        pdf_btn.clicked.connect(self.process_pdf)

        layout.addWidget(pdf_btn)

        diagram_btn=QPushButton("Draw Diagram")

        diagram_btn.clicked.connect(self.show_diagram)

        layout.addWidget(diagram_btn)

        layout.addWidget(QLabel("Answer"))

        self.answer=QTextEdit()

        layout.addWidget(self.answer)

        self.setLayout(layout)


    def process_question(self):

        subject=self.subject_box.currentText()

        q=self.question.toPlainText()

        ans=get_answer(subject,q)

        self.answer.setText(ans)


    def process_pdf(self):

        file,_=QFileDialog.getOpenFileName(self,"Open PDF","","PDF Files (*.pdf)")

        if file:

            result=solve_pdf(file)

            self.answer.setText(result)


    def speech_input(self):

        text=listen_question()

        self.question.setText(text)


    def show_diagram(self):

        topic=self.question.toPlainText()

        draw_diagram(topic)


# -----------------------------
# RUN
# -----------------------------

app=QApplication(sys.argv)

window=TutorApp()

window.show()

sys.exit(app.exec())
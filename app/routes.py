from scrapy import Selector
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, addQuestionFrom, Quiz, makeQuiz, doQuizFrom
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Question, QuizSet,QuizSetList
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)


    return render_template("login.html", title='Login In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, admin=True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)

@app.route('/questions',methods=['GET', 'POST'])
def questions():
    qa = Question.query.all()

    #db.session.delete(note)
    #db.session.commit()
    return render_template("questions.html",data=qa)

@app.route('/addQuestions',methods=['GET', 'POST'])
def addQuestions():
    form = addQuestionFrom()
    if form.validate_on_submit():
        question1 = form.question.data
        answer1 = form.answer.data
        q = Question(question=question1, answer=answer1)
        #print(q.question,q.answer)
        db.session.add(q)
        db.session.commit()
        flash('Congratulations, you are now add one question in data set!')
        return redirect(url_for('questions'))
    return render_template("addQuestions.html",title="AddQuesion",form=form)




@app.route('/makeQuiz',methods=['GET', 'POST'])
def makeQuiz():
    data = Question.query.all()
    list_quizId = request.form.getlist('quiz')
    #if form.validate_on_submit():
    question=""
    answer=""
    for id in list_quizId:
        question = question+","+Question.query.get(int(id)).question
        answer = answer+","+Question.query.get(int(id)).answer
    q = QuizSet(question=question,answer=answer)
    db.session.add(q)
    db.session.commit()
    if request.method == 'POST':
        flash("Successfully make a new quizSet")
        return redirect(url_for("quizset"))
    return render_template("makeQuiz.html",data=data)

@app.route('/users')
def users():
    data = User.query.all()
    return render_template("users.html", data=data)

@app.route('/quizset')
def quizset():
    data = QuizSet.query.all()
    data = list(data)
    for i in range(len(data)-1,-1,-1):
        if data[i].question == "":
            data.remove(data[i])

    return render_template("quizset.html", data=data)



@app.route('/quiz',methods=['GET', 'POST'])
def quiz():
    form = Quiz()
    data = QuizSet.query.filter(QuizSet.release==True)
    data=list(data)
    for i in range(len(data)-1,-1,-1):
        id_str = str(data[i].completed_by_user)
        id_list = id_str.split(",")
        for a in id_list:
            if a =="":
                id_list.remove(a)
        #print(str(current_user.id),id_list)
        if str(current_user.id) in id_list:
            data.remove(data[i])
    #if d.userid == current_user.id and d.completed == True:
    #user_list=[]
    #question_list=[]
    #for dd in data1:
       #question_list.append(dd.question)
    #print(sorted(set(question_list)))
    #for ql in  sorted(set(question_list)):
        #ul=[]
        #for dd in data1:
            #if dd.question == ql:
                #ul.append(dd.userid)
        #user_list.append(ul)
    #print(user_list)
    #for j in range(len(user_list)):
        #for i in range(length1-1,-1,-1):
            #if current_user.id in user_list[j]:
                #data1.remove(data1[i])
    length = 0
    for num in data:
        length = length +1
    return render_template("quiz.html", data=data, form=form, length=length)

@app.route('/doQuiz/<id>/',methods=['GET', 'POST'])
def doQuiz(id):
    form = doQuizFrom()
    data = QuizSet.query.get(id)
    questions = data.question
    questions_list = questions.split(",")
    for q in questions_list:
        if q=="":
            questions_list.remove(q)
    current_id = current_user.id
    if form.validate_on_submit():
        useranswers = request.form.getlist('useranswer')
        #print(useranswers)
        useranswers_str=""
        for ua in useranswers:
            if ua=="":
                ua="giveup"
            useranswers_str=useranswers_str+ua+","

        qz = QuizSetList(question = questions,
                     answer=data.answer,
                     useranswer = useranswers_str,
                     userid = current_id,
                     completed = True,
                     quzisetid=id)

        db.session.add(qz)
        db.session.commit()

        id_str = str(data.completed_by_user)
        id_str = id_str + str(current_user.id)+","
        data.completed_by_user = id_str
        db.session.commit()
        return redirect(url_for("quiz"))
    return render_template("doQuiz.html",questions_list=questions_list, form=form)


@app.route('/updateQuestion', methods=['GET', 'POST'])
def updateQuestion():
    if request.method == 'POST':
        my_data = Question.query.get(request.form.get('id'))
        my_data.qusetion = request.form.get("question")
        my_data.answer = request.form.get("answer")
        db.session.commit()
        flash(" Updated Successfully")

        return redirect(url_for('questions'))


@app.route('/deleteQuestion/<id>/', methods=['GET', 'POST'])
def deleteQuestion(id):
    my_data = Question.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash(" Deleted Successfully")

    return redirect(url_for('questions'))

@app.route('/deleteUser/<id>/', methods=['GET', 'POST'])
def deleteUser(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash(" Deleted Successfully")
    return redirect(url_for('users'))

@app.route('/deleteQuizset/<id>/', methods=['GET', 'POST'])
def deleteQuizset(id):
    my_data = QuizSet.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash(" Deleted Successfully")
    return redirect(url_for('quizset'))

@app.route('/Publish/<id>/', methods=['GET', 'POST'])
def Publish(id):
    my_data = QuizSet.query.get(id)
    my_data.release = True
    db.session.commit()

    flash(" Post Successfully")
    return redirect(url_for('quizset'))

@app.route('/Unpublish/<id>/', methods=['GET', 'POST'])
def Unpublish(id):
    my_data = QuizSet.query.get(id)
    my_data.release = False
    db.session.commit()

    flash(" Decline Successfully ")
    return redirect(url_for('quizset'))


@app.route('/mark', methods=['GET', 'POST'])
def mark():
    data1 = QuizSetList.query.filter(QuizSetList.completed==True)
    data = list(data1)
    l = len(data)
    for i in range(l-1,-1,-1):
        if data[i].marked == True or data[i].userid == None:
            data.remove(data[i])

    #print(data)
    QandA_list = []
    for d in data:
        #print(d.userid)
        #print(d.userid,d.id,d.question,d.useranswer)
        question_list=d.question.split(",")
        answer_list = d.answer.split(",")
        useranswer_list = d.useranswer.split(",")
        for i in question_list:
            if i == "":
                question_list.remove(i)
        for i in answer_list:
            if i == "":
                answer_list.remove(i)
        for i in useranswer_list:
            if i == "":
                useranswer_list.remove(i)
        pair = []
        uid = []
        qid = []
        uid.append(d.userid)
        qid.append(d.id)
        pair.append(uid)
        pair.append(qid)
        pair.append(question_list)
        pair.append(useranswer_list)
        pair.append(answer_list)
        pair.append(len(question_list))
        QandA_list.append(pair)
    #print(QandA_list)
    if request.method == 'POST':
        id_str = request.form.get('id')
        leng = len(id_str)
        id_str=id_str[1:leng-1]
        my_data = QuizSetList.query.get(id_str)
        score = request.form.getlist("score")
        feedback = request.form.getlist("feedback")

        score_str=""
        for s in score:
            if s=="":
                s="No Score"
            score_str = score_str + s +","
        feedback_str=""
        for f in feedback:
            if f=="":
                f="No FeedBack"
            feedback_str = feedback_str + f +","
        my_data.score = score_str
        my_data.feedback = feedback_str
        my_data.marked = True
        db.session.commit()
        return redirect(url_for("mark"))
        #print(my_data.id,my_data.marked)
    return render_template('mark.html',QandA_list=QandA_list)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    my_data = QuizSetList.query.filter(QuizSetList.marked == True)
    my_data = list(my_data)
    currentInfo=[]
    for data in my_data:
        if data.userid == current_user.id:
            currentInfo.append(data)
    data_webpage=[]
    for d in currentInfo:
        question_list = d.question.split(",")
        useranswer_list = d.useranswer.split(",")
        feedback_list = d.feedback.split(",")
        score_list = d.score.split(",")
        for i in question_list:
            if i == "":
                question_list.remove(i)
        for i in score_list:
            if i == "":
                score_list.remove(i)
        for i in feedback_list:
            if i == "":
                feedback_list.remove(i)
        for i in useranswer_list:
            if i == "":
                useranswer_list.remove(i)
        pair = []
        qid = []
        qid.append(d.id)
        pair.append(qid)
        pair.append(question_list)
        pair.append(useranswer_list)
        pair.append(feedback_list)
        pair.append(score_list)
        pair.append(len(question_list))
        data_webpage.append(pair)

    return render_template('feedback.html',data_webpage=data_webpage)


#fonctions de mail
@app.route("/mail") #ne fonctionne pas car : pas les droits... !
def mails():
    msg = Message("Hello",
            sender="admin@tisseo.fr",
            recipients=["baptiste.abel@tisseo.fr"])
    msg.html = '<b>test</b>'
    mail.send(msg)


def ci(departurePlace, arrivalPlace, number, lang='fr'):
    post = {
            'departurePlace': departurePlace,
            'arrivalPlace': arrivalPlace,
            'number': number,
            'lang': lang
            }
    r = req.post("https://api.tisseo.fr/v1/journeys.xml", data=post)
    return r.text


# Flask-user ; methods overriding
def login_required(func):
    """ This decorator ensures that the current user is logged in before calling the actual view.
        Calls the unauthorized_view_function() when the user is not logged in."""
    #@wraps(func)
    def decorated_view(*args, **kwargs):
        # User must be authenticated
        if not current_user.is_authenticated():
            # Redirect to unauthenticated page
            return current_app.user_manager.unauthenticated_view_function()

        # Call the actual view
        return func(*args, **kwargs)
    return decorated_view





#fonctions liées au calcul d'itinéraires
class ciForm(Form):
    departurePlace = TextField(u"Arrêt de départ", [Required(u"Il manque l'arrêt de départ.")])
    arrivalPlace = TextField(u"Arrêt d'arrivée", [Required(u"Il manquet l'arrêt d'arrivée.")])
    firstDepartureDatetime = DateTimeField( u'Jour et heure de départ', validators=[DateRange(min=datetime.now(), max=datetime.now())], default=date.today())
    submit = SubmitField(u"Recherche d'itinéraires")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        print self.firstDepartureDatetime.data
        if not Form.validate(self):
            return False

        return ci(self.departurePlace.data, self.arrivalPlace, 2)#'coucou'#calcul_API() #render_template('ci.html', itineraires=(self.departurePlace.data, self.arrivalPlace.data))

@app.route('/ci', methods = {'GET', 'POST'})
def ci(itineraires=None):
    if not 'sid' in session:
        flash(u'Vous devez vous authentifier')
        return redirect(url_for('login'))
    if itineraires:
        print itineraires
    form = ciForm()
    if request.method == 'POST':
        print 'on entre dans le POST'
        #departurePlace = request.form.get('departurePlace ')
        #arrivalPlace = request.form.get('arrivalPlace ')
        if form.validate() == False:
            print 'form validate : false'
            for errors in form.errors.values():
                for error in errors:
                    flash(error)

            return render_template('ci.html', form=form)
        else:
            url = "https://api.tisseo.fr/v1/places.json"+"?key="+globalData.api_key
            #print r.text
            itineraires = {}
            #itineraires.add(departurePlace)
            return redirect(url_for('ci', itineraires=form.validate()))

    elif request.method == 'GET':
        return render_template('ci.html', form=form)



# diverses fonctions et classes
def getRandToken():
    first = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10))
    second = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10))
    return first + second





# fonctions et méthodes liées aux données
def testLogin(login, password):
    user = User.query.filter_by(login = login).first()
    if user and user.check_password(password):
        return user.id
    else:
        flash("Mauvais login ou mot de passe.")
        return 0


def isLogged(func):
    print 'on passe dans isLogged'
    if not 'sid' in session:
        flash('Vous devez vous authentifier')
        return redirect(url_for('login'))
    else:
        return func


class User(db.Model, UserMixin):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key = True) #, server_default=db.text("nextval('resa_id_seq'::regclass)"))
    #role = Column(String(30))
    login = db.Column(db.String(100)) # ATTENTION conflit flask-user (their field is 'username', not 'login')
    name = db.Column(db.String(20))
    firstname = db.Column(db.String(20))
    email = db.Column(db.String(120))
    password = db.Column(db.String(54))
    phone = db.Column(db.String(30))
    reservations = db.relationship ('Resa', backref='t_user')
    #reservations = Column(ForeignKey(u't_resa.id'))

    roles = db.relationship('Role', secondary='t_user_roles', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, login, name, firstname, email, password):
        self.role = role
        self.login = login
        self.name = name
        self.firstname = firstname
        self.email = email.lower()
        self.set_password(password)
        self.phone = phone

    def __repr__(self):
        #return [self.login, self.email]
        return '<User %r (%r)>' % (self.login, self.email)


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        auth = check_password_hash(self.password, password)
        if not auth:#dans le cas d'un ancien mot de passe ou d'un mot de passe non encrypté
            auth = (self.password == password)
        #if not auth:
            #auth = #tests selon votre encodage de mot de passe
        return auth

# Define Role model
class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define UserRoles model
class UserRoles(db.Model):
    __tablename__ = 't_user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('t_user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('t_role.id', ondelete='CASCADE'))



def getUser(uid):
    user = User.query.filter_by(id = uid).first()
    return user

def setUser(uid, *argv):
    if argv[4] is None: # si le client n'a pas d'email
        print 'forbid auto-resa' # à faire
    else:
        print 'allow auto-resa' # à faire

    user = getUser(uid)
    user.login = argv[0]
    user.firstname = argv[1]
    user.name = argv[2]
    user.phone = argv[3]
    user.email = argv[4]
    db.session.commit()

    #implémenter un try/except
    atry = 'no error' # for testing
    if atry is None: # <- à supprimer !
        flash(u'Erreur de requête')
        print 'return 0'
        return 0
    return 1

@app.route('/autocomplete', methods = {'POST'} )
def autocomplete():
    users = {}#[]
    search = request.form.get('recherche')
    print search
    users = (db.session.query(User).order_by(User.name).filter( #attention, jointure par défaut avec AND
        User.name.ilike('%' + search + '%')\
                | User.firstname.ilike('%' + search + '%')\
                | User.login.ilike('%' + search + '%')\
                | User.phone.ilike('%' + search + '%')\
                | User.email.ilike('%' + search + '%')\
                ).all())
    return render_template("role_c/t_users.html", users = users)

@roles_required(['c_op', 'c_sup', 'admin', 'master'])
@app.route('/user/getAll')
def getUsers():
    if not 'sid' in session:
        flash('Vous devez vous authentifier')
        return redirect(url_for('login'))
    return render_template('role_c/getUsers.html')#, users = users)


class userForm(Form):
    uid = HiddenField('uid')
    login = TextField('Login')
    firstname = TextField(u'Prénom', [Required(u"L'utilisateur doit avoir un prénom.")])
    name = TextField('Nom', [Required(u"L'utilisateur doit avoir un nom.")])
    phone = TextField(u'Téléphone')
    email = TextField('E-mail')


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False, self.uid.data
        return setUser(self.uid.data, self.login.data, self.firstname.data, self.name.data, self.phone.data, self.email.data), self.uid.data

@app.route('/user/see', methods={'GET', 'POST'})
def seeUser():
    form = userForm()
    if request.method == 'POST':
        validation, uid = form.validate()
        user = getUser(uid)
        if validation == False:
            for errors in form.errors.values():
                for error in errors:
                    flash(error)
            return render_template('role_c/seeUser.html', form=form, user=user)
        else:
            flash(u'Modifications sur %s effectuées avec succès.' % str(user.login))
            return render_template('role_c/seeUser.html', form=form, user=user)

    elif request.method == 'GET':
        print 'req GET'
        uid = request.args.get('uid')
        if not uid:
            flash(u'Erreur de requête : aucun utilisateur spécifié.')
            return redirect(url_for('getUsers'))
        user = getUser(uid)
        if user:
            #resa = {}
            #for resa in user.reservations:
            #    resa[data.id] = data.reservations
            print user
            return render_template('role_c/seeUser.html', form=form, user=user)
        else:
            flash('Utilisateur introuvable.')
            return redirect(url_for('getUsers'))


@app.route('/user/merge-<int:uid>')
def mergeUsers(uid):
    user = getUser(uid)
    return render_template('role_c/mergeUsers.html', user = user)



class Resa(db.Model):
    __tablename__ = "t_resa"
    id = Column(db.Integer, primary_key = True) #, server_default=db.text("nextval('resa_id_seq'::regclass)"))
    token = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    #user_id = Column(Integer)
    seats = Column(Integer)
    prm = Column(Boolean)
    #comment = Column(String(500))
    dpt = Column(String(100))
    apt = Column(String(100))
    dpt_date = Column(DateTime)


    def __init__(self, user_id, dpt, apt, dpt_date, seats, prm):
        #la relation User-Resa est à sens unique. actuellement, Resa ne peut pas récupérer son User par référence - car pas besoin. (il faut faire un select sur t_user)
        self.token = bcrypt.gensalt() #ou alors du getRandToken()*3 ?
        self.user_id = str(user_id).title()
        self.dpt = dpt
        self.apt = apt
        self.dpt_date = dpt_date.title() #il faudra peut-être implémenter un parser ISO8601
        self.seats = seats
        self.prm = prm


def addResa(sid, uid, dpt, apt, dpt_date, seats, prm):
    if not (uid and dpt and apt and dpt_date):
        return render_template('400.html') #bad request
    if not sid:
        #actuellement la prod ne renvoie rien (comme pour une résa réussie) mais n'effectue PAS la résa.
        #nous renvoyons désormais une '400 bad request'
        return render_template('400.html')
    elif not( sid == globalData.d_sid[int(uid)] ): #le sid ne correspond pas. erreur.
        return render_template('400.html')

    #ces 5 lignes sont inutiles.
    cookie = request.cookies.get('sid')
    if cookie:
        print "requête en provenance d'une webapp"
    else:
        print "requête en provenance d'une app mobile"

    if not seats:
        seats = 1
    if not prm:
        prm = False
    if not dpt_date:
        #actuellement : set le premier horaire possible. à changer ?
        print 'info dev: à changer'

    try: #ce try est opaque côté client, mais DOIT être détaillé côté serveur /!\
        newresa = Resa(uid, dpt, apt, dpt_date, seats, prm)
        db.session.add(newresa)
        db.session.commit()
    except:
        return render_template('500.html') #erreur quelconque : internal server error

    del globalData.d_sid[int(uid)]
    return '' #reservation success. actuellement la webapp renvoie une 404... (sic).

def seeResa(user_id):
    resas = db.session.query(User).filter_by(id = 1).first().reservations
    for resa in resas:
        print resa.token
    return 'à implémenter'








@app.route('/service/getAll')
def getServices():
    if not 'sid' in session:
        flash('Vous devez vous authentifier')
        return redirect(url_for('login'))
    return render_template('role_tr/getServices.html')
    services = Service.query.order_by(Service.name).all()
    #entries = []
    resa = {}
    for user in users:
        user.phone
        resa[user.id] = user.reservations
    #    entries.appendm[user.name, user.firstname, user.login, user.phone, user.email])
    return render_template('role_/getUsers.html', users = users, resa = resa)

@app.route('/service/get')
def getService():
    return 'ceci est UN service'


def test():
    #import sqlite3
    #import psycopg2
    db_synthese = sqlite3.connect('../../base_synthese/config-prod.db3')
    db_synthese.row_factory = sqlite3.Row
    db_tad = psycopg2.connect("dbname='babel' user='babel' host='localhost' password='babel'")
    sy = db_synthese.cursor()
    tad = db_tad.cursor()

    #sy.execute("""select id, name, surname, login, password, email, phone from t026_users; """)
    sy.execute(""" select count(*), * from t044_reservations t44 group by transaction_id having count(*) > 1 """)
    #sy.execute(""" select * from t044_reservations t44 where (transaction_id =12947848928692226) """)

    return render_template('show_entries.html', entries=sy)






def tesit():
    users = User.query.order_by(User.name).all()
    for user in users:
        print user.login

    return render_template('show_entries.html', entries = users)
#afficher les sid courants

    print globalData.d_sid.items()
    for uid, sid in globalData.d_sid.items():
        print uid, sid
    return 'coucou !'



    cook = request.cookies.get('sid')
    return 'that is a cookie %s' % str(cook)



### fonctions et méthodes liées à l'interface (IHM)
@app.route('/')
#@login_required
def index():
    return isLogged(render_template('loggedin.html'))

class signupForm(Form):
    id = TextField("Id",  [Required("Please enter your id.")])
    login = TextField("Login",  [Required("Please enter your login.")])
    email = TextField("Email",  [Required("Please enter your email address."), Email("Please enter your email address.")])
    password = PasswordField('Password', [Required("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self): #test de l'existence de l'user dans la base
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True

"""
def signup():
    form = signupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:  
            newuser = User(form.id.data, form.login.data, form.email.data, form.password.data)
            session.add(newuser)
            session.commit()

            session['sid'] = newuser.login
            return redirect(url_for('index'))


    elif request.method == 'GET':
        return render_template('signup.html', form=form)
"""




def logout():
    if 'sid' not in session:
        return redirect(url_for('login'))

    session.pop('sid', None)
    session.pop('role', None)
    return redirect(url_for('index'))

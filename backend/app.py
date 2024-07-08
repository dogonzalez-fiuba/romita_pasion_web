from flask import Flask, request, jsonify
from models import db, Team, Player
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:123456@localhost:5432/flask_api_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False


@app.route('/teams', methods=['GET'])
def get_all_teams():
    try:
        teams = Team.query.all()
        teams_data = []
        for team in teams:
            team_data = {
                'id': team.id,
                'name': team.name,
                'img': team.img,
                'players': []
            }
            for player in team.players:
                player_data = {
                    'id': player.id,
                    'name': player.name,
                    'number': player.number,
                    'position': player.position,
                    'img':player.img,
                    'team_id': player.team_id
                }
                team_data['players'].append(player_data)
            teams_data.append(team_data)
        return jsonify({'teams': teams_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    

@app.route("/teams/team/<id>")
def get_team(id):
    try:
        team = Team.query.get(id)
        team_data = {
            'id': team.id,
            'name': team.name,
            'img': team.img,
            'players': []
        }
        for player in team.players:
            player_data = {
                    'id': player.id,
                    'name': player.name,
                    'number': player.number,
                    'position': player.position,
                    'img':player.img,
                    'team_id': player.team_id
            }
            team_data['players'].append(player_data)

        return jsonify(team_data)
    except: 
        return jsonify({'message': 'Internal server error'}), 500


    
    

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)

from flask import Flask, redirect, request, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Clase de configuración para la aplicación Flask
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123456@localhost:5432/flask_api_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()  # Inicializar SQLAlchemy

def create_app():
    # Crear una instancia de la aplicación Flask
    app = Flask(__name__, template_folder="../frontend", static_folder="../frontend/static")
    app.config.from_object(Config)
    CORS(app)  # Habilitar CORS en la aplicación Flask

    db.init_app(app)  # Inicializar la base de datos con la aplicación Flask

    with app.app_context():
        # Importar rutas y modelos
        init_routes(app)  # Inicializar rutas
        db.create_all()  # Crear todas las tablas en la base de datos

    return app

def init_routes(app):
    # Definir las rutas para la aplicación Flask
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/teams', methods=['GET'])
    def get_all_teams():
        try:
            teams = Team.query.all()
            print(f"Teams fetched: {teams}")  # Mensaje de depuración
            return render_template('teams.html', teams=teams)
        except Exception as error:
            print('Error', error)
            return jsonify({'message': 'Internal server error'}), 500

    @app.route('/teams/<int:id>', methods=['GET'])
    def get_team(id):
        try:
            team = Team.query.get_or_404(id)
            return render_template('team_form.html', team=team)
        except Exception as error:
            print('Error', error)
            return jsonify({'message': 'Internal server error'}), 500

    @app.route('/teams/add', methods=['GET', 'POST'])
    def add_team():
        if request.method == 'POST':
            try:
                name = request.form['name']
                img = request.form['img']
                new_team = Team(name=name, img=img)
                db.session.add(new_team)
                db.session.commit()
                return redirect(url_for('get_all_teams'))
            except Exception as error:
                print('Error', error)
                return jsonify({'message': 'Internal server error'}), 500
        return render_template('team_form.html', team=None)

    @app.route('/teams/<int:id>', methods=['POST'])
    def update_team(id):
        try:
            team = Team.query.get_or_404(id)
            data = request.form
            team.name = data['name']
            team.img = data['img']
            db.session.commit()
            return redirect(url_for('get_all_teams'))
        except Exception as error:
            print('Error', error)
            return jsonify({'message': 'Internal server error'}), 500

    @app.route('/teams/<int:id>/delete', methods=['POST'])
    def delete_team(id):
        try:
            team = Team.query.get_or_404(id)
            db.session.delete(team)
            db.session.commit()
            return redirect(url_for('get_all_teams'))
        except Exception as error:
            print('Error', error)
            return jsonify({'message': 'Internal server error'}), 500
        
    @app.route('/teams/images', methods=['GET'])
    def get_team_images():
        try:
            teams = Team.query.all()
            teams_data = [{'name': team.name, 'img': team.img} for team in teams]
            return jsonify({'teams': teams_data})
        except Exception as error:
            print('Error', error)
            return jsonify({'message': 'Internal server error'}), 500
    
    @app.route('/teams/images/view', methods=['GET'])
    def view_team_images():
        return render_template('team_images.html')

    return app

# Definición de modelos
class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer, nullable=False, unique=True)
    position = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(255), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

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

@app.route("/players")
def get_players():
    try:
        players = Player.query.all()
        players_data = []
        for player in players:
            player_data = {
                'id': player.id,
                'name': player.name,
                'number': player.number,
                'position': player.position,
                'img':player.img,
                'team_id': player.team_id                
            }
            players_data.append(player_data)
        return jsonify({"players": players_data})
    except: 
        return jsonify({'message': 'Internal server error'}), 500
    

@app.route("/players/<id_player>")
def get_player(id_player):
    try:
        player = Player.query.get(id_player)

        player_data = {
            'id': player.id,
            'name': player.name,
            'number': player.number,
            'position': player.position,
            'img':player.img,
            'team_id': player.team_id                
        }
        return jsonify({"players": player_data})
    except: 
        return jsonify({'message': 'Internal server error'}), 500




@app.route('/teams', methods=['POST'])
def add_team():
    try:
        data = request.json
        name = data.get('name')
        img = data.get('img')

        if not name or not img:
            return jsonify({'message': 'Bad request, name or img not found'}), 400
        new_team = Team(name=name, img=img)
        db.session.add(new_team)
        db.session.commit()
        return jsonify({'team': {'id': new_team.id, 'name': new_team.name, 'age': new_team.age}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    

@app.route("/teams/team/<id>", methods=['POST'])
def add_player(id):
    try:
        data = request.json
        name = data.get('name')
        number = data.get('number')
        position = data.get('position')
        img = data.get('img')
        team_id = data.get('team_id')
        if not name or not number or not position or not img or not team_id:
            return jsonify({'message': 'Bad request, name or number or position or img not found'}), 400
        new_player = Player(name=name, number=number, position=position, img=img,team_id=team_id)
        db.session.add(new_player)
        db.session.commit()
        return jsonify({'player': {'id': new_player.id, 'name': new_player.name, 'position': new_player.position, 'img': new_player.img, 'team_id': new_player.team_id }}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route("/players/<id_player>", methods=['DELETE'])
def remove_player(id_player):
    try:
        player = Player.query.get(id_player)
        db.session.delete(player)
        db.session.commit()
        return "player removed"
    except: 
        return jsonify({'message': 'Internal server error'}), 500


@app.route("/teams/team/<id>", methods=['DELETE'])
def remove_team(id):
    try:
        team = Team.query.get(id)
        db.session.delete(team)
        db.session.commit()
        return jsonify({'message': 'Team removed'})
    except: 
        return jsonify({'message': 'Internal server error'}), 500
    
@app.route("/players/<id>", methods=['PUT'])
def edit_player(id):
    try:
        player = Player.query.get(id)
        if not player:
            return jsonify({'message': 'Player not fund'}), 404
        
        data = request.json
        name = data.get('name')
        number = data.get('number')
        position = data.get('position')
        img = data.get('img')
        team_id = data.get('team_id')
        
        if not name or not number or not position or not img or not team_id:
            return jsonify({'message': 'Bad request, name or number or position or img not found'}), 400
        
        player.name = name
        player.number = number
        player.position = position
        player.img = img
        player.team_id = team_id
        db.session.commit()
        return jsonify({'player': {'id': player.id, 'name': player.name, 'position': player.position, 'img': player.img, 'team_id': player.team_id }}), 200
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)
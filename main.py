from flask import Flask, jsonify

from data_dao import DataDAO

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

data_dao = DataDAO('netflix.db')


@app.route('/movie/<title>')
def search_by_title(title):
    result = data_dao.search_by_title(title)
    return result


@app.route('/movie/<int:from_year>/to/<int:to_year>')
def search_by_realise_year(from_year, to_year):
    result = data_dao.search_by_years(from_year, to_year)
    return jsonify(result)


@app.route('/movie/rating/<ratings>')
def search_by_ratings(ratings):
    result = data_dao.search_by_rating(ratings)
    return jsonify(result)


@app.route('/movie/genre/<genre>')
def search_by_genre(genre):
    result = data_dao.search_by_genre(genre)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

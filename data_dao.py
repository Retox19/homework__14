import sqlite3


class DataDAO:

    def __init__(self, path):
        self.path = path

    def execute_query(self, sql_query):
        """
        Подключается к базе данных и выполняет запрос sql_query.
        """
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            executed_query = cursor.fetchall()
        return executed_query

    def search_by_title(self, title):
        """
        Выполняет поиск фильма по названию
        """
        query = f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title LIKE '{title}%' COLLATE NOCASE
                ORDER BY release_year DESC
                LIMIT 1
                """

        result = self.execute_query(query)
        if not result:
            return "Такого фильма нет"

        title = {
            "title": result[0][0],
            "country": result[0][1],
            "release_year": result[0][2],
            "genre": result[0][3],
            "description": result[0][4]
        }
        return title

    def search_by_years(self, from_year, to_year):
        """
        Выполняет поиск 100 фильмов в заданном диапозоне лет(от/до)
        """
        query = f"""
                SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN {from_year} AND {to_year}
                ORDER BY release_year 
                LIMIT 100
                """
        movies = self.execute_query(query)
        result = []
        for movie in movies:
            result.append({"title": movie[0], "release_year": movie[1]})
        return result

    def search_by_rating(self, rating):
        """
        Выполняет поиск 100 фильмов по получаемому рейтингу
        """
        rating_parameters = {"children": "'G'", "family": "'G', 'PG', 'PG-13'", "adult": "'R', 'NC-17'"}
        if rating not in rating_parameters:
            return "Вы ошиблись при вводе рейтинга"

        query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating in ({rating_parameters[rating]})
                LIMIT 100
                """

        movies = self.execute_query(query)
        result = []
        for movie in movies:
            result.append({"title": movie[0], "rating": movie[1], "description": movie[2]})
        return result

    def search_by_genre(self, genre):
        """
        Выполняет поиск фильмов по жанру
        """
        query = f"""
            SELECT title, description from netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10
            """
        movies = self.execute_query(query)
        result = []
        for movie in movies:
            result.append({"title": movie[0], "description": movie[1]})
        return result

    def search_actors(self, actor_1, actor_2):
        """
        Получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast
        и возвращает список тех, кто играет с ними в паре больше 2 раз.
        """

        query = f"""
            SELECT `cast` from netflix
            WHERE `cast` LIKE '%{actor_1}%' AND `cast` LIKE '%{actor_2}%' 
            """
        all_actors = self.execute_query(query)
        actor_list = []
        for actors in all_actors:
            actor_list.extend(actors[0].split(', '))

        result = []
        for actor in actor_list:
            if actor not in [actor_1, actor_2]:
                if actor_list.count(actor) > 2:
                    result.append(actor)

        result = set(result)
        result = list(result)
        return result

    def search_by_params(self, type, release_year, genre):
        """
        Принимает тип картины (фильм или сериал), год выпуска и жанр
        и возвращает список названий картин с их описаниями в JSON.
        """
        query = f"""
                SELECT title, description
                from netflix
                WHERE type LIKE '{type}'
                AND release_year LIKE '{release_year}'
                AND listed_in LIKE '%{genre}%'
                """

        movies = self.execute_query(query)
        result = []
        for movie in movies:
            result.append({"title": movie[0], "description": movie[1]})

        return result

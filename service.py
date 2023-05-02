from django.db import connection

class ApplicationService:
    def query_processor(self,query):
        cursor = connection.cursor()
        cursor.execute(query)
        try:
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except:
            return "okay"
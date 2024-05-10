from database.DB_connect import DBConnect
from model.ArtObject import ArtObject
from model.Connessione import Connessione


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllObjects():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM objects"
        cursor.execute(query)

        for row in cursor:
            result.append(ArtObject(
                **row))  # posso farlo solo se nella classe ho definito gli attributi con lo stesso nome delle colonne del db
            # e facendo così posso passare un dizionario con tutti i valori e lui li assegna automaticamente
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni(idMap: dict):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select eo1.object_id as u, eo2.object_id as v, count(*) as weight
        from exhibition_objects eo1, exhibition_objects eo2
        where eo1.exhibition_id = eo2.exhibition_id 
        and eo1.object_id < eo2.object_id 
        group by eo1.object_id, eo2.object_id 
        order by weight desc """
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(idMap[row['u']], idMap[row['v']], row['weight']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getWeight(u: ArtObject, v: ArtObject):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(*)
                    from exhibition_objects eo1, exhibition_objects eo2
                    where eo1.exhibition_id = eo2.exhibition_id 
                    and eo1.object_id < eo2.object_id 
                    and eo1.object_id = %s
                    and eo2.object_id = %s"""
        cursor.execute(query, (u.object_id, v.object_id))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    # @staticmethod
    # def get_all_genes():
    #     cnx = DBConnect.get_connection()
    #     result = []
    #     if cnx is None:
    #         print("Connessione fallita")
    #     else:
    #         cursor = cnx.cursor(dictionary=True)
    #         query = """SELECT *
    #                 FROM genes"""
    #         cursor.execute(query)
    #
    #         for row in cursor:
    #             result.append(Gene(**row))
    #
    #         cursor.close()
    #         cnx.close()
    #     return result

    # @staticmethod
    # def get_all_interactions():
    #     cnx = DBConnect.get_connection()
    #     result = []
    #     if cnx is None:
    #         print("Connessione fallita")
    #     else:
    #         cursor = cnx.cursor(dictionary=True)
    #         query = """SELECT *
    #                    FROM interactions"""
    #         cursor.execute(query)
    #
    #         for row in cursor:
    #             result.append(Interaction(**row))
    #
    #         cursor.close()
    #         cnx.close()
    #     return result

    @staticmethod
    def getAllChromosomes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                        select distinct g.Chromosome 
                        from genes g 
                        order by g.Chromosome asc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Chromosome"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(min, max):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select g.*
                        from genes g
                        where g.Chromosome >= %s and g.Chromosome <= %s"""

            cursor.execute(query, (min,max))

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(min, max, idMapG):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct  g1.GeneID as g1, g1.Function as f1, g2.GeneID as g2, g2.Function as f2, i.Expression_Corr as peso
                        from (select g.GeneID, g.Function, c.Localization 
                        from genes g, classification c 
                        where g.Chromosome >= %s and g.Chromosome <= %s
                        and g.GeneID = c.GeneID ) as g1, 
                        ( select g.GeneID , g.Function, c.Localization 
                        from genes g, classification c 
                        where g.Chromosome >= %s and g.Chromosome <= %s
                        and g.GeneID = c.GeneID ) g2, interactions i
                        where g1.GeneID != g2.GeneID
                        and g1.GeneID = i.GeneID1 and g2.GeneID = i.GeneID2 
                        and g1.Localization = g2.Localization"""
            cursor.execute(query, (min, max, min, max))

            for row in cursor:
                gene1 = idMapG[(row["g1"], row["f1"])]
                gene2 = idMapG[(row["g2"], row["f2"])]
                result.append((gene1, gene2, row["peso"]))

            cursor.close()
            cnx.close()
        return result
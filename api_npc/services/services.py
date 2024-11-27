from flask import jsonify
from logger.logger_base import Logger

class NpcService:
    def __init__(self, db_conn): #This class is used to interact with the database
        self.logger = Logger()
        self.db_conn = db_conn
    
    def get_all_npcs(self): #This method fetches all npcs from the database
        try:
            npcs = list(self.db_conn.db.npcs.find()) #This line fetches all npcs from the database using pymongo
            return npcs
        except Exception as e:
            self.logger.error(f'Error fetching npcs from the database: {e}')
            return jsonify({'error': f'Error fetching npcs from the database: {e}'}), 500
    
    def add_npc(self, new_npc): #This method adds a new npc to the database
        try:
            max_id = self.db_conn.db.npcs.find_one(sort=[('_id', -1)])['_id']
            next_id = max_id + 1 #This line gets the next id for the new npc
            new_npc['_id'] = next_id
            self.db_conn.db.npcs.insert_one(new_npc)
            return new_npc
        except Exception as e:
            self.logger.error(f'Error creating a new npc: {e}')
            return jsonify({'error': f'Error creating a new npc: {e}'}), 501

    def get_npc_by_id(self, npc_id): #This method fetches a npc by its id
        try:
            npc = self.db_conn.db.npcs.find_one({'_id': npc_id})
            return npc
        except Exception as e:
            self.logger.error(f'Error fetching npc by id: {e}')
            return jsonify({'error': f'Error fetching npc by id: {e}'}), 502

    def update_npc(self, npc_id, npc): #This method updates a npc
        try:
            updated_npc = self.get_npc_by_id(npc_id) #This line verifies if the npc exists
            if updated_npc:
                updated_npc = self.db_conn.db.npcs.update_one({'_id': npc_id}, {'$set': npc})
                if updated_npc.modified_count > 0:
                    return updated_npc
                else:
                    return 'The npc is already up-to-date'
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error updating npc: {e}')
            return jsonify({'error': f'Error updating npc: {e}'}), 503
    
    def delete_npc(self, npc_id): #This method deletes a npc
        try:
            deleted_npc = self.get_npc_by_id(npc_id)
            if deleted_npc:
                self.db_conn.db.npcs.delete_one({'_id': npc_id})
                return deleted_npc
            else:
                return None
        except Exception as e:
            self.logger.error(f'Error deleting npc: {e}')
            return jsonify({'error': f'Error deleting npc: {e}'}), 504

if __name__ == '__main__':
    from models.models import NpcModel
    logger = Logger()
    db_conn = NpcModel()
    npc_service = NpcService(db_conn)
    try:
        db_conn.connect_to_database()
        #Get all NPCs
        npcs = npc_service.get_all_npcs()
        logger.info(f'NPCs fetched: {npcs}')
        #Add a new NPC
        new_npc = npc_service.add_npc({'name': 'Goblin', 'type': 'monster'}) #These atributes are yet to be defined using the handbook
        logger.info(f'New NPC added: {new_npc}')
        #Get NPC by id
        npc = npc_service.get_npc_by_id(1)
        logger.info(f'NPC fetched by id: {npc}')
        #Update NPC
        updated_npc = npc_service.update_npc(1, {'name': 'Goblin', 'type': 'monster', 'level': 1}) #These atributes are yet to be defined using the handbook
        logger.info(f'NPC updated: {updated_npc}')
        #Delete NPC
        deleted_npc = npc_service.delete_npc(1)
        logger.info(f'NPC deleted: {deleted_npc}')
    except Exception as e:
        logger.error(f'An error occurred: {e}')
    finally:
        db_conn.close_connection()
        logger.info('Connection to database closed')
        


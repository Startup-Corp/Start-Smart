from objects.dbManager import db as Connection

class AddProject:
    def execute(self,
                owner_id: str,
                request_id: int,
                title: str,
                
                ):
        Connection.insert(
            'Projects',
            {
                'owner_id': owner_id,
                'request_id': request_id,
                'title': title,
            })
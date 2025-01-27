import json
from app import create_app
from app.extensions import db
from app.models import *  # This will import all models

def import_data():
    """Import data from JSON files into MySQL database."""
    app = create_app()
    
    with app.app_context():
        try:
            # Import mods data
            with open('static/data/mods_min.json', 'r', encoding='utf-8') as f:
                mods_data = json.load(f)
                print(f"Loaded {len(mods_data)} mods from mods_min.json")
                
                # Clear existing mods data
                db.session.query(Mod).delete()
                
                # Import each mod
                for url, mod_data in mods_data.items():
                    mod = Mod(
                        url=url,
                        title=mod_data.get('title'),
                        creator=mod_data.get('creator'),
                        description=mod_data.get('description'),
                        downloads_count=mod_data.get('downloads', {}).get('download_count', 0),
                        cover_image=mod_data.get('images', {}).get('cover'),
                        additional_images=json.dumps(mod_data.get('images', {}).get('additional', [])),
                        download_links=json.dumps(mod_data.get('downloads', {}).get('by_host', {}))
                    )
                    db.session.add(mod)
                
                db.session.commit()
                print("Successfully imported mods data")

            # Import tracks data
            with open('static/data/tracks_min.json', 'r', encoding='utf-8') as f:
                tracks_data = json.load(f)
                print(f"Loaded {len(tracks_data)} tracks from tracks_min.json")
                
                # Clear existing tracks data
                db.session.query(Track).delete()
                
                # Import each track
                for url, track_data in tracks_data.items():
                    track = Track(
                        url=url,
                        title=track_data.get('title'),
                        creator=track_data.get('creator'),
                        description=track_data.get('description'),
                        downloads_count=track_data.get('downloads', {}).get('download_count', 0),
                        cover_image=track_data.get('images', {}).get('cover'),
                        additional_images=json.dumps(track_data.get('images', {}).get('additional', [])),
                        download_links=json.dumps(track_data.get('downloads', {}).get('by_host', {}))
                    )
                    db.session.add(track)
                
                db.session.commit()
                print("Successfully imported tracks data")

        except Exception as e:
            print(f"Error importing data: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    import_data()

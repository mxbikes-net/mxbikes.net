from app.extensions import db

class Mod(db.Model):
    __tablename__ = 'mods'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    title = db.Column(db.String(200))
    creator = db.Column(db.String(100))
    description = db.Column(db.Text)
    downloads_count = db.Column(db.Integer, default=0)
    cover_image = db.Column(db.String(500))
    additional_images = db.Column(db.Text)  # JSON string of image URLs
    download_links = db.Column(db.Text)  # JSON string of download links by host
    
    def __repr__(self):
        return f'<Mod {self.title}>'

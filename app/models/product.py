from ..extensions import db
import json

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    file_path = db.Column(db.String(255))
    product_type = db.Column(db.String(20))  # 'mod' or 'track'
    mod_type = db.Column(db.String(20))      # 'free' or 'paid'
    creator = db.Column(db.String(255))
    images = db.Column(db.Text)              # JSON string for image URLs
    downloads = db.Column(db.Text)           # JSON string for download links
    guid_required = db.Column(db.Boolean)
    download_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer)
    password_release_time = db.Column(db.DateTime)

    def _extract_links_from_value(self, value):
        """Helper method to extract links from various value types"""
        links = []
        if isinstance(value, list):
            links.extend(link for link in value if isinstance(link, str) and link.startswith('http'))
        elif isinstance(value, str) and value.startswith('http'):
            links.append(value)
        elif isinstance(value, dict):
            for v in value.values():
                links.extend(self._extract_links_from_value(v))
        return links

    def to_dict(self):
        # Parse JSON strings into Python dictionaries
        try:
            images_dict = json.loads(self.images) if self.images else {}
        except (json.JSONDecodeError, TypeError):
            images_dict = {}
        
        try:
            downloads_dict = json.loads(self.downloads) if self.downloads else {}
        except (json.JSONDecodeError, TypeError):
            downloads_dict = {}
        
        # Ensure downloads is a dictionary
        if not isinstance(downloads_dict, dict):
            downloads_dict = {}
            
        # Initialize all_links list
        all_links = []
        
        # Process by_type structure
        if 'by_type' in downloads_dict and isinstance(downloads_dict['by_type'], dict):
            for type_links in downloads_dict['by_type'].values():
                all_links.extend(self._extract_links_from_value(type_links))
                    
        # Process by_host structure
        if 'by_host' in downloads_dict and isinstance(downloads_dict['by_host'], dict):
            for host_links in downloads_dict['by_host'].values():
                all_links.extend(self._extract_links_from_value(host_links))
                    
        # Process direct links array if it exists
        if 'links' in downloads_dict:
            all_links.extend(self._extract_links_from_value(downloads_dict['links']))

        # Process single link if it exists
        if 'link' in downloads_dict:
            all_links.extend(self._extract_links_from_value(downloads_dict['link']))
            
        # Process any top-level arrays or links
        for key, value in downloads_dict.items():
            if key not in ['by_type', 'by_host', 'links', 'link', 'download_count']:
                all_links.extend(self._extract_links_from_value(value))
                    
        # If no links were found in any structure, initialize default structure based on type
        if not downloads_dict:
            if self.product_type == 'mod':
                downloads_dict = {
                    'by_type': {'mod': []},
                    'by_host': {},
                    'download_count': 0
                }
            else:  # track
                downloads_dict = {
                    'by_type': {'other': []},
                    'by_host': {},
                    'download_count': 0
                }
        
        # Preserve the original structure while ensuring links array exists
        downloads_dict['links'] = list(set(link for link in all_links if link and isinstance(link, str) and link.startswith('http')))
        
        # Preserve download count if it exists
        if 'download_count' not in downloads_dict and isinstance(self.download_count, int):
            downloads_dict['download_count'] = self.download_count
        
        return {
            'id': self.id,
            'title': self.name,
            'description': self.description,
            'creator': self.creator,
            'images': images_dict,
            'downloads': downloads_dict,
            'type': self.product_type,
            'mod_type': self.mod_type,
            'download_count': self.download_count
        }

    def __repr__(self):
        return f"<Product {self.name}>"

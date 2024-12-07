from sqlalchemy import CheckConstraint

from app.auth.utils import mask_value
from app.extensions import db
from app.artists import artistService


class Position(db.Model):
    __tablename__ = "positions"

    account_id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    average_entry_price = db.Column(db.Float, nullable=False)

    __table_args__ = (
        CheckConstraint('quantity > 0', name="check_quantity_positive"),
    )

    @property
    def masked_account_id(self):
        return mask_value(self.account_id)

    @property
    def serialize(self):

        asset_info = self.asset_info

        return {
            'id': f'{self.masked_account_id}:{asset_info.id}',
            'account_id': self.masked_account_id,
            'asset_info': asset_info.serialize,
            'quantity': self.quantity,
            'average_entry_price': self.average_entry_price
        }

    @property
    def asset_info(self):
        artist_info = artistService.get_artist_from_id(self.asset_id)

        # TODO: Add error handling

        return artist_info
        # return {
        #     "id": artist_info['id'],
        #     "url": artist_info['external_urls']['spotify'],
        #     "followers": artist_info['followers']['total'],
        #     "name": artist_info['name'],
        #     "popularity": artist_info['popularity'],
        #     "type": artist_info['type']
        # }
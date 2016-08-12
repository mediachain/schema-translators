from __future__ import unicode_literals
import os
from mediachain.translation.translator import Translator

class Artsy(Translator):

    @staticmethod
    def translator_id():
        return 'artsy'

    @staticmethod
    def get_image(json):
        try:
            return json['image_url']
        except KeyError:
            pass
        try:
            return json['_links']['image']['href']
        except KeyError:
            return "NO_IMAGE"


    @staticmethod
    def translate(json):
        image = Artsy.get_image(json)

        # extract artwork Artefact
        data = {'_id': u'artsy_' + json['id'],
                'title': json['title'],
                'category': json['category'],
                'medium': json['medium'],
                'collecting_institution': json['collecting_institution'],
                'created_at': json['created_at'],
                'image_url': image
                }

        if 'artist' in json and isinstance(json['artist'], dict):
            artist_name = json['artist']['name']
            data['artist'] = artist_name

            # extract artist Entity
            artist_entity = {
                '__mediachain_object__': True,
                'type': 'entity',
                'meta': {
                    'data': {
                        'name': artist_name
                    }
                }
            }

        data['thumbnail'] = {
            '__mediachain_asset__': True,
            'uri': image
        }

        artwork_artefact = {
            '__mediachain_object__': True,
            'type': 'artefact',
            'meta': {'data': data}
        }

        translated = {
            'canonical': artwork_artefact,
            'chain': [
            ]
        }

        try:
            chain_entry = {'__mediachain_object__': True,
                'type': 'artefactCreatedBy',
                'meta': {},
                'entity': artist_entity
            }
            translated['chain'].append(chain_entry)
        except NameError:
            pass

        return translated

    @staticmethod
    def can_translate_file(file_path):
        ext = os.path.splitext(file_path)[-1]
        return ext.lower() == '.json'


from base64 import b64decode

from config import Config


def generate_mask(seed):
    """ Creates a new mask from a seed for making ids """
    return ((seed * 1664525) + 1013904223) % 2**32

def mask_value(id, seed=int.from_bytes(b64decode(Config.SECRET_KEY), 'big')):
    """ Masks a given value to obfuscate the original value """
    mask = generate_mask(seed)
    return hex(id ^ mask)[2:]

def unmask_value(masked_id, seed=int.from_bytes(b64decode(Config.SECRET_KEY), 'big')):
    """ Unmakes obfuscated values """
    mask = generate_mask(seed)
    return int(masked_id, 16) ^ mask
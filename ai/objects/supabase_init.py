from supabase import create_client, Client
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

url: str = config['supabase']['url']
key: str = config['supabase']['key']
supabase: Client = create_client(url, key)
from typing import NoReturn, List
import sys
from pathlib import Path

sys.path.append(Path(__file__))

from telethon import TelegramClient
import fire
import pandas as pd

from utils import load_config

async def collect_memes(client: TelegramClient,
                        groups_sources: List[str],
                        max_posts: int,
                        path_media_dir: str,
                        meme_cache: pd.DataFrame = None,
                        csv_file_name: str = 'tele_data.csv'
                        ) -> NoReturn:
    """
    Load last memes and save info about message in post.
    Media data will have name by the next pattern '{channel_id}_{post_id}'.
    Saved dataframe with information about post by path `path_media_dir/csv_file_name`.

    Args:
        client (TelegramClient): client for connect to telegram api and recieve messages
        groups_sources (List[str]): telegram sources on groups for loading memes
        max_posts (int): max post per one channel
        path_media_dir (str): path to directory for save media data;
        meme_cache (pd.DataFrame, optional): check that post was viewed (by columns 'post_id', 'channel_id'). Defaults to None.
        csv_file_name (str, optional): name of pd.DataFrame with columns (channel_id, post_id, message, path_media). Default to 'tele_data.csv'

    Returns:
        NoReturn.
    """
    me = await client.get_entity('me')
    data_info = []
    for group_src in groups_sources:
        channel = await client.get_entity(group_src)
        posts = client.iter_messages(
                channel,
                limit=max_posts,
                reverse=False
        )
        async for post in posts:
            channel_id, post_id = post.peer_id.channel_id, post.id
            if meme_cache is not None and \
            (meme_cache['post_id'] == post_id & meme_cache['channel_id'] == channel_id).sum() > 0:
                continue
            cur_info = {
                'message': post.message,
                'channel_id': channel_id,
                'post_id': post_id,
                'path_media': None 
            }
            if hasattr(post, 'media') and post.media:
                path_media = f'{path_media_dir}/{str(post.peer_id.channel_id)}_{str(post.id)}'
                await client.download_media(post.media, path_media)
                cur_info['path_media'] = path_media
            data_info.append(cur_info)

    data = pd.DataFrame(data_info)
    path_dataframe = f'{path_media_dir}/{csv_file_name}'
    data.to_csv(path_dataframe)
    client.disconnect()

def run_collector(path_config: str) -> NoReturn:
    """
    Run config for collect images

    Args:
        path_config (str): path to config

    Returns:
        NoReturn.
    """
    config = load_config(path_config)
    api_id = config['api']['id']
    api_hash = config['api']['hash']
    client = TelegramClient('user_content_getter', api_id, api_hash)
    client.start()
    client.loop.run_until_complete(
        collect_memes(
            client,
            config['channels'],
            config['max_posts'],
            config['path_media_dir']
        )
    )
    
if __name__ == '__main__':
    fire.Fire(run_collector)
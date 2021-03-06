#! /usr/bin/env python
import argparse

from fabric.operations import local
from torrentmediasearcher import TorrentMediaSearcher

from subtitles import get_subtitle


def main(name, season=None, episode=None, sub_lang=None, serve=False,
         quality=None):

    def get_magnet(results):
        magnet = results['magnet']
        command = "peerflix \"%s\"" % magnet
        if sub_lang is not None:
            print("Obteniendo subtitulo")
            subtitle = get_subtitle(magnet, sub_lang)
            if subtitle is not None:
                command += " -t %s" % subtitle

        if not serve:
            command += " --vlc"

        local(command, capture=False)

    print("Obteniendo magnet")
    search = TorrentMediaSearcher
    if season is None and episode is None:
        search.request_movie_magnet('torrentproject', name,
                                    callback=get_magnet, quality=quality)
    else:
        search.request_tv_magnet(provider='eztv', show=name,
                                 season=int(season), episode=int(episode),
                                 quality=quality, callback=get_magnet)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("name")

    parser.add_argument("sea_ep", nargs='*', default=[None, None])
    parser.add_argument("--sub", nargs='?', default=None)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--quality", nargs='?', default=None)
    args = parser.parse_args()

    main(args.name, season=args.sea_ep[0], episode=args.sea_ep[1],
         sub_lang=args.sub, serve=args.serve, quality=args.quality)

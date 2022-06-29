

import aria2p
import os

if __name__ == "__main__":
    # initialization, these are the default values
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://192.168.30.30",
            port=7000,
            secret=""
        )
    )

    # add downloads
    magnet_uri = "magnet:?xt=urn:btih:64F18CF55D0322D02940577AE4E33AADF36B6A97"

    download = aria2.add_magnet(magnet_uri)
    os.system("pause")
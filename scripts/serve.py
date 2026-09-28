"""Preview the static site locally with its clean /page URLs."""
from argparse import ArgumentParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

PUBLIC = Path(__file__).resolve().parents[1] / 'dist'


class SiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def send_head(self):
        original = self.path
        url = urlsplit(self.path)
        relative = unquote(url.path).lstrip('/')
        candidate = (PUBLIC / (relative + '.html')).resolve()
        if (not Path(relative).suffix and candidate.is_relative_to(PUBLIC)
                and candidate.is_file()):
            self.path = urlunsplit(('', '', url.path + '.html', url.query, ''))
        try:
            return super().send_head()
        finally:
            self.path = original


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), SiteHandler)
    print(f'AsriyyaMUN preview: http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

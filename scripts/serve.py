"""Preview the static site locally with its clean /page URLs."""
from argparse import ArgumentParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

PUBLIC = Path(__file__).resolve().parents[1] / 'dist'


class SiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def send_error(self, code, message=None, explain=None):
        error_page = PUBLIC / '404.html'
        if code != 404 or not error_page.is_file():
            return super().send_error(code, message, explain)
        body = error_page.read_bytes()
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(body)

    def send_head(self):
        original = self.path
        url = urlsplit(self.path)
        relative = unquote(url.path).strip('/')
        candidate = (PUBLIC / (relative + '.html')).resolve()
        if (not Path(relative).suffix and candidate.is_relative_to(PUBLIC)
                and candidate.is_file()):
            self.path = urlunsplit(('', '', url.path.rstrip('/') + '.html', url.query, ''))
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

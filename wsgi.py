# -*- coding: utf-8 -*-
from st import create_app


application = create_app('prod')


if __name__ == '__main__':
    application.run()

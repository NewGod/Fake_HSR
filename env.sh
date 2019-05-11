#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=development
export DYLD_LIBRARY_PATH=/usr/local/mysql-8.0.15-macos10.14-x86_64/lib/:$DYLD_LIBRARY_PATH

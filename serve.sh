#!/bin/bash
python -m uvicorn buttonRecorder.main:app --reload --host 0.0.0.0
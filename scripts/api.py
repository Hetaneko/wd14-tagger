import numpy as np
from fastapi import FastAPI, Body
from fastapi.exceptions import HTTPException
import requests
import os
import gradio as gr
import subprocess
import modules.shared
from PIL import Image
from io import BytesIO
import base64
from tagger.interrogator import Interrogator

from modules.api.models import *
from modules.api import api

def civitdown_api(_: gr.Blocks, app: FastAPI):
    @app.post("/mikww/tagimg")
    async def civitdown(
        image: str = Body("none", title='Image'),
        undesired: str = Body("none", title='Undesired Tags'),
    ):
        def image_interrogate():
        	im = Image.open(BytesIO(base64.b64decode(image)))
        	result = interrogator.interrogate(im)
        	
        	return Interrogator.postprocess_tags(
        	    result[1],
        	    threshold=0.4,
        	    escape_tag=False,
        	    replace_underscore=False,
        	    exclude_tags=undesired)

        return "Success"
try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(civitdown_api)
except:
    pass
